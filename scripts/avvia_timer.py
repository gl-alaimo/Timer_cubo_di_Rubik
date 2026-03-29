"""Script che calcola il tempo di risoluzione e fornisce varie statistiche"""

from random import choice, shuffle
from pyfiglet import Figlet
import modulo_rubik


lista_tipi_cubo_piccoli = modulo_rubik.lista_tipi_cubo_piccoli
movimenti_cubi_piccoli = modulo_rubik.movimenti_cubi_piccoli
movimenti_cubi_grandi = modulo_rubik.movimenti_cubi_grandi


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


def funzione_principale():
    """Funzione principale"""
    titolo = Figlet(font="speed") # http://www.figlet.org/examples.html
    print(titolo.renderText("Timer cubo di Rubik"))
    cubo = input("Digita il tipo di cubo (ad esempio 2x2x2, 3x3x3, megaminx): ").lower()
    riprovare = "si"

    while riprovare == "si":
        if cubo in lista_tipi_cubo_piccoli:
            genera_mosse_casuali(lista=movimenti_cubi_piccoli)
        else:
            genera_mosse_casuali(lista=movimenti_cubi_grandi)

        record_personale = modulo_rubik.ricerca_record(cubo)
        if record_personale != 0:
            minuti, secondi = modulo_rubik.conversione_secondi(record_personale)
            if minuti == 0:
                print(f"Record da battere: {secondi} secondi")
            elif minuti == 1:
                print(f"Record da battere: {minuti} minuto e {secondi} secondi")
            else:
                print(f"Record da battere: {minuti} minuti e {secondi} secondi")
        else:
            print("Nessun record impostato al momento.")

        tempo_impiegato, cubo = modulo_rubik.calcolo_tempo(cubo)
        # Informazioni sul record
        modulo_rubik.controllo_nuovo_record(tempo_impiegato, cubo)
        modulo_rubik.diff_record_tempo_attuale(record=record_personale, tempo_impiegato=tempo_impiegato)
        # Informazioni sulla media
        modulo_rubik.diffs_media_tempo_attuale(cubo=cubo, tempo_impiegato=tempo_impiegato)
        modulo_rubik.media_ultime_tot_risoluzioni(cubo=cubo, num_ultime_risoluzioni=100)
        modulo_rubik.media_ultime_tot_risoluzioni(cubo=cubo, num_ultime_risoluzioni=12)
        modulo_rubik.media_ultime_tot_risoluzioni(cubo=cubo, num_ultime_risoluzioni=5)
        # Salvataggio risoluzione e prompt
        modulo_rubik.salvataggio_dati(tempo_impiegato, cubo)
        riprovare = input("\nVuoi riprovare? (digita 'si' oppure 'no' e premi invio): ")
        print()


if __name__ == "__main__":
    funzione_principale()