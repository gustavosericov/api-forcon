from fastapi import FastAPI
import pyodbc

app = FastAPI()

server = "forcon-sql-server-demo.database.windows.net"
database = "free-sql-db-1455719"
username = "forconadmin"
password = "Forcon@2026!"

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=30;"
    )

@app.get("/pedido/{codigo_tracking}")
def get_pedido(codigo_tracking: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT
                codigo_tracking,
                numero_nf,
                numero_pedido,
                cliente,
                transportadora,
                status_atual,
                etapa_atual,
                observacao
            FROM portal_cliente_status_nf
            WHERE codigo_tracking = ?
        """

        cursor.execute(query, (codigo_tracking,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "codigo_tracking": row[0],
                "numero_nf": row[1],
                "numero_pedido": row[2],
                "cliente": row[3],
                "transportadora": row[4],
                "status_atual": row[5],
                "etapa_atual": row[6],
                "observacao": row[7]
            }
        else:
            return {
                "codigo_tracking": codigo_tracking,
                "status": "não encontrado"
            }

    except Exception as e:
        return {"erro": str(e)}