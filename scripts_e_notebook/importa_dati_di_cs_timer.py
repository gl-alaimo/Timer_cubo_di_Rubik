"""Importa i dati delle risoluzioni di CS Timer"""

from argparse import ArgumentParser
from pandas import read_csv


def conversione_minuti(tempo: str) -> str:
    """Converte il tempo in minuti e secondi in secondi.

    Params:
        tempo (str): Numero di minuti.

    Returns:
        secondi (float): Restituisce i secondi.
    """
    if ":" in tempo:
        minuti_e_secondi = tempo.split(":")
        minuti_in_secondi = int(minuti_e_secondi[0]) * 60
        tempo_in_minuti_e_secondi = minuti_in_secondi + float(minuti_e_secondi[1])
        return tempo_in_minuti_e_secondi
    else:
        return tempo


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
df["Time"] = df["Time"].apply(conversione_minuti)


# Salvataggio dei dati nel database
with open("../database.csv", mode="a", encoding="utf-8") as database_file:
    for indice, valore in df.iterrows():
        database_file.write(f"{valore['Date']}\t{valore["Time"]}\t{cubo}\n")

print("Dati importati ed aggiunti al database.")
