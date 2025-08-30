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
        print(f"Hai battuto il tuo record di {record_min-current_min} minuti e {(record_sec-current_sec).__round__(2)} secondi!!!\n"
              f"Record precedente {record_min} minuti e {record_sec} secondi")


def calcolo_tempo(cubo:str):
    """Calculate solving time"""
    input("Premi invio per iniziare ")
    finito = False
    tempo_parziale = 0

    while finito == False:
        ora_iniziale = time.time()
        stop = input("Premi 'p' e invio se vuoi mettere in pausa o solo invio per terminare: ")
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
    print("Fine!")
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
    """Calcolo diff tempo in media e tempo attuale"""
    df = pd.read_csv("database.csv", sep="\t")
    media_df = df[df["Cubo"] == cubo]
    media = media_df["Secondi"].mean()
    if tempo_impiegato < media:
        print(f"Ci hai impiegato {(media-tempo_impiegato).__round__(2)} secondi in meno del solito")
    elif tempo_impiegato > media:
        print(f"Ci hai impiegato {(tempo_impiegato-media).__round__(2)} secondi in piu del solito")
    else:
        print("Ci hai impiegato come al solito")

def main_function():
    titolo = Figlet(font="speed") # http://www.figlet.org/examples.html
    print(titolo.renderText("Rubik Timer"))
    
    small_cube_moves = ['U', 'D', 'R', 'L', 'F', 'B', 'U1°', 'D1°', 'R1°', 'L1°', 'F1°', 'B1°', 'U2', 'D2', 'R2', 'L2', 'F2', 'B2']
    big_cube_moves = ["u", "d", "r", "l", "f", "b", "u1°", "d1°", "r1°", "l1°", "f1°", "b1°", "u2", "d2", "r2", "l2", "f2", "b2", "Uu2", "Dd2", "Rr2", "Ll2", "Ff2", "Bb2", "U2", "D2", "R2", "L2", "F2", "B2", "U1°", "D1°", "R1°", "L1°", "F1°", "B1°"]

    cubo = input("Digita il tipo di cubo: ")
    if cubo == "4x4" or cubo == "5x5":
        mescolamento_random_4x4_5x5 = [random.choice(big_cube_moves) for m in range(20)]
        print("Movimenti casuali suggeriti per mischiare il cubo:\n",mescolamento_random_4x4_5x5)
    else:
        mescolamento_random_2x2_3x3 = [random.choice(small_cube_moves) for i in range(20)]
        print("Movimenti casuali suggeriti per mischiare il cubo:\n",mescolamento_random_2x2_3x3)

    my_record = get_record(cubo)
    min, sec = convert_seconds(my_record)
    print(f"Record da battere {min} minuti e {sec} secondi")

    tempo_impiegato, cubo = calcolo_tempo(cubo)
    is_new_record(tempo_impiegato, cubo)
    diffs_media_tempo_attuale(cubo=cubo, tempo_impiegato=tempo_impiegato)
    salvataggio_dati(tempo_impiegato, cubo)

if __name__ == "__main__": 
    main_function()
