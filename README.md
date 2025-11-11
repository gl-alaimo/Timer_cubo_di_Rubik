# Rubik Timer time tracker

This repository contains a set of Python scripts for managing and logging Rubik's Cube time-related data. It includes functionality for manually adding time entries, running a timer, and storing data in a CSV file.
The scripts suggests moves to perform in order to scrumble the cube and allows to pause the timer. In the end calculates average time, records, diffs between current solve and average and record.

## Files and Their Purpose

### `run_timer.py`
This script runs a timer and logs the results into the `database.csv` file. It is useful for tracking time while solving the cube in real time.

### `add_time_manually.py`
This script allows you to manually add time entries to the `database.csv` file. It is useful for logging data that was not recorded in real-time.

### `database.csv`
A tab-separated values (TSV) file that stores time data. Each row contains:
- **Data**: The date of the entry (e.g., `2025-11-08`).
- **Secondi**: The time recorded in seconds (e.g., `281.5`).
- **Cubo**: The type of cube (e.g., `4x4`, `3x3`).

### `notebook.ipynb`
A Jupyter Notebook for analyzing and visualizing the data stored in `database.csv`.

## How to run the scripts

- Run the timer: `python run_timer.py`
- Add time manually: `python add_time_manually.py`


## License

This project is private.<br>
Author: Giuseppe Luca Alaimo (gl-alaimo)
