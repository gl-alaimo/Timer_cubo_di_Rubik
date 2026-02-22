"""Modulo Rubik timer"""

from datetime import datetime
from time import time
import pandas
from matplotlib import pyplot as plt


# Funzioni per gli script

def conversione_secondi(secondi: int) -> tuple:
    """Converte i secondi in minuti e secondi

        Parametri:
            secondi (int): Numero di secondi da convertire
        Returns:
            minuti, sec (tuple): Restituisce una tuple composta da minuti e secondi
    """
    minuti, sec = divmod(secondi, 60)
    minuti = int(minuti)
    sec = round(number=sec, ndigits=2)
    return minuti, sec


def ricerca_record(cubo:str) -> int:
    """Ricerca il record attuale nel database

        Parametri:
            cubo (str): Tipo di cubo
        Returns:
            tempo_record (int): Restituisce il tempo record
    """
    df = pandas.read_csv("../database.csv", sep="\t")
    if len(df[df["Cubo"] == cubo]) != 0:
        record_risoluzione = df[df["Cubo"] == cubo].min()
        tempo_record = record_risoluzione["Secondi"]
        return tempo_record
    else:
        return 0


def controllo_nuovo_record(tempo_impiegato:int, cubo:str) -> None:
    """Controlla se il record è stato battuto.

        Parametri:
            tempo_impiegato (int): Tempo impiegato in secondi
            cubo (str): Tipo di cubo
        Returns:
            Stampa informazioni sul record
    """
    mio_record = ricerca_record(cubo)
    if tempo_impiegato < mio_record:
        record_min, record_sec = conversione_secondi(mio_record)
        minuti_attuali, secondi_attuali = conversione_secondi(tempo_impiegato)
        print(f"Hai battuto il tuo record di {record_min-minuti_attuali} minuti e {abs(round(number=record_sec-secondi_attuali, ndigits=2))} secondi!!!\n"
              f"Record precedente {record_min} minuti e {record_sec} secondi")


def calcolo_tempo(cubo:str) -> tuple:
    """Calcola il tempo impiegato.

    Parametri:
            cubo (str): Tipo di cubo
        Returns:
            tempo_impiegato, cubo (tuple): Stampa informazioni e restiruisce una tuple con il tempo impiegato e il tipo di cubo
    """
    input("Premi invio per iniziare ")
    finito = False
    tempo_parziale = 0

    while finito is False:
        ora_iniziale = time()
        stop = input("Premi 'p' ed invio se vuoi mettere in pausa o invio per terminare: ")
        if stop == "p":
            ora_finale = time()
            tempo_parziale = round(number=tempo_parziale + ora_finale - ora_iniziale, ndigits=2)
            min, sec = conversione_secondi(tempo_parziale)
            if min == 1:
                print(f"In pausa... Tempo impiegato fino ad ora: {min} minuto e {sec} secondi")
            else:
                print(f"In pausa... Tempo impiegato fino ad ora: {min} minuti e {sec} secondi")
            input("Premi invio per continuare")
        else:
            finito = True

    ora_finale = time()
    tempo_impiegato = round(number=ora_finale - ora_iniziale, ndigits=2) + tempo_parziale
    print("Fine!\n")
    min, sec = conversione_secondi(tempo_impiegato)
    if min == 1:
        print(f"Tempo impiegato: {min} minuto e {sec} secondi")
    else:
        print(f"Tempo impiegato: {min} minuti e {sec} secondi")
    return tempo_impiegato, cubo


def salvataggio_dati(tempo:int, cubo:str) -> None:
    """Salva il tempo di risoluzione nel database

        Parametri:
            tempo (int): Tempo impiegato
            cubo (str): Tipo di cubo
        Returns:
            Salva i dati in un file csv
    """
    data = datetime.now().date()
    with open(file="../database.csv", mode="a", encoding="utf-8") as db_file:
        db_file.write(f"{data}\t{tempo}\t{cubo}\n")


def diffs_media_tempo_attuale(cubo:str, tempo_impiegato:int) -> None:
    """Calcola la diffeerenza del tempo medio di risoluzione e il tempo di risoluzione attuale

        Parametri:
            cubo (str): Tipo di cubo
            tempo_impiegato (int): Tempo impiegato
        Returns:
            Stampa informazioni sul terminale
    """
    df = pandas.read_csv("../database.csv", sep="\t")
    if len(df[df["Cubo"] == cubo]) != 0:
        media_df = df[df["Cubo"] == cubo]
        media = media_df["Secondi"].mean()
        media = round(number=media, ndigits=2)
        media_in_minuti = conversione_secondi(media)
        media_in_minuti_formattata = (media_in_minuti[0], str(media_in_minuti[1]))
        media_in_minuti_formattata = f"{media_in_minuti[0]} minuti e {media_in_minuti[1]} secondi"

        print("La tua media attuale è di", media_in_minuti_formattata)
        if tempo_impiegato < media:
            print(f"Ci hai impiegato {round(number=media-tempo_impiegato, ndigits=2)} secondi in meno del solito")
        elif tempo_impiegato > media:
            print(f"Ci hai impiegato {round(number=tempo_impiegato-media, ndigits=2)} secondi in piu del solito")
        else:
            print("Ci hai impiegato come al solito")


def diff_record_tempo_attuale(record:int, tempo_impiegato:int) -> None:
    """Calcola la differenza di tempo tra il record personale e il tempo di risoluzione attuale

        Parametri:
            record (int): Record attuale
            tempo_impiegato (int): Tempo impiegato
        Returns:
            Stampa informazioni sul terminale
    """
    if record != 0:
        if tempo_impiegato > record:
            print("Ci hai impiegato", round(number=tempo_impiegato-record, ndigits=2), "secondi in più rispetto al record")
        elif tempo_impiegato == record:
            print("Hai eguaglito il tuo record")
        else:
            pass # Informazioni sul record in questo caso verrano date dalla funzione controllo_nuovo_record()


def media_ultime_5(cubo:str) -> None:
    """Calcola la media delle ultime 5 risoluzioni per un determinato tipo di cubo
    
        Parametri:
            cubo (str): Tipo di cubo
        Returns:
            Stampa informazioni sul terminale
    """
    df = pandas.read_csv("../database.csv", sep="\t")
    if len(df[df["Cubo"] == cubo]) >= 5:
        ultime_5 = df[df["Cubo"] == cubo].tail(5)["Secondi"]
        media_soluzioni, tempi_totali = 0, 0
        for tempo in ultime_5:
            tempi_totali = tempi_totali + tempo
        media_soluzioni = tempi_totali / 5
        media_in_minuti = conversione_secondi(media_soluzioni)
        print(f"Media delle ultime 5 risoluzioni di questo cubo: {media_in_minuti[0]} minuti e { media_in_minuti[1]} secondi")


def aggiunta_colonne_data(df:pandas.DataFrame) -> pandas.DataFrame:
    """Aggiunge colonne anno mese e giorno e riordina le colonne"""
    df = df.assign(Anno=df["Data"].dt.year)
    df = df.assign(Mese=df["Data"].dt.month)
    df = df.assign(Giorno=df["Data"].dt.day)
    df = df[["Data", "Anno", "Mese", "Giorno", "Secondi", "Tempo", "Cubo"]] # Riordinamento colonne
    df = df.rename(columns={"Data":"Data completa"}) # Cambio nome colonna Data
    df["Mese"] = df["Mese"].replace({1:"Gen",
                                    2:"Feb",
                                    3:"Mar",
                                    4:"Apr",
                                    5:"Mag",
                                    6:"Giu",
                                    7:"Lug",
                                    8:"Ago",
                                    9:"Set",
                                    10:"Ott",
                                    11:"Nov",
                                    12:"Dic"
                                    })
    return df

# Funzioni per i notebook

def grafico_medie_mensili(df_cubo: pandas.DataFrame, anno: int) -> None:
    """Crea un grafico con il tempo medio mensile delle soluzioni per un determinato tipo di cubo.
    
    Parametri:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        anno (int): Anno per cui calcolare le medie mensili.
        
    Returns:
        None
    """
    df_cubo[df_cubo["Anno"]==anno].groupby(by=["Mese"],
                                           sort=False)["Secondi"].mean().plot(kind="bar")
    plt.title(label=f"Tempo medio mensile risoluzioni cubo nel {anno}")
    plt.ylabel(ylabel="Secondi")
    plt.xlabel(xlabel="Mese")
    plt.xticks(rotation=0)
    plt.show()


def grafico_medie_annuali(df_cubo: pandas.DataFrame) -> None:
    """Crea un grafico con il tempo medio annuale delle soluzioni per un determinato tipo di cubo.
    
    Parametri:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    df_cubo.groupby(by=["Anno"])["Secondi"].mean().plot(kind="bar")
    plt.title(label="Tempo medio annuale risoluzioni cubo")
    plt.ylabel(ylabel="Secondi")
    plt.xlabel(xlabel="Anno")
    plt.xticks(rotation=0)
    plt.show()


def grafico_record_media_massimo(df_cubo: pandas.DataFrame) -> None:
    """Crea un grafico a barre con tempo record, media e tempo massimo per un determinato tipo di cubo.
    
    Parametri:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    plt.figure(figsize=(4,4))
    plt.bar(x=["Record", "Media", "Tempo massimo"],
            height=[ricerca_record(cubo="3x3x3"),
                    df_cubo["Secondi"].mean().round(2),
                    df_cubo["Secondi"].max().round(2)],
            color=["green", "blue", "red"])
    plt.title("Record media e tempo massimo")
    plt.ylabel("Secondi")
    plt.show()


def grafico_risoluz_mensile(df_cubo: pandas.DataFrame, anno: int) -> None:
    """Crea un grafico a barre con il numero di risoluzioni mensili per un determinato tipo di cubo.
    
    Parametri:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        anno (int): Anno per cui calcolare il numero di risoluzioni mensili.
        
    Returns:
        None
    """
    df_cubo[df_cubo["Anno"]==anno]["Data completa"].dt.month.value_counts().sort_index().plot(kind="bar")
    plt.title(f"Numero risoluzioni del {anno} in base al mese")
    plt.ylabel("Num risoluzioni")
    plt.xlabel("Mese")
    plt.xticks(rotation=0)
    plt.show()


def grafico_tutti_record(df: pandas.DataFrame) -> None:
    """Crea un grafico con i record per tutti i tipi di cubo.
    
    Parametri:
        df (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    df.drop(columns=["Data", "Tempo"]).groupby(by="Cubo").min().sort_values(by="Secondi").plot.bar()
    plt.title("Soluzioni piu veloci per tipo di cubo")
    plt.ylabel("Secondi")
    plt.xlabel("Cubi")
    plt.xticks(rotation=0)
    plt.show()


def mostra_record(df: pandas.DataFrame) -> None:
    """Mostra i record per tutti i tipi di cubo.
    
    Parametri:
        df (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    print(df.groupby(by="Cubo").min().sort_values(by="Secondi").drop(columns=["Data", "Secondi"]))


def calcola_media_risoluzioni(df: pandas.DataFrame) -> None:
    """Calcola la media dei tempi di risoluzione per tutti i tipi di cubo.
    
    Parametri:
        df (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    medie_df = df.groupby(by="Cubo")["Secondi"].mean().round(2)
    print("Media in secondi\n\n",medie_df,"\n")
    print("Media in minuti e secondi\n")
    print("Cubo     Minuti e secondi")
    for i, s in medie_df.items():
        print(i, "\t", conversione_secondi(s))


def grafico_media_risoluzioni(df: pandas.DataFrame) -> None:
    """Crea un grafico con i tempi medi di risoluzione per tutti i tipi di cubo.
    
    Parametri:
        df (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    df.groupby(by="Cubo")["Secondi"].mean().sort_values().plot.bar()
    plt.title("Medie delle soluzioni per tipo di cubo")
    plt.ylabel("Secondi")
    plt.xlabel("Cubi")
    plt.xticks(rotation=0)
    plt.show()


def calcola_num_risoluzioni(df: pandas.DataFrame) -> None:
    """Calcola il numero di risoluzioni per tutti i tipi di cubo.
    
    Parametri:
        df (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    print(df["Cubo"].value_counts())


def grafico_num_risoluzioni(df: pandas.DataFrame) -> None:
    """Crea un grafico con il numero di risoluzioni per tutti i tipi di cubo.
    
    Parametri:
        df (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    df["Cubo"].value_counts().plot.bar()
    plt.title("Numero di risoluzioni dei diversi cubi")
    plt.ylabel("Num di risoluzioni")
    plt.xlabel("Cubi")
    plt.xticks(rotation=0)
    plt.show()


def grafico_risoluzioni_recenti(df: pandas.DataFrame) -> None:
    """Crea un grafico con le ultime 10 risoluzioni.
    
    Parametri:
        df (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    plt.figure()
    plt.title("Tempi di risoluzione recenti")
    plt.scatter(df.tail(10)["Data completa"], df.tail(10)["Secondi"])
    plt.xticks(rotation=65)
    plt.ylabel("Secondi")
    plt.xlabel("Data")
    plt.show()


def caricamento_dati(cubo: str) -> pandas.DataFrame:
    """
    Carica i dati dal database.

    Parametri:
        cubo (str): Tipo di cubo
    
        Returns:
        df (pandas.DataFrame)
    """
    df = pandas.read_csv("../database.csv", sep="\t", parse_dates=["Data"])
    df = df[df["Cubo"] == cubo]
    # Inserimento colonna "Tempo" con i secondi convertiti in minuti e secondi
    df.insert(loc=2, column="Tempo", value=df["Secondi"].apply(conversione_secondi))
    df = aggiunta_colonne_data(df)
    return df


def stampa_record(cubo:str) -> None:
    """Stampa il record del cubo specificato
    
    Parametri:
        cubo (str): Tipo di cubo
    
    Returns:
        None
    """
    minuti, secondi = conversione_secondi((ricerca_record(cubo)))
    if minuti > 0:
        print(f"Il record attuale è di {minuti} minuti e {secondi} secondi")
    else:
        print(f"Il record attuale è di {secondi} secondi")
