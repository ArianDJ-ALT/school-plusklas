import pandas as pd
from collections import defaultdict
import itertools

def process_input(file_path):
    # Stap 1: Converteer Excel naar CSV
    excel_file = pd.ExcelFile(file_path)
    data = excel_file.parse(excel_file.sheet_names[0])
    csv_path = file_path.replace(".xlsx", ".csv")
    data.to_csv(csv_path, index=False)

    # Stap 2: Haal dubbele rijen weg
    data = data.drop_duplicates()

    # Stap 3: Groepeer docenten per klas
    class_teachers = defaultdict(set)
    for _, row in data.iterrows():
        class_group = row['Gevolgd door groepen']
        teachers = row['Gegeven door medewerkers']
        if pd.notna(teachers):
            class_teachers[class_group].update(teachers.split(","))

    return class_teachers

def plan_meetings(class_teachers, start_time, end_time, meeting_duration=30, rooms=None):
    if rooms is None:
        rooms = ["222", "223", "224"]

    # Maak een lijst met tijdslots
    time_slots = []
    current_time = start_time
    while current_time < end_time:
        time_slots.append(current_time)
        current_time += meeting_duration

    # Plan gesprekken per tijdslot
    schedule = defaultdict(list)
    available_teachers = {teacher: True for teacher in set(itertools.chain(*class_teachers.values()))}

    for time_slot in time_slots:
        for room in rooms:
            for class_group, teachers in class_teachers.items():
                if all(available_teachers[teacher] for teacher in teachers):
                    schedule[time_slot].append((room, class_group, teachers))
                    for teacher in teachers:
                        available_teachers[teacher] = False
                    break
    return schedule

def main():
    file_path = "input.xlsx"  # Inputbestand
    start_time = 9.3 * 60  # Starttijd in minuten (bijv. 8:00 = 480)
    end_time = 16.4 * 60  # Eindtijd in minuten (bijv. 17:00 = 1020)

    class_teachers = process_input(file_path)
    schedule = plan_meetings(class_teachers, start_time, end_time)

    # Print het schema
    for time_slot, meetings in schedule.items():
        print(f"Tijdslot {time_slot // 60:02}:{time_slot % 60:02}")
        for room, class_group, teachers in meetings:
            print(f"  Lokaal {room}: {class_group} ({', '.join(teachers)})")

if __name__ == "__main__":
    main()
