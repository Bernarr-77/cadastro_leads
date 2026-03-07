import sqlite3
import time

def testar_performance():
    con = sqlite3.connect("leads.db")
    cur = con.cursor()

    print("Iniciando 1.000 buscas completas no banco de dados...")
    
    # Marca o tempo inicial no relógio do processador
    inicio = time.time()
    
    # Fazemos o banco procurar um nome que nem existe 1.000 vezes seguidas
    for _ in range(1000):
        cur.execute("SELECT * FROM leads WHERE name = 'Bernardo Inexistente'")
        cur.fetchall()
        
    # Marca o tempo final
    fim = time.time()
    
    tempo_total = fim - inicio
    print(f"Tempo gasto: {tempo_total:.5f} segundos")

if __name__ == "__main__":
    testar_performance()