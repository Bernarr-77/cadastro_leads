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
    
def get_lead_email(lead_mail, lead_phone, lead_name, lead_id):
    with sqlite3.connect("leads.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        sql = """
        SELECT * FROM leads WHERE email = ? OR phone = ? OR id = ? OR name LIKE ?
        """
        cur.execute(sql, (lead_mail, lead_phone,lead_id,f"%{lead_name}%",))
        row  = cur.fetchall()
        if row:
            return [dict(r) for r in row]
        return None
    
def delete_lead_id(lead_id):
    with sqlite3.connect("leads.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        sql = """
        DELETE FROM leads WHERE id = ?
        """
        cur.execute(sql, (lead_id,))
        affected_lines = cur.rowcount
        return affected_lines
    
def update_lead(name, email, phone, status, lead_id ):
    with sqlite3.connect("leads.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        sql = """
        UPDATE leads SET name=?, email=?, phone=?, status=? WHERE id = ?
        """
        cur.execute(sql, (name,email,phone,status,lead_id,))

# def get_lead_by_name(name):
#         with sqlite3.connect("leads.db") as con:
#             con.row_factory = sqlite3.Row
#             cur = con.cursor()
#             sql = """
#             SELECT * FROM leads WHERE name LIKE = 
#             """
#             cur.execute(sql, (f"%{name}%",))
#             row  = cur.fetchall()
#             return row
        
if __name__ == "__main__":
    start_bank()
    print("Banco de dados funcionando 100%")


