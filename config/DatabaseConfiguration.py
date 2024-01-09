import sqlite3

with sqlite3.connect("stock_data.db") as conn:
    cursor = conn.cursor()

    # create script_state table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS script_state (
            id INTEGER PRIMARY KEY,
            running_var TEXT
        );
    ''')

    cursor.execute('INSERT INTO script_state (id, running_var) VALUES (0, False)')
    cursor.commit()

    # create support_resistance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS support_resistance (
            symbol TEXT PRIMARY KEY,
            day_range INTEGER,
            touches INTEGER,
            sensitivity INTEGER
        );
    ''')
    cursor.commit()

    # create stock_boundaries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_boundaries (
            symbol TEXT PRIMARY KEY,
            support INTEGER,
            resistance INTEGER,
            support_distance INTEGER,
            resistance_distance INTEGER
        );
    ''')
    cursor.commit()

    # create modify_sr
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modify_sr (
            symbol TEXT,
            value INTEGER,
            binary INTEGER
        );
    ''')    
