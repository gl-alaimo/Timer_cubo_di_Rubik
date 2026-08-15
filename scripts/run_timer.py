"""Script that calculates the solve time and provides various statistics."""

import rubik_module


small_cube_types = rubik_module.small_cube_types
dodecahedrons = rubik_module.dodecahedrons
small_cubes_moves = rubik_module.small_cubes_moves
large_cubes_moves = rubik_module.large_cubes_moves
pyraminx_moves = rubik_module.pyraminx_moves
dodecahedron_moves = rubik_module.dodecahedron_moves


def main_function():
    """Main function"""
    rubik_module.show_title()
    cube = input("Enter the cube type (e.g., 2x2x2, 3x3x3, megaminx): ").lower()
    retry = "yes"
    print()

    while retry == "yes" or retry == "si" or retry == "sì":
        if cube == "pyraminx":
            rubik_module.generate_random_moves(moves_list=pyraminx_moves)
        elif cube in dodecahedrons:
            rubik_module.generate_random_moves(moves_list=dodecahedron_moves)
        elif cube in small_cube_types:
            rubik_module.generate_random_moves(moves_list=small_cubes_moves)
        else:
            rubik_module.generate_random_moves(moves_list=large_cubes_moves)

        personal_record = rubik_module.show_record(cube=cube)
        average = rubik_module.calculate_absolute_average(cube=cube)
        print("Current average:", average)
        time_taken, cube = rubik_module.calculate_time(cube)
        # Record information
        rubik_module.check_new_record(time_taken, cube)
        rubik_module.diff_current_record_time(record=personal_record, time_taken=time_taken)
        # Average information
        rubik_module.diff_current_average_time(cube=cube, time_taken=time_taken)
        rubik_module.average_last_total_solves(cube=cube, num_last_solves=100)
        rubik_module.average_last_total_solves(cube=cube, num_last_solves=50)
        rubik_module.average_last_total_solves(cube=cube, num_last_solves=12)
        rubik_module.average_last_total_solves(cube=cube, num_last_solves=5)
        # Save solve and prompt
        rubik_module.save_data(time_taken, cube)
        retry = input("\nDo you want to try again? (type 'yes' or 'no' and press enter): ")
        print()


if __name__ == "__main__":
    main_function()
