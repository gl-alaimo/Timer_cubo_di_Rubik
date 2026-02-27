"""Script che misura il tempo di risoluzione e fornisce varie statistiche"""

from random import choice
from pyfiglet import Figlet
import modulo_rubik


def funzione_principale():
    """Funzione principale"""
    titolo = Figlet(font="speed") # http://www.figlet.org/examples.html
    print(titolo.renderText("Timer cubo di Rubik"))

    moviementi_cubi_piccoli = ['U', 'D', 'R', 'L', 'F', 'B', 'U1°', 'D1°', 'R1°', 'L1°', 'F1°', 'B1°', 'U2', 'D2', 'R2', 'L2', 'F2', 'B2']
    moviementi_cubi_grandi = ["u", "d", "r", "l", "f", "b", "u1°", "d1°", "r1°", "l1°", "f1°", "b1°", "u2", "d2", "r2", "l2", "f2", "b2", "Uu2", "Dd2", "Rr2", "Ll2", "Ff2", "Bb2", "U2", "D2", "R2", "L2", "F2", "B2", "U1°", "D1°", "R1°", "L1°", "F1°", "B1°"]

    cubo = input("Digita il tipo di cubo (ad esempio 2x2x2, 3x3x3, Megaminx): ").lower()
    if cubo == "4x4x4" or cubo == "5x5x5":
        mescolamento_random_4x4x4_5x5x5 = [choice(moviementi_cubi_grandi) for i in range(20)]
        print("Movimenti casuali suggeriti per mischiare il cubo:\n",mescolamento_random_4x4x4_5x5x5)
    else:
        mescolamento_random_2x2x2_3x3x3 = [choice(moviementi_cubi_piccoli) for i in range(20)]
        print("Movimenti casuali suggeriti per mischiare il cubo:\n",mescolamento_random_2x2x2_3x3x3)

    record_personale = modulo_rubik.ricerca_record(cubo)
    if record_personale != 0:
        tempo_record = modulo_rubik.conversione_secondi(record_personale)
        print(f"Record da battere: {tempo_record[0]} minuti e {tempo_record[1]} secondi")
    else:
        print("Nessun record impostato al momento.")

    tempo_impiegato, cubo = modulo_rubik.calcolo_tempo(cubo)
    modulo_rubik.controllo_nuovo_record(tempo_impiegato, cubo)
    modulo_rubik.diffs_media_tempo_attuale(cubo=cubo, tempo_impiegato=tempo_impiegato)
    modulo_rubik.diff_record_tempo_attuale(record=record_personale, tempo_impiegato=tempo_impiegato)
    modulo_rubik.media_ultime_5(cubo=cubo)
    modulo_rubik.salvataggio_dati(tempo_impiegato, cubo)


if __name__ == "__main__":
    funzione_principale()
