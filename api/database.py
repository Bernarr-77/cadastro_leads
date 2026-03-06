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
    with sqlite3.connect("leads.db") as con:
        cur = con.cursor()
        sql = """
        INSERT INTO leads(name, email, phone, status, created_at)
        VALUES (?, ?, ?, ?, ?)
        """
        cur.execute(sql, (name, email, phone, status, created_at))

def get_lead_id(lead_id):
    with sqlite3.connect("leads.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        sql = """
        SELECT * FROM leads WHERE id = ?
        """
        cur.execute(sql, (lead_id,))
        row  = cur.fetchone()
        if row:
            return dict(row)
        return None
    
def get_lead_email(lead_mail, lead_phone):
    with sqlite3.connect("leads.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        sql = """
        SELECT * FROM leads WHERE email = ? OR phone = ? 
        """
        cur.execute(sql, (lead_mail, lead_phone,))
        row  = cur.fetchone()
        if row:
            return dict(row)
        return None

if __name__ == "__main__":
    start_bank()
    print("Banco de dados funcionando 100%")


