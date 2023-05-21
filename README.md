# Blind SQL Injection Data Spoofer

This repository contains solutions to a Computer Security Challenge involving Blind SQL Injection Attack.

The solution includes 3 Python scripts: 

1. `tables_spoofer.py`: This script spoofs the attacked database's tables and their indexes and writes them into `tables.txt`.
2. `columns_spoofer.py`: This script identifies the columns of specific tables and writes the result into `columns.txt`.
3. `flag_spoofer.py`: This script identifies the attacked user's flag stored in a specific row and column of a table in the database and writes the flag into `flag.txt`.

## Prerequisites
- Python 3.6+
- `requests` library for Python

## Usage

**Step 1.** Modify the `session_cookie` in each script with your own cookie.

**Step 2.** Run `tables_spoofer.py` to find the table indexes and names.
```bash
python tables_spoofer.py
```
The output will be stored in `tables.txt`.

**Step 3.** Modify the `tables_names` variable in `columns_spoofer.py` with the tables you wish to know the columns of. Then, run the script:
```bash
python columns_spoofer.py
```
The output will be stored in `columns.txt`.

**Step 4.** In `flag_spoofer.py`, modify `table_name_where_flag_is`, `column_name_where_flag_is`, `username_column_name`, and `attacked_username` according to your needs. Then, run the script:
```bash
python flag_spoofer.py
```
The flag will be stored in `flag.txt`.

## Disclaimer
These scripts are provided for educational purposes only. Unauthorized access to a computer system is illegal, and this repository does not condone or promote such actions.
