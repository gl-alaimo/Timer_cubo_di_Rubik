"""Caricamento manuale nel database del tempo di risoluzione del cubo."""

from datetime import datetime
import modulo_rubik

modulo_rubik.mostra_titolo()
print("Inserisci i seguenti dati:")
data_risoluzione = input("Data (con formato ANNO-MESE-GIORNO) ad esempio '2026-03-20' oppure 'oggi': ")
if data_risoluzione == "oggi":
    data_risoluzione = datetime.now().strftime("%Y-%m-%d")

cubo = input("Digita il tipo di cubo (ad esempio 2x2x2, 3x3x3, Megaminx): ").lower()
record_personale = modulo_rubik.mostra_record(cubo=cubo)
media = modulo_rubik.calcolo_media_assoluta(cubo=cubo)
print("Media attuale:", media, "\n")
aggiungere_altra_soluzione = "si"

while aggiungere_altra_soluzione == "si":
    minuti = int(input("Minuti: "))
    secondi = int(input("Secondi: "))
    millesimi = float(input("Millesimi di secondo (ad esempio 0.43): "))
    tempo_impiegato = (minuti * 60) + secondi + millesimi
    print()

    modulo_rubik.controllo_nuovo_record(tempo_impiegato, cubo)
    record_personale = modulo_rubik.ricerca_record(cubo)
    modulo_rubik.diff_record_tempo_attuale(record=record_personale, tempo_impiegato=tempo_impiegato)
    # Informazioni sulla media
    modulo_rubik.diff_media_tempo_attuale(cubo=cubo, tempo_impiegato=tempo_impiegato)
    modulo_rubik.media_ultime_tot_risoluzioni(cubo=cubo, num_ultime_risoluzioni=100)
    modulo_rubik.media_ultime_tot_risoluzioni(cubo=cubo, num_ultime_risoluzioni=12)
    modulo_rubik.media_ultime_tot_risoluzioni(cubo=cubo, num_ultime_risoluzioni=5)

    with open(file="../database.csv", mode="a", encoding="utf-8") as db_file:
        db_file.write(f"{data_risoluzione}\t{tempo_impiegato}\t{cubo}\n")

    print("Tempo di risoluzione aggiunto al database:", data_risoluzione, tempo_impiegato, cubo)
    aggiungere_altra_soluzione = input("\nVuoi inserire un altro tempo di risoluzione per lo stesso cubo e per la stessa data? (si o no): ")
