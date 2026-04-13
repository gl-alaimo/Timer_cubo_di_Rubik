"""Caricamento manuale del tempo di risoluzione del cubo al database."""


from datetime import datetime
import modulo_rubik


print("Inserisci i seguenti dati:")
data_risoluzione = input("Data (con formato ANNO-MESE-GIORNO) ad esempio '2026-03-20' oppure 'oggi': ")
if data_risoluzione == "oggi":
    data_risoluzione = datetime.now().strftime("%Y-%m-%d")

cubo = input("Digita il tipo di cubo (ad esempio 2x2x2, 3x3x3, Megaminx): ").lower()
aggiungere_altra_soluzione = "si"

while aggiungere_altra_soluzione == "si":
    minuti = int(input("Minuti: "))
    secondi = int(input("Secondi: "))
    millesimi = float(input("Millesimi di secondo (ad esempio 0.43): "))
    print()
    tempo_impiegato = (minuti * 60) + secondi + millesimi

    modulo_rubik.controllo_nuovo_record(tempo_impiegato, cubo)
    record_personale = modulo_rubik.ricerca_record(cubo)
    modulo_rubik.diff_record_tempo_attuale(record=record_personale, tempo_impiegato=tempo_impiegato)
    # Informazioni sulla media
    modulo_rubik.diffs_media_tempo_attuale(cubo=cubo, tempo_impiegato=tempo_impiegato)
    modulo_rubik.media_ultime_tot_risoluzioni(cubo=cubo, num_ultime_risoluzioni=100)
    modulo_rubik.media_ultime_tot_risoluzioni(cubo=cubo, num_ultime_risoluzioni=12)
    modulo_rubik.media_ultime_tot_risoluzioni(cubo=cubo, num_ultime_risoluzioni=5)

    with open(file="../database.csv", mode="a", encoding="utf-8") as db_file:
        db_file.write(f"{data_risoluzione}\t{tempo_impiegato}\t{cubo}\n")

    print("Tempo risoluzione aggiunto al database:", data_risoluzione, tempo_impiegato, cubo)
    aggiungere_altra_soluzione = input("\nVuoi inserire un altro tempo per lo stesso cubo? (si o no): ")
