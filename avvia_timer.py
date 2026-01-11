from random import choice
from pyfiglet import Figlet
import rubik_library


def funzione_principale():
    titolo = Figlet(font="speed") # http://www.figlet.org/examples.html
    print(titolo.renderText("Rubik Timer"))
    
    moviementi_cubi_piccoli = ['U', 'D', 'R', 'L', 'F', 'B', 'U1°', 'D1°', 'R1°', 'L1°', 'F1°', 'B1°', 'U2', 'D2', 'R2', 'L2', 'F2', 'B2']
    moviementi_cubi_grandi = ["u", "d", "r", "l", "f", "b", "u1°", "d1°", "r1°", "l1°", "f1°", "b1°", "u2", "d2", "r2", "l2", "f2", "b2", "Uu2", "Dd2", "Rr2", "Ll2", "Ff2", "Bb2", "U2", "D2", "R2", "L2", "F2", "B2", "U1°", "D1°", "R1°", "L1°", "F1°", "B1°"]

    cubo = input("Digita il tipo di cubo: ")
    if cubo == "4x4" or cubo == "5x5":
        mescolamento_random_4x4_5x5 = [choice(moviementi_cubi_grandi) for i in range(20)]
        print("Movimenti casuali suggeriti per mischiare il cubo:\n",mescolamento_random_4x4_5x5)
    else:
        mescolamento_random_2x2_3x3 = [choice(moviementi_cubi_piccoli) for i in range(20)]
        print("Movimenti casuali suggeriti per mischiare il cubo:\n",mescolamento_random_2x2_3x3)

    record_personale = rubik_library.ricerca_record(cubo)
    min, sec = rubik_library.conversione_secondi(record_personale)
    print(f"Record da battere {min} minuti e {sec} secondi")

    tempo_impiegato, cubo = rubik_library.calcolo_tempo(cubo)
    rubik_library.controllo_nuovo_record(tempo_impiegato, cubo)
    rubik_library.diffs_media_tempo_attuale(cubo=cubo, tempo_impiegato=tempo_impiegato)
    rubik_library.diff_record_tempo_attuale(record=record_personale, tempo_impiegato=tempo_impiegato)
    rubik_library.salvataggio_dati(tempo_impiegato, cubo)

if __name__ == "__main__": 
    funzione_principale()
