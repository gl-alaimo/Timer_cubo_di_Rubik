"""Script che calcola il tempo di 5 risoluzioni e fornisce la media dei risultati escludendo
quelli con tempo minimo e massimo"""

from time import time
from pyfiglet import Figlet
import modulo_rubik


lista_tipi_cubo_piccoli = modulo_rubik.lista_tipi_cubo_piccoli
lista_dodecaedri = modulo_rubik.lista_dodecaedri
movimenti_cubi_piccoli = modulo_rubik.movimenti_cubi_piccoli
movimenti_cubi_grandi = modulo_rubik.movimenti_cubi_grandi
movimenti_pyraminx = modulo_rubik.movimenti_pyraminx
movimenti_dodecaedro = modulo_rubik.movimenti_dodecaedro
lista_risultati = []


def funzione_principale():
    """Funzione principale"""
    titolo = Figlet(font="speed") # http://www.figlet.org/examples.html
    print(titolo.renderText("Timer cubo di Rubik"))
    cubo = input("Digita il tipo di cubo (ad esempio 2x2x2, 3x3x3, megaminx): ").lower()
    if cubo in ("6x6x6", "7x7x7"):
        lista_round = [1,2,3]
    else:
        lista_round = [1,2,3,4,5]

    for num_round in lista_round:
        print(f"\nRound numero {num_round}")

        if cubo == "pyraminx":
            modulo_rubik.genera_movimenti_casuali(lista_movimenti=movimenti_pyraminx)
        elif cubo in lista_dodecaedri:
            modulo_rubik.genera_movimenti_casuali(lista_movimenti=movimenti_dodecaedro)
        elif cubo in lista_tipi_cubo_piccoli:
            modulo_rubik.genera_movimenti_casuali(lista_movimenti=movimenti_cubi_piccoli)
        else:
            modulo_rubik.genera_movimenti_casuali(lista_movimenti=movimenti_cubi_grandi)

        input("Premi invio per iniziare: ")
        ora_iniziale = time()
        input("Premi invio per terminare: ")
        ora_finale = time()
        tempo_impiegato = round(number=ora_finale - ora_iniziale, ndigits=2)
        print("Fine!\n")
        minuti, secondi = modulo_rubik.conversione_secondi(tempo_impiegato)
        if minuti == 0:
            print(f"Tempo impiegato: {secondi} secondi")
        elif minuti == 1:
            print(f"Tempo impiegato: {minuti} minuto e {secondi} secondi")
        else:
            print(f"Tempo impiegato: {minuti} minuti e {secondi} secondi")
        print("Tempo di risoluzione aggiunto al database")

        modulo_rubik.controllo_nuovo_record(tempo_impiegato=tempo_impiegato, cubo=cubo)
        modulo_rubik.salvataggio_dati(tempo=tempo_impiegato, cubo=cubo)
        lista_risultati.append(tempo_impiegato)
    
    print("\nLista di tutti i risultati", lista_risultati)
    tempo_massimo = max(lista_risultati)
    tempo_minimo = min(lista_risultati)

    if cubo not in ("6x6x6", "7x7x7"):
        print("Rimozione del maggior tempo:", tempo_massimo)
        print("Rimozione del minor tempo:", tempo_minimo)
        lista_risultati.remove(tempo_massimo)
        lista_risultati.remove(tempo_minimo)
        print("Lista dei risultati rimanenti", lista_risultati)

    media_3_risoluzioni = round(number=(lista_risultati[0] + lista_risultati[1]
                                        + lista_risultati[2]) / 3, ndigits=2)
    minuti, secondi = modulo_rubik.conversione_secondi(media_3_risoluzioni)

    if minuti == 0:
        print(f"Media delle tre risoluzioni: {secondi} secondi")
    elif minuti == 1:
        print(f"Media delle tre risoluzioni: {minuti} minuto e {secondi} secondi")
    else:
        print(f"Media delle tre risoluzioni: {minuti} minuti e {secondi} secondi")


if __name__ == "__main__":
    funzione_principale()
