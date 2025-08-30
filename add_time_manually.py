"""Add time manually to database."""
import datetime

from run_timer import is_new_record


# Inserimento dati manuali
print("Inserisci i seguenti dati:")
data_risoluzione = input("Data (ANNO-MESE-GIORNO) oppure 'oggi': ")
if data_risoluzione == "oggi":
    data_risoluzione = datetime.datetime.now().strftime("%Y-%m-%d")

cubo = input("Tipo di cubo: ")
agg_altra_soluzione = "si"

while agg_altra_soluzione == "si":
    minuti = int(input("Minuti: "))
    secondi = int(input("Secondi: "))
    millesimi = float(input("Millesimi di secondo (per esempio 0.43): "))
    # Conversione tempo in secondi
    tempo_impiegato = (minuti * 60) + secondi + millesimi

    is_new_record(tempo_impiegato, cubo)

    # Salvataggio dati nel database
    with open(file="database.csv", mode="a") as db_file:
        db_file.write(f"{data_risoluzione}\t{tempo_impiegato}\t{cubo}\n")

    print("Tempo risoluzione aggiunto al database:", data_risoluzione, tempo_impiegato, cubo)
    agg_altra_soluzione = input("\nVuoi inserire un altro tempo per lo stesso cubo? (si o no): ")
