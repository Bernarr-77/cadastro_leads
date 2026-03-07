import sqlite3
import random
from datetime import datetime
from faker import Faker

fake = Faker('pt_BR')

def seedbomb(quantidade = 30000):
    lote_de_dados = []
    status_opcoes = ["novo","em negociação", "fechado", " perdido"]
    for _ in range(quantidade):
        nome = fake.name()
        email = fake.unique.email()

        telefone = f"+55{random.randint(11111111111, 99999999999)}"
        status = random.choice(status_opcoes)
        data_criacao = str(datetime.now())

        lote_de_dados.append((nome, email, telefone, status, data_criacao))
    print(f"{quantidade} leads gerados. Abrindo o cofre do banco de dados...")

    with sqlite3.connect("leads.db") as con:
        cur = con.cursor()
        # O IGNORE é o seu escudo contra falhas de integridade em massa
        sql = """
        INSERT OR IGNORE INTO leads(name, email, phone, status, created_at)
        VALUES (?, ?, ?, ?, ?)
        """
        
        # O golpe de mestre: executemany dispara a lista inteira de uma vez
        cur.executemany(sql, lote_de_dados)
        linhas_injetadas = cur.rowcount
        
    print(f"{linhas_injetadas} leads foram injetados com sucesso.")

if __name__  == "__main__":
    seedbomb()