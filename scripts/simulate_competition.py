"""Script that calculates the time of 5 solves (or 3 in the case of large cubes) and provides the average of the results excluding
the minimum and maximum times."""

from time import time
import rubik_module


small_cube_types = rubik_module.small_cube_types
dodecahedrons = rubik_module.dodecahedrons
small_cubes_moves = rubik_module.small_cubes_moves
large_cubes_moves = rubik_module.large_cubes_moves
pyraminx_moves = rubik_module.pyraminx_moves
dodecahedron_moves = rubik_module.dodecahedron_moves
results_list = []


def main_function():
    """Main function"""
    rubik_module.show_title()
    cube = input("Enter the cube type (e.g., 2x2x2, 3x3x3, megaminx): ").lower()
    personal_record = rubik_module.show_record(cube=cube)
    average = rubik_module.calculate_absolute_average(cube=cube)
    print("Current average:", average)

    if cube in ("6x6x6", "7x7x7"):
        rounds_list = [1, 2, 3]
    else:
        rounds_list = [1, 2, 3, 4, 5]

    for round_num in rounds_list:
        print(f"\nRound number {round_num}")

        if cube == "pyraminx":
            rubik_module.generate_random_moves(moves_list=pyraminx_moves)
        elif cube in dodecahedrons:
            rubik_module.generate_random_moves(moves_list=dodecahedron_moves)
        elif cube in small_cube_types:
            rubik_module.generate_random_moves(moves_list=small_cubes_moves)
        else:
            rubik_module.generate_random_moves(moves_list=large_cubes_moves)

        input("Press enter to start: ")
        print("Timer started!")
        start_time = time()
        input("Press enter to finish: ")
        end_time = time()
        time_taken = round(number=end_time - start_time, ndigits=2)
        print("Done!\n")
        minutes, seconds = rubik_module.convert_seconds(time_taken)
        rubik_module.show_current_time(minutes, seconds)
        print("Solve time added to database")

        rubik_module.check_new_record(time_taken=time_taken, cube=cube)
        rubik_module.save_data(time_taken=time_taken, cube=cube)
        results_list.append(time_taken)

    print("\nList of all results", results_list)
    maximum_time = max(results_list)
    minimum_time = min(results_list)

    if cube not in ("6x6x6", "7x7x7"):
        print("Removing the worst result:", maximum_time)
        print("Removing the best result:", minimum_time)
        results_list.remove(maximum_time)
        results_list.remove(minimum_time)
        print("List of remaining results", results_list)

    average_3_solves = round(number=(results_list[0] + results_list[1]
                                     + results_list[2]) / 3, ndigits=2)
    minutes, seconds = rubik_module.convert_seconds(average_3_solves)

    if minutes == 0:
        print(f"Average of the three remaining solves: {seconds} seconds")
    elif minutes == 1:
        print(f"Average of the three remaining solves: {minutes} minute and {seconds} seconds")
    else:
        print(f"Average of the three remaining solves: {minutes} minutes and {seconds} seconds")


if __name__ == "__main__":
    main_function()
