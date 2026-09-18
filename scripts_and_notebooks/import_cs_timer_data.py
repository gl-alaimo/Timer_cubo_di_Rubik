"""Import CS Timer solve data"""

from argparse import ArgumentParser
from pandas import read_csv


def convert_minutes(time_str: str) -> float:
    """Convert a time in minutes:seconds into seconds.

    Params:
        time_str (str): Time as "M:S" or as seconds.

    Returns:
        float: Time in seconds.
    """
    if ":" in time_str:
        minutes_and_seconds = time_str.split(":")
        minutes_in_seconds = int(minutes_and_seconds[0]) * 60
        total_seconds = minutes_in_seconds + float(minutes_and_seconds[1])
        return total_seconds
    else:
        return float(time_str)


# Argument parsing
parser = ArgumentParser()
parser.add_argument("-c", "--cube", dest="cube", help="type of cube", type=str, required=True)
parser.add_argument("-f", "--file", dest="input_file",
                    help="CSV filename exported from CS Timer", type=str, required=True)
args = parser.parse_args()
cube = args.cube
input_file = args.input_file

# Import data
print("Importing CS Timer data from", input_file, "for cube", cube)
df = read_csv(filepath_or_buffer=input_file, sep=";", parse_dates=["Date"])
df = df[["Date", "Time"]]
df["Date"] = df["Date"].dt.date.astype(str)
df["Time"] = df["Time"].apply(convert_minutes)


# Save data to the database
with open("../database.csv", mode="a", encoding="utf-8") as database_file:
    for index, row in df.iterrows():
        database_file.write(f'{row["Date"]}\t{row["Time"]}\t{cube}\n')

print("Data imported and appended to database.")
