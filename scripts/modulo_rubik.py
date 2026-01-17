"""Modulo Rubik timer"""

from datetime import datetime
from time import time
from pandas import read_csv


def conversione_secondi(secondi:int):
    """Converte i secondi in minuti e secondi"""
    minuti, secondi = divmod(secondi, 60)
    minuti = int(minuti)
    secondi = round(secondi, 2)
    return minuti, secondi


def ricerca_record(cubo:str):
    """Ricerca il record attuale nel database"""
    df = read_csv("../database.csv", sep="\t")
    record_risoluzione = df[df["Cubo"] == cubo].min()
    tempo_record = record_risoluzione["Secondi"]
    return tempo_record


def controllo_nuovo_record(tempo_impiegato:int, cubo:str):
    """Controlla se il record è stato battuto."""
    mio_record = ricerca_record(cubo)
    if tempo_impiegato < mio_record:
        record_min, record_sec = conversione_secondi(mio_record)
        minuti_attuali, secondi_attuali = conversione_secondi(tempo_impiegato)
        print(f"Hai battuto il tuo record di {record_min-minuti_attuali} minuti e {abs((record_sec-secondi_attuali).__round__(2))} secondi!!!\n"
              f"Record precedente {record_min} minuti e {record_sec} secondi")


def calcolo_tempo(cubo:str):
    """Calcola il tempo impiegato."""
    input("Premi invio per iniziare ")
    finito = False
    tempo_parziale = 0

    while finito is False:
        ora_iniziale = time()
        stop = input("Premi 'p' ed invio se vuoi mettere in pausa o invio per terminare: ")
        if stop == "p":
            ora_finale = time()
            tempo_parziale = (tempo_parziale + ora_finale - ora_iniziale).__round__(2)
            min, sec = conversione_secondi(tempo_parziale)
            if min == 1:
                print(f"In pausa... Tempo impiegato fino ad ora: {min} minuto e {sec} secondi")
            else:
                print(f"In pausa... Tempo impiegato fino ad ora: {min} minuti e {sec} secondi")
            input("Premi invio per continuare")
        else:
            finito = True

    ora_finale = time()
    tempo_impiegato = (ora_finale - ora_iniziale).__round__(2) + tempo_parziale
    print("Fine!\n")
    min, sec = conversione_secondi(tempo_impiegato)
    if min == 1:
        print(f"Tempo impiegato: {min} minuto e {sec} secondi")
    else:
        print(f"Tempo impiegato: {min} minuti e {sec} secondi")
    return tempo_impiegato, cubo


def salvataggio_dati(tempo, cubo):
    """Salva il tempo di risoluzione nel database"""
    data = datetime.now().date()
    with open(file="../database.csv", mode="a", encoding="utf-8") as db_file:
        db_file.write(f"{data}\t{tempo}\t{cubo}\n")


def diffs_media_tempo_attuale(cubo:str, tempo_impiegato:int):
    """Calcola la diffeerenza del tempo medio di risoluzione e il tempo di risoluzione attuale"""
    df = read_csv("../database.csv", sep="\t")
    media_df = df[df["Cubo"] == cubo]
    media = media_df["Secondi"].mean()
    media = media.__round__(2)
    media_in_minuti = conversione_secondi(media)
    media_in_minuti_formattata = (media_in_minuti[0], str(media_in_minuti[1]))
    media_in_minuti_formattata = f"{media_in_minuti[0]} minuti e {media_in_minuti[1]} secondi"

    print("La tua media attuale è di", media, "secondi, ovvero", media_in_minuti_formattata)
    if tempo_impiegato < media:
        print(f"Ci hai impiegato {(media-tempo_impiegato).__round__(2)} secondi in meno del solito")
    elif tempo_impiegato > media:
        print(f"Ci hai impiegato {(tempo_impiegato-media).__round__(2)} secondi in piu del solito")
    else:
        print("Ci hai impiegato come al solito")


def diff_record_tempo_attuale(record:int, tempo_impiegato:int):
    """Calcola la differenza di tempo tra il record personale e il tempo di risoluzione attuale"""
    if tempo_impiegato > record:
        print("Ci hai impiegato", (tempo_impiegato-record).__round__(2), "secondi in più rispetto al record")
    elif tempo_impiegato == record:
        print("Hai eguaglito il tuo record")
    else:
        pass # Informazioni sul record in questo caso verrano date dalla funzione controllo_nuovo_record()


def media_ultime_5(cubo):
    """Calcola la media delle ultime 5 risoluzioni di un certo tipo di cubo"""
    df = read_csv("../database.csv", sep="\t")
    ultime_5 = df[df["Cubo"] == cubo].tail(5)["Secondi"]
    media_soluzioni, tempi_totali = 0, 0
    for tempo in ultime_5:
        tempi_totali = tempi_totali + tempo
    media_soluzioni = tempi_totali / 5
    media_in_minuti = conversione_secondi(media_soluzioni)
    print("Media delle ultime 5 risoluzioni di questo cubo:", media_in_minuti)

