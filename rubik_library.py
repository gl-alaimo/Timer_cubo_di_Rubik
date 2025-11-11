""" Rubik timer library"""

from datetime import datetime
import pandas as pd
import random
import time
from pyfiglet import Figlet


def convert_seconds(seconds:int):
    """Conversione dei secondi in minuti e secondi"""
    minutes, seconds = divmod(seconds, 60)
    minutes = int(minutes)
    seconds = round(seconds, 2)
    return minutes, seconds


def get_record(cubo:str):
    """Get current record from dataframe"""
    df = pd.read_csv("database.csv", sep="\t")
    record_solves = df[df["Cubo"] == cubo].min()
    record_time = record_solves["Secondi"]
    return record_time


def is_new_record(tempo_impiegato:int, cubo:str):
    """Check if record has been beaten"""
    my_record = get_record(cubo)
    if tempo_impiegato < my_record:
        record_min, record_sec = convert_seconds(my_record)
        current_min, current_sec = convert_seconds(tempo_impiegato)
        print(f"Hai battuto il tuo record di {record_min-current_min} minuti e {abs((record_sec-current_sec).__round__(2))} secondi!!!\n"
              f"Record precedente {record_min} minuti e {record_sec} secondi")


def calcolo_tempo(cubo:str):
    """Calculate solving time"""
    input("Premi invio per iniziare ")
    finito = False
    tempo_parziale = 0

    while finito == False:
        ora_iniziale = time.time()
        stop = input("Premi 'p' ed invio se vuoi mettere in pausa o invio per terminare: ")
        if stop == "p":
            ora_finale = time.time()
            tempo_parziale = (tempo_parziale + ora_finale - ora_iniziale).__round__(2)
            min, sec = convert_seconds(tempo_parziale)
            if min == 1:
                print(f"In pausa... Tempo impiegato fino ad ora: {min} minuto e {sec} secondi")
            else:
                print(f"In pausa... Tempo impiegato fino ad ora: {min} minuti e {sec} secondi")
            input("Premi invio per continuare")
        else:
            finito = True

    ora_finale = time.time()
    tempo_impiegato = (ora_finale - ora_iniziale).__round__(2) + tempo_parziale
    print("Fine!\n")
    min, sec = convert_seconds(tempo_impiegato)
    if min == 1:
        print(f"Tempo impiegato: {min} minuto e {sec} secondi")
    else:
        print(f"Tempo impiegato: {min} minuti e {sec} secondi")
    return tempo_impiegato, cubo


def salvataggio_dati(tempo, cubo):
    """Save time into the database"""
    data = datetime.now().date()
    with open(file="database.csv", mode="a") as db_file:
        db_file.write(f"{data}\t{tempo}\t{cubo}\n")


def diffs_media_tempo_attuale(cubo:str, tempo_impiegato:int):
    """Calcolo diff tempo soluzione media e tempo soluzione attuale"""
    df = pd.read_csv("database.csv", sep="\t")
    media_df = df[df["Cubo"] == cubo]
    media = media_df["Secondi"].mean()
    print("La tua media attuale è di", media.__round__(2), "secondi")
    if tempo_impiegato < media:
        print(f"Ci hai impiegato {(media-tempo_impiegato).__round__(2)} secondi in meno del solito")
    elif tempo_impiegato > media:
        print(f"Ci hai impiegato {(tempo_impiegato-media).__round__(2)} secondi in piu del solito")
    else:
        print("Ci hai impiegato come al solito")


def diffs_record_tempo_attuale(record:int, tempo_impiegato:int):
    """Calcolo diff tempo record personale e tempo soluzione attuale"""
    if tempo_impiegato > record:
        print(f"Ci hai impiegato", (tempo_impiegato-record).__round__(2), "secondi in più rispetto al record")
    elif tempo_impiegato == record:
        print("Hai eguaglito il tuo record")
    else:
        pass # Informazioni sul record in questo caso verrano date dalla funzione is_new_record()

