"""Caricamento manuale del tempo di risoluzione del cubo al database."""


from datetime import datetime

from scripts.modulo_rubik import controllo_nuovo_record


print("Inserisci i seguenti dati:")
data_risoluzione = input("Data (ANNO-MESE-GIORNO) oppure 'oggi': ")
if data_risoluzione == "oggi":
    data_risoluzione = datetime.now().strftime("%Y-%m-%d")

cubo = input("Tipo di cubo: ")
aggiungere_altra_soluzione = "si"

while aggiungere_altra_soluzione == "si":
    minuti = int(input("Minuti: "))
    secondi = int(input("Secondi: "))
    millesimi = float(input("Millesimi di secondo (per esempio 0.43): "))
    tempo_impiegato = (minuti * 60) + secondi + millesimi

    controllo_nuovo_record(tempo_impiegato, cubo)

    with open(file="../database.csv", mode="a", encoding="utf-8") as db_file:
        db_file.write(f"{data_risoluzione}\t{tempo_impiegato}\t{cubo}\n")

    print("Tempo risoluzione aggiunto al database:", data_risoluzione, tempo_impiegato, cubo)
    aggiungere_altra_soluzione = input("\nVuoi inserire un altro tempo per lo stesso cubo? (si o no): ")
