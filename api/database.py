import sqlite3 


def start_bank():
    con = sqlite3.connect("leads.db")
    cur = con.cursor()

    sql_command = '''
    CREATE TABLE IF NOT EXISTS leads(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        created_at TEXT,
        phone TEXT NOT NULL UNIQUE,
        status TEXT
    )
    '''
    cur.execute(sql_command)

    con.commit()
     
    con.close()

def save_lead(name, email, phone, status, created_at):
    con = sqlite3.connect("leads.db")
    cur = con.cursor()
    sql = """
    INSERT INTO leads(name, email, phone, status, created_at)
    VALUES (?, ?, ?, ?, ?)
    """
    cur.execute(sql, (name, email, phone, status, created_at))
    
    con.commit()
     
    con.close()

if __name__ == "__main__":
    start_bank()
    print("Banco de dados funcionando 100%")


