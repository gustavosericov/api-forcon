from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()

# =========================
# CONEXÃO AZURE SQL (CLOUD SAFE)
# =========================

server = "forcon-sql-server-demo.database.windows.net"
database = "free-sql-db-1455719"
username = "forconadmin"
password = "Forcon@2026!"

connection_string = (
    "mssql+pyodbc://"
    f"{username}:{password}@{server}/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

engine = create_engine(connection_string)


# =========================
# API CONSULTA PEDIDO
# =========================

@app.get("/pedido/{codigo_tracking}")
def get_pedido(codigo_tracking: str):
    try:
        query = text("""
            SELECT TOP 1
                codigo_tracking,
                numero_nf,
                numero_pedido,
                cliente,
                transportadora,
                status_atual,
                etapa_atual,
                observacao
            FROM portal_cliente_status_nf
            WHERE codigo_tracking = :codigo
        """)

        with engine.connect() as conn:
            result = conn.execute(query, {"codigo": codigo_tracking}).fetchone()

        if result:
            return {
                "codigo_tracking": result[0],
                "numero_nf": result[1],
                "numero_pedido": result[2],
                "cliente": result[3],
                "transportadora": result[4],
                "status_atual": result[5],
                "etapa_atual": result[6],
                "observacao": result[7]
            }

        return {
            "codigo_tracking": codigo_tracking,
            "status": "não encontrado"
        }

    except Exception as e:
        return {
            "erro": str(e)
        }