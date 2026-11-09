import os
import psycopg2
import time

DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "datamart")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres_pass_123")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

def conectar():
    for _ in range(10):
        try:
            conn = psycopg2.connect(
                host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
            )
            return conn
        except psycopg2.OperationalError:
            time.sleep(2)
    raise Exception("No se pudo conectar a la base de datos")

def cargar():
    conn = conectar()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS resultados (
            id SERIAL PRIMARY KEY,
            categoria VARCHAR(100),
            mes VARCHAR(10),
            ingreso_total NUMERIC(15, 2)
        );
    """)
    cur.execute("TRUNCATE TABLE resultados;")

    file_path = "/data/output/part-00000"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) == 3:
                    cat, mes, ingreso = parts[0], parts[1], float(parts[2])
                    cur.execute(
                        "INSERT INTO resultados (categoria, mes, ingreso_total) VALUES (%s, %s, %s)",
                        (cat, mes, ingreso)
                    )
        conn.commit()
        print("Carga finalizada con éxito.")
    else:
        print(f"Archivo {file_path} no encontrado.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    cargar()