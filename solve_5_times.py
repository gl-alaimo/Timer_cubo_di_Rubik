import rubik_library
import random
import pandas as pd
from pyfiglet import Figlet


def main_function():
    titolo = Figlet(font="speed") # http://www.figlet.org/examples.html
    print(titolo.renderText("Rubik Timer"))
    
    small_cube_moves = ['U', 'D', 'R', 'L', 'F', 'B', 'U1°', 'D1°', 'R1°', 'L1°', 'F1°', 'B1°', 'U2', 'D2', 'R2', 'L2', 'F2', 'B2']
    big_cube_moves = ["u", "d", "r", "l", "f", "b", "u1°", "d1°", "r1°", "l1°", "f1°", "b1°", "u2", "d2", "r2", "l2", "f2", "b2", "Uu2", "Dd2", "Rr2", "Ll2", "Ff2", "Bb2", "U2", "D2", "R2", "L2", "F2", "B2", "U1°", "D1°", "R1°", "L1°", "F1°", "B1°"]

    cubo = input("Digita il tipo di cubo: ")
    for solve in range(5):
        print("\nSoluzione numero", solve+1)
        if cubo == "4x4" or cubo == "5x5":
            mescolamento_random_4x4_5x5 = [random.choice(big_cube_moves) for m in range(20)]
            print("Movimenti casuali suggeriti per mischiare il cubo:\n",mescolamento_random_4x4_5x5)
        else:
            mescolamento_random_2x2_3x3 = [random.choice(small_cube_moves) for i in range(20)]
            print("Movimenti casuali suggeriti per mischiare il cubo:\n",mescolamento_random_2x2_3x3)

        tempo_impiegato, cubo = rubik_library.calcolo_tempo(cubo)
        rubik_library.salvataggio_dati(tempo_impiegato, cubo)

    df = pd.read_csv("database.csv", sep="\t")
    last_5_solves = df.tail(5)
    media = last_5_solves["Secondi"].mean()
    print("\nRisultati:")
    print("Tempo medio", media.__round__(2))
    best = last_5_solves["Secondi"].min()
    print("Tempo migliore", best.__round__(2))


if __name__ == "__main__": 
    main_function()