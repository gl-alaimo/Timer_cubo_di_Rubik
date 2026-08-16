"""Module containing code that is used in various scripts and notebooks."""

from datetime import datetime
from time import time
from random import choice, shuffle
from colorama import Fore, Style
import seaborn as sns
import pandas
from matplotlib import pyplot as plt
from pyfiglet import Figlet


small_cube_types = ["2x2x2", "3x3x3",  "mirror"]
dodecahedrons = ["kilominx", "megaminx"]
pyraminx_moves = [["U", "U'"], ["L", "L'"], ["R", "R'"], ["F", "F'"]]
dodecahedron_moves = [["U", "U'", "U2"], ["L", "L'", "L2"], ["R", "R'", "R2"],
                      ["F", "F'", "F2"], ["B", "B'", "B2"], ["BL", "BL'", "BL2"],
                      ["BR", "BR'", "BR2"], ["W", "W'", "W2"], ["E", "E'", "E2"]]
small_cubes_moves = [["U", "U'", "U2"], ["D", "D'", "D2"],
                     ["L", "L'", "L2"], ["R", "R'", "R2"],
                     ["B", "B'", "B2"], ["F", "F'", "F2"]]
large_cubes_moves = [["U", "U'", "u", "u'", "U2", "u2", "Uu2"],
                     ["D", "D'", "d", "d'", "D2", "d2", "Dd2"],
                     ["L", "L'", "l", "l'", "L2", "l2", "Ll2"],
                     ["R", "R'", "r", "r'", "R2", "r2", "Rr2"],
                     ["B", "B'", "b", "b'", "B2", "b2", "Bb2"],
                     ["F", "F'", "f", "f'", "F2", "f2", "Ff2"],
                     ["M", "M'", "m", "m'", "M2", "m2", "Mm2"],
                     ["S", "S'", "s", "s'", "S2", "s2", "Ss2"],
                     ["E", "E'", "e", "e'", "E2", "e2", "Ee2"]]
YELLOW = "#ffbf57"
RED = "#d21518"
GREEN = "#73b06a"
BLUE = "#0caaf6"
PURPLE = "#7366cb"
GRAY = "#838d99"
TURQUOISE = "#479fa6"

# Functions for scripts


def show_title():
    """Displays the project title in the terminal."""

    title = Figlet(font="speed") # http://www.figlet.org/examples.html
    print(title.renderText("Rubik's Cube Timer"))


def generate_random_moves(moves_list: list):
    """Generates a list of random moves to scramble the cube before solving it.

    Params:
        moves_list (list): List of lists containing all the moves.

    Returns:
        None.
    
    """
    random_moves_list = []

    for _ in range(2):
        random_moves_list_a = []
        random_moves_list_b = []
        random_moves_list_c = []

        for move in moves_list:
            random_moves_list_a.append(choice(move))
            random_moves_list_b.append(choice(move))
            random_moves_list_c.append(choice(move))

        shuffle(random_moves_list_a)
        shuffle(random_moves_list_b)
        shuffle(random_moves_list_c)

        if random_moves_list_a[-1].startswith(random_moves_list_b[0][0]):
            random_moves_list_a.pop()
        if random_moves_list_b[-1].startswith(random_moves_list_c[0][0]):
            random_moves_list_b.pop()

        random_moves_list = random_moves_list + random_moves_list_a +\
        random_moves_list_b + random_moves_list_c

    print("Suggested random moves to scramble the cube:\n", *random_moves_list)
    print()


def convert_seconds(seconds: int) -> tuple:
    """Converts seconds to minutes and seconds.
    
    Params:
        seconds (int): Number of seconds to convert.

    Returns:
        minutes, sec (tuple): Returns a tuple composed of minutes and seconds.
    """
    minutes, sec = divmod(seconds, 60)
    minutes = int(minutes)
    sec = round(number=sec, ndigits=2)
    return minutes, sec


def search_record(cube: str) -> int:
    """Searches for the current record in the database.

    Params:
        cube (str): Cube type.

    Returns:
        record_time (int): Returns the record time.
    """
    df = pandas.read_csv("../database.csv", sep="\t")
    if len(df[df["Cube"] == cube]) != 0:
        solve_record = df[df["Cube"] == cube].min()
        record_time = solve_record["Seconds"]
        return record_time
    else:
        return 0


def check_new_record(time_taken: int, cube: str) -> None:
    """Checks if the record has been beaten.

    Params:
        time_taken (int): Time taken in seconds.
        cube (str): Cube type.

    Returns:
        Prints information about the record.
    """
    my_record = search_record(cube)
    if time_taken < my_record:
        record_min, record_sec = convert_seconds(my_record)
        current_min, current_sec = convert_seconds(time_taken)
        print(Fore.GREEN + "New personal record!")

        if record_min - current_min == 0:
            print(Fore.GREEN + f"This solve took you {abs(round(number=record_sec - current_sec, ndigits=2))} seconds less than your best time")
        elif record_min - current_min == 1:
            print(Fore.GREEN + f"This solve took you 1 minute and {abs(round(number=record_sec - current_sec, ndigits=2))} seconds less than your best time")
        else:
            print(Fore.GREEN + f"This solve took you {record_min - current_min} minutes and {abs(round(number=record_sec - current_sec, ndigits=2))} seconds less than your best time")
        print(Style.RESET_ALL)


def show_current_time(minutes: int, seconds: int) -> None:
    """Displays the current elapsed time.

    Params:
        minutes (int): Minutes elapsed.
        seconds (int): Seconds elapsed.

    Returns:
        None.
    """
    if minutes == 0:
        print(Fore.CYAN + f"Solve time: {seconds} seconds" + Style.RESET_ALL)
    elif minutes == 1:
        print(Fore.CYAN + f"Solve time: 1 minute and {seconds} seconds" + Style.RESET_ALL)
    else:
        print(Fore.CYAN + f"Solve time: {minutes} minutes and {seconds} seconds" + Style.RESET_ALL)


def calculate_time(cube: str) -> tuple:
    """Calculates the elapsed time.

    Params:
        cube (str): Cube type.

    Returns:
        time_taken, cube (tuple): Prints information and returns a tuple
        with the elapsed time and the cube type.
    """
    input("Press enter to start: ")
    print("Timer started!")
    finished = False
    partial_time = 0

    while finished is False:
        start_time = time()
        stop = input("Type 'p' and press enter to pause, or press enter to finish: ")
        if stop == "p":
            end_time = time()
            partial_time = round(number=partial_time + end_time - start_time, ndigits=2)
            minutes, seconds = convert_seconds(partial_time)
            if minutes == 0:
                print(f"Paused... Elapsed time: {seconds} seconds")
            elif minutes == 1:
                print(f"Paused... Elapsed time: 1 minute and {seconds} seconds")
            else:
                print(f"Paused... Elapsed time: {minutes} minutes and {seconds} seconds")
            input("Press enter to resume: ")
            print("Timer resumed!")
        else:
            finished = True

    end_time = time()
    time_taken = round(number=end_time - start_time, ndigits=2) + partial_time
    print("Done!\n")
    minutes, seconds = convert_seconds(time_taken)
    show_current_time(minutes, seconds)

    return time_taken, cube


def save_data(time_taken: int, cube: str) -> None:
    """Saves the solve time to the database.

    Params:
        time_taken (int): Time taken.
        cube (str): Cube type.

    Returns:
        Saves data to a csv file.
    """
    date = datetime.now().date()
    with open(file="../database.csv", mode="a", encoding="utf-8") as db_file:
        db_file.write(f"{date}\t{time_taken}\t{cube}\n")


def calculate_absolute_average(cube: str) -> str:
    """Calculates the average time of all solves.

    Params:
        cube (str): Cube type.

    Returns:
        formatted_average_minutes (str): Formatted average in minutes.
    """
    df = pandas.read_csv("../database.csv", sep="\t")
    if len(df[df["Cube"] == cube]) != 0:
        average_df = df[df["Cube"] == cube]
        average = average_df["Seconds"].mean()
        average = round(number=average, ndigits=2)
        average_in_minutes = convert_seconds(average)
        formatted_average_minutes = (average_in_minutes[0], str(average_in_minutes[1]))
        if formatted_average_minutes[0] == 0:
            formatted_average_minutes = f"{average_in_minutes[1]} seconds"
        elif formatted_average_minutes[0] == 1:
            formatted_average_minutes = f"{formatted_average_minutes[0]} minute and {average_in_minutes[1]} seconds"
        else:
            formatted_average_minutes = f"{formatted_average_minutes[0]} minutes and {average_in_minutes[1]} seconds"
        return formatted_average_minutes
    else:
        return "None"


def diff_current_average_time(cube: str, time_taken: int) -> None:
    """Calculates the difference between the average solve time and the current solve time.

    Params:
        cube (str): Cube type.
        time_taken (int): Time taken.

    Returns:
        Displays information in the terminal.
    """
    df = pandas.read_csv("../database.csv", sep="\t")
    if len(df[df["Cube"] == cube]) != 0:
        average_df = df[df["Cube"] == cube]
        average = average_df["Seconds"].mean()
        average = round(number=average, ndigits=2)
        more_less = ""
        time_difference = abs(round(number=average - time_taken, ndigits=2))
        if time_taken < average:
            more_less = "less"
        elif time_taken > time_difference:
            more_less = "more"
        else:
            print("You did the same as usual")

        if more_less != "":
            minutes, seconds = convert_seconds(time_difference)
            if minutes == 0:
                print(f"This solve took you {seconds} seconds {more_less} than the absolute average")
            elif minutes == 1:
                print(f"This solve took you {minutes} minute and {seconds} seconds {more_less} than the absolute average")
            else:
                print(f"This solve took you {minutes} minutes and {seconds} seconds {more_less} than the absolute average")


def diff_current_record_time(record: int, time_taken: int) -> None:
    """Calculates the time difference between the personal record and the current solve time.
    
    Params:
        record (int): Current record.
        time_taken (int): Time taken.

    Returns:
        Displays information in the terminal.
    """
    if record != 0:
        if time_taken > record:
            time_difference = time_taken - record
            if time_difference >= 60:
                minutes, seconds = convert_seconds(time_difference)
                if minutes == 0:
                    print(f"This solve took you {seconds} seconds more than the record")
                elif minutes == 1:
                    print(f"This solve took you {minutes} minute and {seconds} seconds more than the record")
                else:
                    print(f"This solve took you {minutes} minutes and {seconds} seconds more than the record")
            else:
                print(f"This solve took you {round(number=time_difference, ndigits=2)} seconds more than the record")
        elif time_taken == record:
            print("You tied your record")
        else:
            pass  # Record information in this case will be provided by the check_new_record() function


def average_last_total_solves(cube: str, num_last_solves: int) -> None:
    """Calculates the average of the last 5 solves for a specific cube type.
    
    Params:
        cube (str): Cube type.
        num_last_solves (int): Number of last solves.

    Returns:
        Displays information in the terminal.
    """
    df = pandas.read_csv("../database.csv", sep="\t")
    if len(df[df["Cube"] == cube]) >= num_last_solves:
        last_solves = df[df["Cube"] == cube].tail(num_last_solves)["Seconds"]
        average_solves = round(number=last_solves.mean(), ndigits=2)
        minutes, seconds = convert_seconds(average_solves)
        if minutes == 0:
            print(f"Average of last {num_last_solves} solves: {seconds} seconds")
        elif minutes == 1:
            print(f"Average of last {num_last_solves} solves: {minutes} minute and {seconds} seconds")
        else:
            print(f"Average of last {num_last_solves} solves: {minutes} minutes and {seconds} seconds")


def add_date_columns(df_cube: pandas.DataFrame) -> pandas.DataFrame:
    """Adds 'Year', 'Month', and 'Day' columns to the DataFrame and reorders columns.

    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.

    Returns:
        df_cube (pandas.DataFrame): Updated DataFrame.
    """
    df_cube = df_cube.assign(Year=df_cube["Date"].dt.year)
    df_cube = df_cube.assign(Month=df_cube["Date"].dt.month)
    df_cube = df_cube.assign(Day=df_cube["Date"].dt.day)
    df_cube = df_cube[["Date", "Year", "Month", "Day", "Seconds", "Time", "Cube"]]  # Reordering columns
    df_cube = df_cube.rename(columns={"Date": "Full Date"})  # Renaming Date column
    df_cube["Month"] = df_cube["Month"].replace({1: "January",
                                     2: "February",
                                     3: "March",
                                     4: "April",
                                     5: "May",
                                     6: "June",
                                     7: "July",
                                     8: "August",
                                     9: "September",
                                     10: "October",
                                     11: "November",
                                     12: "December"
                                     })
    return df_cube


def show_record(cube: str) -> str:
    """Displays information about the personal record in the terminal.

    Params:
        cube (str): Cube type.

    Returns:
        personal_record (str): Displays information in the terminal.
    """
    personal_record = search_record(cube)
    if personal_record != 0:
        minutes, seconds = convert_seconds(personal_record)
        if minutes == 0:
            print(f"Fastest solve: {seconds} seconds")
        elif minutes == 1:
            print(f"Fastest solve: {minutes} minute and {seconds} seconds")
        else:
            print(f"Fastest solve: {minutes} minutes and {seconds} seconds")
    else:
        print("No record set at the moment")
    return personal_record


# Functions for notebooks

def monthly_averages_chart(df_cube: pandas.DataFrame, year: int) -> None:
    """Creates a chart with the monthly average time of solves for a specific cube type.
    
    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        year (int): Year for which to calculate monthly averages.
        
    Returns:
        None.
    """
    years = df_cube["Year"].values
    if year in years:
        chart_data = df_cube[df_cube["Year"] == year].groupby(by=["Month"], sort=False)["Seconds"].mean()
        chart = chart_data.plot(kind="bar", figsize=(11, 5), color=BLUE)
        plt.title(label=f"Monthly average solve time in {year}", fontweight="bold")
        plt.ylabel(ylabel="Seconds", fontweight="bold")
        plt.xlabel(xlabel="Month", fontweight="bold")
        plt.xticks(rotation=0)
        for bar in chart.containers:
            chart.bar_label(container=bar, labels=chart_data.values.round(2), label_type='center')
        plt.show()
    else:
        print(f"No solves present for the year {year}.")


def show_monthly_records(df_cube: pandas.DataFrame, year: int):
    """Displays the monthly record times of solves for a specific cube type and year.
    
    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        year (int): Year for which to calculate monthly records.
        
    Returns:
        None.
    """
    years = df_cube["Year"].values
    if year in years:
        df_records = df_cube[df_cube["Year"] == year].groupby(by=["Month"], sort=False)["Seconds"].min()
        df_records = pandas.DataFrame(df_records)
        df_records.insert(loc=1, column="Time", value=df_records["Seconds"].apply(convert_seconds))
        df_records['Time'] = df_records['Time'].apply(lambda x: f"{x[0]}:{x[1]:05.2f}")
        print("Records established each month\n")
        print(df_records)
    else:
        print(f"No solves present for the year {year}.")


def monthly_records_chart(df_cube: pandas.DataFrame, year: int) -> None:
    """Creates a chart with the monthly record times of solves for a specific cube type and year.
    
    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        year (int): Year for which to calculate monthly records.
        
    Returns:
        None.
    """
    years = df_cube["Year"].values
    if year in years:
        chart_data = df_cube[df_cube["Year"] == year].groupby(by=["Month"], sort=False)["Seconds"].min()
        chart = chart_data.plot(kind="bar", figsize=(11, 5), color=GREEN)
        plt.title(label=f"Monthly best solve time in {year}", fontweight="bold")
        plt.ylabel(ylabel="Seconds", fontweight="bold")
        plt.xlabel(xlabel="Month", fontweight="bold")
        plt.xticks(rotation=0)
        for bar in chart.containers:
            chart.bar_label(container=bar, labels=chart_data.values.round(2), label_type='center')
        plt.show()
    else:
        print(f"No solves present for the year {year}.")


def yearly_averages_chart(df_cube: pandas.DataFrame) -> None:
    """Creates a chart with the yearly average time of solves for a specific cube type.
    
    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        
    Returns:
        None.
    """
    chart_data = df_cube.groupby(by=["Year"])["Seconds"].mean()
    chart = chart_data.plot(kind="bar", figsize=(11, 5), color=PURPLE, width=0.3)
    plt.title(label="Yearly average solve time", fontweight="bold")
    plt.ylabel(ylabel="Seconds", fontweight="bold")
    plt.xlabel(xlabel="Year", fontweight="bold")
    plt.xticks(rotation=0)
    for bar in chart.containers:
        chart.bar_label(container=bar, labels=chart_data.values.round(2), label_type='center')
    plt.show()


def print_record_average_maximum(df_cube: pandas.DataFrame, cube: int) -> None:
    """Prints the maximum, average, and minimum time.
    
    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        cube (str): Cube type.
        
    Returns:
        None.
    """
    record = search_record(cube)
    record_min, record_sec = convert_seconds(record)
    average = df_cube["Seconds"].mean().round(2)
    average_min, average_sec = convert_seconds(average)
    maximum_time = df_cube["Seconds"].max().round(2)
    maximum_time_min, maximum_time_sec = convert_seconds(maximum_time)
    print("Minimum, average, and maximum solve time:")
    print(f"- Minimum time {record_min}:{record_sec}\n",
          f"- Average time {average_min}:{average_sec}\n",
          f"- Maximum time {maximum_time_min}:{maximum_time_sec}")


def record_average_maximum_chart(df_cube: pandas.DataFrame) -> None:
    """Creates a bar chart with record, average, and maximum time for a specific cube type.
    
    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        
    Returns:
        None.
    """
    plt.figure(figsize=(11, 5))
    plt.bar(x=["Minimum time", "Average time", "Maximum time"],
            height=[search_record(cube=df_cube["Cube"].iloc[0]),
                    df_cube["Seconds"].mean().round(2),
                    df_cube["Seconds"].max().round(2)],
            color=[GREEN, BLUE, RED],
            width=0.3)
    plt.title("Minimum, average, and maximum time", fontweight="bold")
    plt.ylabel("Seconds", fontweight="bold")
    plt.show()


def monthly_solves_chart(df_cube: pandas.DataFrame, year: int) -> None:
    """Creates a bar chart with the number of monthly solves for a specific cube type.
    
    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        year (int): Year for which to calculate the number of monthly solves.
        
    Returns:
        None.
    """
    years = df_cube["Year"].values
    if year in years:
        chart_data = df_cube[df_cube["Year"] == year]["Full Date"].dt.month.value_counts().sort_index()
        chart = chart_data.plot(kind="bar", figsize=(11, 5), color=GRAY)
        plt.title(f"Monthly solves in {year}", fontweight="bold")
        plt.ylabel("Number of solves", fontweight="bold")
        plt.xlabel("Month", fontweight="bold")
        plt.xticks(rotation=0)
        for bar in chart.containers:
            chart.bar_label(container=bar, labels=chart_data.values, label_type='center')
        plt.show()
    else:
        print(f"No solves present for the year {year}.")


def all_records_chart(df_cube: pandas.DataFrame) -> None:
    """Creates a chart with records for all cube types.
    
    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        
    Returns:
        None.
    """
    chart_data = df_cube.drop(columns=["Date", "Time"]).groupby(by="Cube").min().sort_values(by="Seconds")
    chart = chart_data.plot.bar(figsize=(11, 5), color=GREEN)
    plt.title("Fastest solves by cube type", fontweight="bold")
    plt.ylabel("Seconds", fontweight="bold")
    plt.xlabel("Cubes", fontweight="bold")
    plt.xticks(rotation=0)
    for bar in chart.containers:
        chart.bar_label(container=bar, labels=chart_data.values[0], label_type="edge")
    plt.show()


def show_all_records(df_cube: pandas.DataFrame) -> None:
    """Displays records for all cube types.
    
    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        
    Returns:
        None.
    """
    df_records = df_cube[["Seconds", "Cube"]].groupby(by="Cube").min()
    df_records.insert(loc=1, column="Time", value=df_records["Seconds"].apply(convert_seconds))
    df_records['Time'] = df_records['Time'].apply(lambda x: f"{x[0]}:{x[1]:05.2f}")
    print(df_records.sort_values(by="Seconds"))


def calculate_solves_average(df_cube: pandas.DataFrame) -> None:
    """Calculates the average solve times for all cube types.
    
    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        
    Returns:
        None.
    """
    averages_df = df_cube[["Seconds", "Cube"]].groupby(by="Cube").mean().round(2)
    averages_df.insert(loc=1, column="Time", value=averages_df["Seconds"].apply(convert_seconds))
    averages_df['Time'] = averages_df['Time'].apply(lambda x: f"{x[0]}:{x[1]:05.2f}")
    print(averages_df.sort_values(by="Seconds"))


def solves_average_chart(df_cube: pandas.DataFrame) -> None:
    """Creates a chart with average solve times for all cube types.
    
    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        
    Returns:
        None.
    """
    chart_data = df_cube[["Seconds", "Cube"]].groupby(by="Cube").mean().round(2).sort_values(by="Seconds")
    chart = chart_data.plot.bar(figsize=(11, 5), color=BLUE)
    plt.title("Average solves by cube type", fontweight="bold")
    plt.ylabel("Seconds", fontweight="bold")
    plt.xlabel("Cubes", fontweight="bold")
    plt.xticks(rotation=0)
    for bar in chart.containers:
        chart.bar_label(container=bar, labels=chart_data.values[0].round(2), label_type="edge")
    plt.show()


def calculate_solves_count(df_cube: pandas.DataFrame) -> None:
    """Calculates the number of solves for all cube types.
    
    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        
    Returns:
        None.
    """
    print(df_cube["Cube"].value_counts().sort_values(ascending=False))


def solves_count_chart(df_cube: pandas.DataFrame) -> None:
    """Creates a chart with the number of solves for all cube types.
    
    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        
    Returns:
        None.
    """
    chart_data = df_cube["Cube"].value_counts()
    chart = chart_data.plot(kind="bar", figsize=(11, 5), color=TURQUOISE)
    plt.title("Number of solves by different cubes", fontweight="bold")
    plt.ylabel("Number of solves", fontweight="bold")
    plt.xlabel("Cubes", fontweight="bold")
    plt.xticks(rotation=0)
    for bar in chart.containers:
        chart.bar_label(container=bar, labels=chart_data.values, label_type="center")
    plt.show()


def recent_solves_chart(df_cube: pandas.DataFrame) -> None:
    """Creates a chart with the last 10 solves.
    
    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        
    Returns:
        None.
    """
    plt.figure(figsize=(13, 5))
    plt.title("Times and dates of recent solves", fontweight="bold")
    plt.scatter(df_cube.tail(10)["Full Date"], df_cube.tail(10)["Seconds"])
    plt.grid(axis="y")
    plt.xticks(rotation=0)
    plt.ylabel("Seconds", fontweight="bold")
    plt.xlabel("Date", fontweight="bold")
    plt.show()


def load_data(cube: str) -> pandas.DataFrame:
    """Loads data from the database.

    Params:
        cube (str): Cube type.
    
    Returns:
        df (pandas.DataFrame): DataFrame with loaded data from the database.
    """
    df = pandas.read_csv("../database.csv", sep="\t", parse_dates=["Date"])
    if cube in df["Cube"].values:
        df = df[df["Cube"] == cube]
        df = df.reset_index(drop=True)
        # Insert "Time" column with seconds converted to minutes and seconds
        df.insert(loc=2, column="Time", value=df["Seconds"].apply(convert_seconds))
        df['Time'] = df['Time'].apply(lambda x: f"{x[0]}:{x[1]:05.2f}")
        df = add_date_columns(df)
        return df
    else:
        print("No solves found for this type of cube.")


def load_general_notebook_data() -> pandas.DataFrame:
    """Loads data for all cube types from the database.

    Params:
        None.

    Returns:
        df (pandas.DataFrame): DataFrame with loaded data from the database.
    """
    df = pandas.read_csv("../database.csv", sep="\t", parse_dates=["Date"])
    # Insert "Time" column with seconds converted to minutes and seconds
    df.insert(loc=2, column="Time", value=df["Seconds"].apply(convert_seconds))
    # Formatting time as min:sec,millisec
    df['Time'] = df['Time'].apply(lambda x: f"{x[0]}:{x[1]:05.2f}")
    return df


def print_record(cube: str) -> None:
    """Prints the record for the specified cube.
    
    Params:
        cube (str): Cube type.
    
    Returns:
        None.
    """
    minutes, seconds = convert_seconds((search_record(cube)))
    if minutes == 0:
        print(f"Personal best: {seconds} seconds")
    elif minutes == 1:
        print(f"Personal best:s {minutes} minute and {seconds} seconds")
    else:
        print(f"Personal best: {minutes} minutes and {seconds} seconds")


def monthly_solves_averages(df_cube: pandas.DataFrame, year: int) -> pandas.Series:
    """Prints the monthly average solve times for the specified cube and year.
    
    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        year (int): Year for which to calculate monthly averages.
    
    Returns:
        None.
    """
    years = df_cube["Year"].values
    if year in years:
        df_monthly_averages = df_cube[df_cube["Year"] == year].groupby(by=["Month"], sort=False)["Seconds"].mean().round(2)
        df_monthly_averages = pandas.DataFrame(df_monthly_averages)
        df_monthly_averages.insert(loc=1, column="Time", value=df_monthly_averages["Seconds"].apply(convert_seconds))
        df_monthly_averages['Time'] = df_monthly_averages['Time'].apply(lambda x: f"{x[0]}:{x[1]:05.2f}")
        print("Monthly average solve times\n")
        print(df_monthly_averages)
    else:
        print(f"No solves present for the year {year}.")


def monthly_solves_count(df_cube: pandas.DataFrame, year: int) -> pandas.Series:
    """Displays the number of monthly solves for the specified year.

    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        year (int): Year.
    
    Returns:
        None.
    """
    years = df_cube["Year"].values
    if year in years:
        print(f"Number of monthly solves in {year}\n")
        print(df_cube[df_cube["Year"] == year]["Month"].value_counts())
    else:
        print(f"No solves present for the year {year}.")


def yearly_solves_averages(df_cube: pandas.DataFrame):
    """Prints the yearly average solve times.
    
    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
    
    Returns:
        None.
    """
    df_yearly_averages = df_cube.groupby(by=["Year"])["Seconds"].mean().round(2)
    df_yearly_averages = pandas.DataFrame(df_yearly_averages)
    df_yearly_averages.insert(loc=1, column="Time", value=df_yearly_averages["Seconds"].apply(convert_seconds))
    df_yearly_averages['Time'] = df_yearly_averages['Time'].apply(lambda x: f"{x[0]}:{x[1]:05.2f}")
    print("Monthly average times in seconds of yearly solves\n")
    print(df_yearly_averages)


def last_total_solves_chart(df_cube: pandas.DataFrame, num_last_solves: int = 50) -> None:
    """Creates a chart with times and average of the last N solves.

    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        num_last_solves (int): Number of last solves. 
        If not specified, its default value is 50.

    Returns:
        None.
    """
    df_cube = df_cube.tail(num_last_solves)
    average = df_cube["Seconds"].mean().round(2)

    plt.figure(figsize=(13, 5))
    plt.title(f"Times of last {num_last_solves} solves", fontweight="bold")
    plt.scatter(df_cube.index, df_cube["Seconds"])
    plt.plot(df_cube.index, df_cube["Seconds"])
    plt.axhline(y=average, color="purple", label="Average")
    plt.grid(axis="y")
    plt.xticks(rotation=0)
    plt.ylabel("Seconds", fontweight="bold")
    plt.xlabel("Solve number", fontweight="bold")
    plt.legend()
    plt.show()

    minutes, seconds = convert_seconds(average)
    print(f"Average time: {minutes}:{seconds}")


def top_solves_ranking(df_cube: pandas.DataFrame) -> None:
    """Displays information about the times of the top 10 solves.

    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.

    Returns:
        None.
    """
    print("Ranking of the 10 fastest solves\n")
    df_top_10 = df_cube.sort_values(by="Seconds", ascending=True).head(10).reset_index(drop=True)
    df_top_10.insert(loc=6, column="Time Difference", value=pandas.DataFrame.diff(df_top_10["Seconds"]))
    df_top_10["Time Difference"] = df_top_10["Time Difference"].fillna(value=0)
    df_top_10.drop(columns=["Cube"], inplace=True)
    print(df_top_10)


def yearly_solves_count(df_cube: pandas.DataFrame) -> pandas.Series:
    """Displays the number of yearly solves for the specified year.

    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
    
    Returns:
        None.
    """
    print("Number of yearly solves\n")
    print(df_cube["Year"].value_counts().sort_values())


def yearly_solves_chart(df_cube: pandas.DataFrame) -> None:
    """Creates a bar chart with the number of yearly solves for a specific cube type.
    
    Params:
        df_cube (pandas.DataFrame): DataFrame containing solve data.
        
    Returns:
        None.
    """
    chart_data = df_cube["Year"].value_counts().sort_index()
    chart = chart_data.plot(kind="bar", figsize=(11, 5), width=0.3, color=YELLOW)
    plt.title("Number of yearly solves", fontweight="bold")
    plt.ylabel("Number of solves", fontweight="bold")
    plt.xlabel("Year", fontweight="bold")
    plt.xticks(rotation=0)
    for bar in chart.containers:
        chart.bar_label(container=bar, labels=chart_data.values, label_type='center')
    plt.show()


def all_solves_chart(df: pandas.DataFrame) -> None:
    """Creates a chart with data of all solves for all cube types.

    Params:
        df (pandas.DataFrame): DataFrame containing solve data.
        
    Returns:
        None.
    """
    plt.figure(figsize=(13, 5))

    for cube in df["Cube"].unique():
        plt.scatter(df[df["Cube"] == cube].index,
                    df[df["Cube"] == cube]["Seconds"],
                    label=cube)

    plt.title("Solve times for all cube types", fontweight="bold")
    plt.grid(axis="y")
    plt.ylabel("Seconds", fontweight="bold")
    plt.xlabel("Solve number", fontweight="bold")
    plt.legend()
    plt.show()


def data_concentration_chart(df: pandas.DataFrame) -> None:
    """Creates a chart with data concentration of all solves.

    Params:
        df (pandas.DataFrame): DataFrame containing solve data.
        
    Returns:
        None.
    """
    plt.figure(figsize=(11, 5))
    plt.title("Data concentration of all solves")
    sns.scatterplot(data=df, x=df.index, y="Seconds", color="#8a6a5a")
    sns.rugplot(data=df,
                x=df.index,
                y="Seconds",
                color="#3e302c")
    plt.xlabel("Solve number")
    plt.show()


def calculate_correlation(df: pandas.DataFrame) -> float:
    """Calculates the correlation coefficient.

    Params:
        df (pandas.DataFrame): DataFrame containing solve data.
        
    Returns:
        coefficient (float): Correlation coefficient.
    """
    indices = pandas.Series(df.index.to_list())
    correlation_coefficient = df["Seconds"].corr(indices)
    print("Correlation coefficient", correlation_coefficient)
    if correlation_coefficient < 0 and correlation_coefficient > -1:
        print("This value indicates that the more solves you do, the shorter the solve time becomes")
    elif correlation_coefficient == -1:
        print("This value indicates that every single time you solve the cube, the solve time decreases")
    elif correlation_coefficient > 0 and correlation_coefficient < 1:
        print("This value indicates that the more solves you do, the longer the solve time becomes")
    elif correlation_coefficient == 1:
        print("This value indicates that every single time you solve the cube, the solve time increases")

