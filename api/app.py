import os
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="DataMart Big Data API")

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "db"),
        database=os.getenv("POSTGRES_DB", "datamart"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres_pass_123"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )

class RegistroItem(BaseModel):
    categoria: str
    mes: str
    ingreso_total: float

@app.get("/resultados")
def get_resultados():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, categoria, mes, ingreso_total FROM resultados;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "categoria": r[1], "mes": r[2], "ingreso_total": float(r[3])} for r in rows]

@app.get("/resultados/{clave}")
def get_resultado_by_clave(clave: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, categoria, mes, ingreso_total FROM resultados WHERE LOWER(categoria) = LOWER(%s);", (clave,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return [{"id": r[0], "categoria": r[1], "mes": r[2], "ingreso_total": float(r[3])} for r in rows]

@app.post("/resultados", status_code=201)
def create_resultado(item: RegistroItem):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO resultados (categoria, mes, ingreso_total) VALUES (%s, %s, %s) RETURNING id;",
        (item.categoria, item.mes, item.ingreso_total)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"id": new_id, "message": "Registro agregado correctamente"}