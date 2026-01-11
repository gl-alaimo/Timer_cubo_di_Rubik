# Progetto Rubik Timer

Questo progetto è un'applicazione Python progettata per gestire e analizzare i tempi di risoluzione del cubo di Rubik. Include funzionalità per registrare i tempi in tempo reale o caricare tempi di risoluzione manualmente.

## Struttura del Progetto

- **rubik_library.py**: Libreria Python con funzioni utili per la gestione del cubo di Rubik.
- **avvia_timer.py**: Script principale per avviare il timer e registrare i tempi di risoluzione.
- **carica_tempo.py**: Script per caricare i tempi salvati da un file CSV.
- **risolvi_5_volte.py**: Script per risolvere il cubo 5 volte e registrare i tempi.
- **database.csv**: File CSV che memorizza i tempi di risoluzione.
- **notebook.ipynb**: Notebook Jupyter per analisi e visualizzazioni dei dati.

## Tipi di cubi supportati
<li>2x2
<li>3x3
<li>4x4
<li>5x5
<li>Mirror
<li>Megaminx

## Requisiti

- Python 3.x
- Librerie aggiuntive specificate nel file `requirements.txt`.

## Come Utilizzare
Per prima cosa bisogna andare nella cartella "scripts" con il seguente comando del terminale:
`cd scripts` e poi eseguire uno dei comandi descritti sotto:
1. **Avviare il Timer**:
   Esegui lo script `avvia_timer.py` per registrare i tempi di risoluzione:
   ```bash
   python avvia_timer.py
2. **Caricare i dati manualmente**:
    Esegui lo script `carica_tempo.py` per caricare i tempi di risoluzione:
    ```bash
    python carica_tempo.py
3. **Riolvere il cubo 5 volte**:
    Esegui lo script `risolvi_5_volte.py` per registrare i tempi di risoluzione:
    ```bash
    python risolvi_5_volte.py
4. **Eseguire il notebook**:
    Eseguire il notebook in un ambiente supportato (ad esempio Jupyter https://jupyter.org/)
## Contributi
Se desideri contribuire al progetto, sentiti libero di aprire una pull request o segnalare problemi nella sezione "Issues".

## Licenza
Questo progetto è distribuito sotto la licenza MIT.

## Contatti
Giuseppe Luca Alaimo gl.alaimo@protonmail.com