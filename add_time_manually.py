"""Add time manually to database."""

from run_timer import is_new_record


# Inserimento dati manuali
print("Inserisci i seguenti dati:")
data_risoluzione = input("Data (ANNO-MESE-GIORNO): ")
cubo = input("Tipo di cubo: ")
minuti = int(input("Minuti: "))
secondi = int(input("Secondi: "))
millesimi = float(input("Millesimi di secondo: "))

# Conversione tempo in secondi
tempo_impiegato = (minuti * 60) + secondi + millesimi

is_new_record(tempo_impiegato, cubo)

# Salvataggio dati nel database
with open(file="database.csv", mode="a") as db_file:
    db_file.write(f"{data_risoluzione}\t{tempo_impiegato}\t{cubo}\n")

print("Tempo risoluzione aggiunto al database:", data_risoluzione, tempo_impiegato, cubo)
