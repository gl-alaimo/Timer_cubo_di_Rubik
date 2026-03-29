"""Modulo Rubik timer"""

from datetime import datetime
from time import time
from random import choice, shuffle
import pandas
from matplotlib import pyplot as plt


lista_tipi_cubo_piccoli = ["2x2x2", "3x3x3",  "mirror", "kilominx", "pyraminx", "megaminx"]
movimenti_cubi_piccoli = [["U", "U'", "U2"], ["D", "D'", "D2"],
                          ["L", "L'", "L2"], ["R", "R'", "R2"],
                          ["B", "B'", "B2"], ["F", "F'", "F2"]]
movimenti_cubi_grandi = [["U", "U'", "u", "u'", "U2", "u2", "Uu2"],
                         ["D", "D'", "d", "d'", "D2", "d2", "Dd2"],
                         ["L", "L'", "l", "l'", "L2", "l2", "Ll2"],
                         ["R", "R'", "r", "r'", "R2", "r2", "Rr2"],
                         ["B", "B'", "b", "b'", "B2", "b2", "Bb2"],
                         ["F", "F'", "f", "f'", "F2", "f2", "Ff2"],
                         ["M", "M'", "m", "m'", "M2", "m2", "Mm2"],
                         ["S", "S'", "s", "s'", "S2", "s2", "Ss2"],
                         ["E", "E'", "e", "e'", "E2", "e2", "Ee2"]]

# Funzioni per gli script

def genera_mosse_casuali(lista:list):
    """Genera una lista di mosse casuali da fare per mischiare il cubo prima di risolverlo"""
    lista_movimenti_casuali_a = []
    lista_movimenti_casuali_b = []
    lista_movimenti_casuali_c = []

    for mossa in lista:
        lista_movimenti_casuali_a.append(choice(mossa))
        lista_movimenti_casuali_b.append(choice(mossa))
        lista_movimenti_casuali_c.append(choice(mossa))

    shuffle(lista_movimenti_casuali_a)
    shuffle(lista_movimenti_casuali_b)
    shuffle(lista_movimenti_casuali_c)

    if lista_movimenti_casuali_a[-1].startswith(lista_movimenti_casuali_b[0]):
        lista_movimenti_casuali_a.pop()
    if lista_movimenti_casuali_b[-1].startswith(lista_movimenti_casuali_c[0]):
        lista_movimenti_casuali_b.pop()

    lista_movimenti_casuali = lista_movimenti_casuali_a + lista_movimenti_casuali_b + lista_movimenti_casuali_c
    print("Movimenti casuali suggeriti per mischiare il cubo:\n", *lista_movimenti_casuali)


def conversione_secondi(secondi: int) -> tuple:
    """Converte i secondi in minuti e secondi
    
    Params:
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

    Params:
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

    Params:
        tempo_impiegato (int): Tempo impiegato in secondi
        cubo (str): Tipo di cubo
    Returns:
        Stampa informazioni sul record
    """
    mio_record = ricerca_record(cubo)
    if tempo_impiegato < mio_record:
        record_min, record_sec = conversione_secondi(mio_record)
        minuti_attuali, secondi_attuali = conversione_secondi(tempo_impiegato)

        if record_min-minuti_attuali == 0:
            print(f"Hai battuto il tuo record di {abs(round(number=record_sec-secondi_attuali, ndigits=2))} secondi!!!")
        elif record_min-minuti_attuali == 1:
            print(f"Hai battuto il tuo record di {record_min-minuti_attuali} "
                  f"minuto e {abs(round(number=record_sec-secondi_attuali, ndigits=2))} secondi!!!")
        else:
            print(f"Hai battuto il tuo record di {record_min-minuti_attuali} "
                  f"minuti e {abs(round(number=record_sec-secondi_attuali, ndigits=2))} secondi!!!")

        if record_min == 0:
            print(f"Record precedente: {record_sec} secondi")
        elif record_min == 1:
            print(f"Record precedente: {record_min} minuto e {record_sec} secondi")
        else:
            print(f"Record precedente: {record_min} minuti e {record_sec} secondi")


def calcolo_tempo(cubo:str) -> tuple:
    """Calcola il tempo impiegato.

    Params:
        cubo (str): Tipo di cubo
    Returns:
        tempo_impiegato, cubo (tuple): Stampa informazioni e restiruisce una tuple
        con il tempo impiegato e il tipo di cubo
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
            if min == 0:
                print(f"In pausa... Tempo impiegato fino ad ora: {sec} secondi")
            elif min == 1:
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
    if min == 0:
        print(f"Tempo impiegato: {sec} secondi")
    elif min == 1:
        print(f"Tempo impiegato: {min} minuto e {sec} secondi")
    else:
        print(f"Tempo impiegato: {min} minuti e {sec} secondi")
    return tempo_impiegato, cubo


def salvataggio_dati(tempo:int, cubo:str) -> None:
    """Salva il tempo di risoluzione nel database

    Params:
        tempo (int): Tempo impiegato
        cubo (str): Tipo di cubo
    Returns:
        Salva i dati in un file csv
    """
    data = datetime.now().date()
    with open(file="../database.csv", mode="a", encoding="utf-8") as db_file:
        db_file.write(f"{data}\t{tempo}\t{cubo}\n")


def diffs_media_tempo_attuale(cubo:str, tempo_impiegato:int) -> None:
    """Calcola la differenza del tempo medio di risoluzione e il tempo di risoluzione attuale

    Params:
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
        if media_in_minuti_formattata[0] == 0:
            media_in_minuti_formattata = f"{media_in_minuti[1]} secondi"
        elif media_in_minuti_formattata[0] == 1:
            media_in_minuti_formattata = f"{media_in_minuti[0]} minuto e {media_in_minuti[1]} secondi"
        else:
            media_in_minuti_formattata = f"{media_in_minuti[0]} minuti e {media_in_minuti[1]} secondi"

        print("La tua media assoluta è di", media_in_minuti_formattata)
        if tempo_impiegato < media:
            print(f"Ci hai impiegato {round(number=media-tempo_impiegato, ndigits=2)} secondi in meno rispetto alla media assoluta")
        elif tempo_impiegato > media:
            print(f"Ci hai impiegato {round(number=tempo_impiegato-media, ndigits=2)} secondi in piu rispetto alla media assoluta")
        else:
            print("Ci hai impiegato come al solito")


def diff_record_tempo_attuale(record:int, tempo_impiegato:int) -> None:
    """Calcola la differenza di tempo tra il record personale e il tempo di risoluzione attuale
    
    Params:
        record (int): Record attuale
        tempo_impiegato (int): Tempo impiegato
    Returns:
        Stampa informazioni sul terminale
    """
    if record != 0:
        if tempo_impiegato > record:
            print("Ci hai impiegato", round(number=tempo_impiegato-record, ndigits=2), "secondi in più rispetto al record")
        elif tempo_impiegato == record:
            print("Hai eguagliato il tuo record")
        else:
            pass # Informazioni sul record in questo caso verrano date dalla funzione controllo_nuovo_record()


def media_ultime_tot_risoluzioni(cubo:str, num_ultime_risoluzioni: int) -> None:
    """Calcola la media delle ultime 5 risoluzioni per un determinato tipo di cubo
    
    Params:
        cubo (str): Tipo di cubo
        num_ultime_risoluzioni (int): Numero delle ultime risoluzioni
    Returns:
        Stampa informazioni sul terminale
    """
    df = pandas.read_csv("../database.csv", sep="\t")
    if len(df[df["Cubo"] == cubo]) >= num_ultime_risoluzioni:
        ultime_risoluzioni = df[df["Cubo"] == cubo].tail(num_ultime_risoluzioni)["Secondi"]
        media_soluzioni, tempi_totali = 0, 0
        for tempo in ultime_risoluzioni:
            tempi_totali = tempi_totali + tempo
        media_soluzioni = tempi_totali / num_ultime_risoluzioni
        minuti, secondi = conversione_secondi(media_soluzioni)
        if minuti == 0:
            print(f"Media delle ultime {num_ultime_risoluzioni} risoluzioni: {secondi} secondi")
        elif minuti == 1:
            print(f"Media delle ultime {num_ultime_risoluzioni} risoluzioni: {minuti} minuto e {secondi} secondi")
        else:
            print(f"Media delle ultime {num_ultime_risoluzioni} risoluzioni: {minuti} minuti e {secondi} secondi")


def aggiunta_colonne_data(df_cubo:pandas.DataFrame) -> pandas.DataFrame:
    """Aggiunge colonne 'Anno' 'Mese' e 'Giorno" al DataFrame e riordina le colonne.

    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
    Returns:
        df_cubo (pandas.DataFrame): DataFrame aggiornato
    """
    df_cubo = df_cubo.assign(Anno=df_cubo["Data"].dt.year)
    df_cubo = df_cubo.assign(Mese=df_cubo["Data"].dt.month)
    df_cubo = df_cubo.assign(Giorno=df_cubo["Data"].dt.day)
    df_cubo = df_cubo[["Data", "Anno", "Mese", "Giorno", "Secondi", "Tempo", "Cubo"]] # Riordinamento colonne
    df_cubo = df_cubo.rename(columns={"Data":"Data completa"}) # Cambio nome colonna Data
    df_cubo["Mese"] = df_cubo["Mese"].replace({1:"Gennaio",
                                    2:"Febbraio",
                                    3:"Marzo",
                                    4:"Aprile",
                                    5:"Maggio",
                                    6:"Giugno",
                                    7:"Luglio",
                                    8:"Agosto",
                                    9:"Settembre",
                                    10:"Ottobre",
                                    11:"Novembre",
                                    12:"Dicembre"
                                    })
    return df_cubo

# Funzioni per i notebook

def grafico_medie_mensili(df_cubo: pandas.DataFrame, anno: int) -> None:
    """Crea un grafico con il tempo medio mensile delle soluzioni per un determinato tipo di cubo.
    
    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        anno (int): Anno per cui calcolare le medie mensili.
        
    Returns:
        None
    """
    dati_per_grafico = df_cubo[df_cubo["Anno"]==anno].groupby(by=["Mese"], sort=False)["Secondi"].mean()
    grafico = dati_per_grafico.plot(kind="bar", figsize=(11,5))
    plt.title(label=f"Tempo medio mensile delle risoluzioni nel {anno}")
    plt.ylabel(ylabel="Secondi")
    plt.xlabel(xlabel="Mese")
    plt.xticks(rotation=0)
    for la_barra in grafico.containers:
        grafico.bar_label(container=la_barra, labels=dati_per_grafico.values.round(2), label_type='center')
    plt.show()


def mostra_record_mensili(df_cubo: pandas.DataFrame, anno: int):
    """Mostra i tempi record mensili delle soluzioni per un determinato tipo di cubo e anno.
    
    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        anno (int): Anno per cui calcolare i record mensili.
        
    Returns:
        None
    """
    print("Record stabiliti ogni mese\n")
    print(df_cubo[df_cubo["Anno"]==anno].groupby(by=["Mese"], sort=False)["Secondi"].min())


def grafico_record_mensili(df_cubo: pandas.DataFrame, anno: int) -> None:
    """Crea un grafico con i tempi record mensili delle soluzioni per un determinato tipo di cubo e anno.
    
    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        anno (int): Anno per cui calcolare i record mensili.
        
    Returns:
        None
    """
    dati_per_grafico = df_cubo[df_cubo["Anno"]==anno].groupby(by=["Mese"], sort=False)["Secondi"].min()
    grafico = dati_per_grafico.plot(kind="bar", figsize=(11,5))
    plt.title(label=f"Tempo record mensile delle risoluzioni nel {anno}")
    plt.ylabel(ylabel="Secondi")
    plt.xlabel(xlabel="Mese")
    plt.xticks(rotation=0)
    for la_barra in grafico.containers:
        grafico.bar_label(container=la_barra, labels=dati_per_grafico.values.round(2), label_type='center')
    plt.show()


def grafico_medie_annuali(df_cubo: pandas.DataFrame) -> None:
    """Crea un grafico con il tempo medio annuale delle soluzioni per un determinato tipo di cubo.
    
    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    dati_per_grafico = df_cubo.groupby(by=["Anno"])["Secondi"].mean()
    grafico = dati_per_grafico.plot(kind="bar", figsize=(11,5))
    plt.title(label="Tempo medio annuale delle risoluzioni")
    plt.ylabel(ylabel="Secondi")
    plt.xlabel(xlabel="Anno")
    plt.xticks(rotation=0)
    for la_barra in grafico.containers:
        grafico.bar_label(container=la_barra, labels=dati_per_grafico.values.round(2), label_type='center')
    plt.show()


def stampa_record_media_massimo(df_cubo: pandas.DataFrame, cubo:int) -> None:
    """Stampa il tempo massimo, medio e minimo
    
    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        cubo (str): Tipo di cubo
        
    Returns:
        None
    """
    record = ricerca_record(cubo)
    record_min, record_sec = conversione_secondi(record)
    media = df_cubo["Secondi"].mean().round(2)
    media_min, media_sec = conversione_secondi(media)
    tempo_massimo = df_cubo["Secondi"].max().round(2)
    tempo_massimo_min, tempo_massimo_sec = conversione_secondi(tempo_massimo)
    print("Tempo minimo medio e massimo delle risoluzioni:")
    print(f"- Tempo minimo {record_min}:{record_sec}\n",
          f"- Tempo medio {media_min}:{media_sec}\n",
          f"- Tempo massimo {tempo_massimo_min}:{tempo_massimo_sec}")


def grafico_record_media_massimo(df_cubo: pandas.DataFrame) -> None:
    """Crea un grafico a barre con tempo record, media e tempo massimo per un determinato tipo di cubo.
    
    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    plt.figure(figsize=(11,5))
    plt.bar(x=["Tempo minimo", "Tempo medio", "Tempo massimo"],
            height=[ricerca_record(cubo=df_cubo["Cubo"].iloc[0]),
                    df_cubo["Secondi"].mean().round(2),
                    df_cubo["Secondi"].max().round(2)],
            color=["green", "blue", "red"],
            width=0.3)
    plt.title("Tempo minimo, medio e massimo")
    plt.ylabel("Secondi")
    plt.show()


def grafico_risoluz_mensile(df_cubo: pandas.DataFrame, anno: int) -> None:
    """Crea un grafico a barre con il numero di risoluzioni mensili per un determinato tipo di cubo.
    
    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        anno (int): Anno per cui calcolare il numero di risoluzioni mensili.
        
    Returns:
        None
    """
    dati_per_grafico = df_cubo[df_cubo["Anno"]==anno]["Data completa"].dt.month.value_counts().sort_index()
    grafico = dati_per_grafico.plot(kind="bar", figsize=(11,5))
    plt.title(f"Numero risoluzioni mensili del {anno}")
    plt.ylabel("Num risoluzioni")
    plt.xlabel("Mese")
    plt.xticks(rotation=0)
    for la_barra in grafico.containers:
        grafico.bar_label(container=la_barra, labels=dati_per_grafico.values, label_type='center')
    plt.show()


def grafico_tutti_record(df_cubo: pandas.DataFrame) -> None:
    """Crea un grafico con i record per tutti i tipi di cubo.
    
    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    dati_per_grafico = df_cubo.drop(columns=["Data", "Tempo"]).groupby(by="Cubo").min().sort_values(by="Secondi")
    grafico = dati_per_grafico.plot.bar(figsize=(11,5))
    plt.title("Soluzioni piu veloci per tipo di cubo")
    plt.ylabel("Secondi")
    plt.xlabel("Cubi")
    plt.xticks(rotation=0)
    for barra in grafico.containers:
        grafico.bar_label(container=barra, labels=dati_per_grafico.values[0], label_type="edge")
    plt.show()


def mostra_tutti_record(df_cubo: pandas.DataFrame) -> None:
    """Mostra i record per tutti i tipi di cubo.
    
    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    df_records = df_cubo[["Secondi", "Cubo"]].groupby(by="Cubo").min()
    df_records.insert(loc=1, column="Tempo", value=df_records["Secondi"].apply(conversione_secondi))
    df_records['Tempo'] = df_records['Tempo'].apply(lambda x: f"{x[0]}:{x[1]:05.2f}")
    print(df_records)


def calcola_media_risoluzioni(df_cubo: pandas.DataFrame) -> None:
    """Calcola la media dei tempi di risoluzione per tutti i tipi di cubo.
    
    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    medie_df = df_cubo[["Secondi", "Cubo"]].groupby(by="Cubo").mean().round(2)
    medie_df.insert(loc=1, column="Tempo", value=medie_df["Secondi"].apply(conversione_secondi))
    medie_df['Tempo'] = medie_df['Tempo'].apply(lambda x: f"{x[0]}:{x[1]:05.2f}")
    print(medie_df)


def grafico_media_risoluzioni(df_cubo: pandas.DataFrame) -> None:
    """Crea un grafico con i tempi medi di risoluzione per tutti i tipi di cubo.
    
    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    dati_per_grafico = df_cubo[["Secondi", "Cubo"]].groupby(by="Cubo").mean().round(2).sort_values(by="Secondi")
    grafico = dati_per_grafico.plot.bar(figsize=(11,5))
    plt.title("Medie delle soluzioni per tipo di cubo")
    plt.ylabel("Secondi")
    plt.xlabel("Cubi")
    plt.xticks(rotation=0)
    for barra in grafico.containers:
        grafico.bar_label(container=barra, labels=dati_per_grafico.values[0].round(2), label_type="edge")
    plt.show()


def calcola_num_risoluzioni(df_cubo: pandas.DataFrame) -> None:
    """Calcola il numero di risoluzioni per tutti i tipi di cubo.
    
    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    print(df_cubo["Cubo"].value_counts())


def grafico_num_risoluzioni(df_cubo: pandas.DataFrame) -> None:
    """Crea un grafico con il numero di risoluzioni per tutti i tipi di cubo.
    
    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    dati_per_grafico = df_cubo["Cubo"].value_counts()
    grafico = dati_per_grafico.plot(kind="bar", figsize=(11,5))
    plt.title("Numero di risoluzioni dei diversi cubi")
    plt.ylabel("Num di risoluzioni")
    plt.xlabel("Cubi")
    plt.xticks(rotation=0)
    for barra in grafico.containers:
        grafico.bar_label(container=barra,labels=dati_per_grafico.values, label_type="center")
    plt.show()


def grafico_risoluzioni_recenti(df_cubo: pandas.DataFrame) -> None:
    """Crea un grafico con le ultime 10 risoluzioni.
    
    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        
    Returns:
        None
    """
    plt.figure(figsize=(13,5))
    plt.title("Tempi e data delle risoluzioni recenti")
    plt.scatter(df_cubo.tail(10)["Data completa"], df_cubo.tail(10)["Secondi"])
    plt.grid(axis="y")
    plt.xticks(rotation=0)
    plt.ylabel("Secondi")
    plt.xlabel("Data")
    plt.show()


def caricamento_dati(cubo: str) -> pandas.DataFrame:
    """Carica i dati dal database.

    Params:
        cubo (str): Tipo di cubo
    
    Returns:
        df (pandas.DataFrame)
    """
    df = pandas.read_csv("../database.csv", sep="\t", parse_dates=["Data"])
    df = df[df["Cubo"] == cubo]
    df = df.reset_index(drop=True)
    # Inserimento colonna "Tempo" con i secondi convertiti in minuti e secondi
    df.insert(loc=2, column="Tempo", value=df["Secondi"].apply(conversione_secondi))
    df['Tempo'] = df['Tempo'].apply(lambda x: f"{x[0]}:{x[1]:05.2f}")
    df = aggiunta_colonne_data(df)
    return df


def caricamento_dati_notebook_generale() -> pandas.DataFrame:
    """Carica i dati di tutti i tipi di cubi dal database.

    Params:
        None

    Returns:
        df (pandas.DataFrame): Dataframe con i dati caricati dal database
    """
    df = pandas.read_csv("../database.csv", sep="\t", parse_dates=["Data"])
    # Inserimento colonna "Tempo" con i secondi convertiti in minuti e secondi
    df.insert(loc=2, column="Tempo", value=df["Secondi"].apply(conversione_secondi))
    # Formattazione del tempo in min:sec,millisec
    df['Tempo'] = df['Tempo'].apply(lambda x: f"{x[0]}:{x[1]:05.2f}")
    return df


def stampa_record(cubo:str) -> None:
    """Stampa il record del cubo specificato
    
    Params:
        cubo (str): Tipo di cubo
    
    Returns:
        None
    """
    minuti, secondi = conversione_secondi((ricerca_record(cubo)))
    if minuti == 0:
        print(f"Il record attuale è di {secondi} secondi")
    elif minuti == 1 :
        print(f"Il record attuale è di {minuti} minuto e {secondi} secondi")
    else:
        print(f"Il record attuale è di {minuti} minuti e {secondi} secondi")


def medie_risoluzioni_mensili(df_cubo:pandas.DataFrame, anno:int) -> pandas.Series:
    """Stampa i tempi medi di risoluzione mensili del cubo e dell'anno specificato.
    
    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        anno (int): Anno per cui calcolare le medie mensili.
    
    Returns:
        None
    """
    print("Tempi medi delle risoluzioni mensili\n")
    print(df_cubo[df_cubo["Anno"]==anno].groupby(by=["Mese"], sort=False)["Secondi"].mean().round(2))


def numero_risoluzioni_mensili(df_cubo:pandas.DataFrame, anno:int) -> pandas.Series:
    """Mostra il numero di risoluzioni mensili dell'anno specificato.

    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        anno (int): anno
    
    Returns:
        None
    """
    print(f"Numero di risoluzioni mensili del {anno}\n")
    print(df_cubo[df_cubo["Anno"]==anno]["Mese"].value_counts())


def medie_risoluzioni_annuali(df_cubo:pandas.DataFrame):
    """Stampa i tempi medi di risoluzione annuali.
    
    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
    
    Returns:
        None
    """
    print("Tempi medi mensili in secondi delle risoluzioni annuali\n")
    print(df_cubo.groupby(by=["Anno"])["Secondi"].mean().round(2))


def grafico_ultime_tot_risoluzioni(df_cubo: pandas.DataFrame, num_ultime_risoluzioni:int = 50) -> None:
    """Crea un grafico con i tempi e la media delle ultime tot risoluzioni.

    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.
        num_ultime_risoluzioni (int): Numero delle ultime risoluzioni. 
        Se non specificato, il suo valore predefinito è 50.

    Returns:
        None
    """
    df_cubo = df_cubo.tail(num_ultime_risoluzioni)
    media = df_cubo["Secondi"].mean().round(2)

    plt.figure(figsize=(13,5))
    plt.title(f"Tempi delle ultime {num_ultime_risoluzioni} risoluzioni")
    plt.scatter(df_cubo.index, df_cubo["Secondi"])
    plt.plot(df_cubo.index, df_cubo["Secondi"])
    plt.axhline(y=media, color="purple", label="Media")
    plt.grid(axis="y")
    plt.xticks(rotation=0)
    plt.ylabel("Secondi")
    plt.xlabel("Numemo risoluzione")
    plt.legend()
    plt.show()

    minuti, secondi = conversione_secondi(media)
    print(f"Tempo medio: {minuti}:{secondi}")


def classifica_migliori_soluzioni(df_cubo: pandas.DataFrame) -> None:
    """Mostra informazioni sui tempi delle 10 risoluzioni migliori.

    Params:
        df_cubo (pandas.DataFrame): DataFrame contenente i dati delle risoluzioni.

    Returns:
        None
    """
    print("Classifica delle 10 risoluzioni più veloci\n")
    df_top_10 = df_cubo.sort_values(by="Secondi", ascending=True).head(10).reset_index(drop=True)
    df_top_10.insert(loc=6, column="Differenza secondi", value=pandas.DataFrame.diff(df_top_10["Secondi"]))
    df_top_10["Differenza secondi"] = df_top_10["Differenza secondi"].fillna(value=0)
    df_top_10.drop(columns=["Cubo"], inplace=True)
    print(df_top_10)