"""Importa i dati delle risoluzioni di CS Timer"""

from argparse import ArgumentParser
from pandas import read_csv

# Gestione argomenti
parser = ArgumentParser()
parser.add_argument("-c", "--cubo", help="tipo di cubo", type=str, required=True)
parser.add_argument("-f", "--file", help="nome del file CSV con i dati esportati da CS Timer",
                    type=str, required=True)
args = parser.parse_args()
cubo = args.cubo
file = args.file

# Importazione dei dati
print("Importazione dei dati di CS Timer dal file", file, "per il cubo", cubo)
df = read_csv(filepath_or_buffer=file, sep=";", parse_dates=["Date"])
df = df[["Date", "Time"]]
df["Date"] = df["Date"].dt.date.astype(str)

# Salvataggio dei dati nel database
with open("../database.csv", mode="a", encoding="utf-8") as database_file:
    for the_index, the_data in df.iterrows():
        database_file.write(f"{the_data['Date']}\t{the_data["Time"]}\t{cubo}\n")

print("Dati importati ed aggiunti al database.")
