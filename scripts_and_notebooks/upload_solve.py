"""Manual entry of cube solve time into the database."""

from datetime import datetime
import rubik_module

rubik_module.show_title()
print("Enter the following data:")
solve_date = input("Date (in YEAR-MONTH-DAY format) e.g., '2026-03-20' or 'today': ")
if solve_date == "today":
    solve_date = datetime.now().strftime("%Y-%m-%d")

cube = input("Enter the cube type (e.g., 2x2x2, 3x3x3, Megaminx): ").lower()
personal_record = rubik_module.show_record(cube=cube)
average = rubik_module.calculate_absolute_average(cube=cube)
print("Current average:", average, "\n")
upload_another_solve = "yes"

while upload_another_solve in ("yes", "y"):
    minutes = int(input("Minutes: "))
    seconds = int(input("Seconds: "))
    milliseconds = float(input("Milliseconds (e.g., 0.43): "))
    time_taken = (minutes * 60) + seconds + milliseconds
    print()

    rubik_module.check_new_record(time_taken, cube)
    personal_record = rubik_module.search_record(cube)
    rubik_module.diff_current_record_time(record=personal_record, time_taken=time_taken)
    # Average information
    rubik_module.diff_current_average_time(cube=cube, time_taken=time_taken)
    rubik_module.average_last_total_solves(cube=cube, num_last_solves=100)
    rubik_module.average_last_total_solves(cube=cube, num_last_solves=12)
    rubik_module.average_last_total_solves(cube=cube, num_last_solves=5)

    with open(file="../database.csv", mode="a", encoding="utf-8") as db_file:
        db_file.write(f"{solve_date}\t{time_taken}\t{cube}\n")

    print("Solve time added to database:", solve_date, time_taken, cube)
    upload_another_solve = input("\nDo you want to enter another solve time for the same cube and date? (yes or no): ")
