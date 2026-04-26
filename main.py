from fastapi import FastAPI
import pytds

app = FastAPI()

server = "forcon-sql-server-demo.database.windows.net"
database = "free-sql-db-1455719"
username = "forconadmin"
password = "Forcon@2026!"

# =========================
# CONEXÃO AZURE SQL (CORRIGIDA)
# =========================
def get_conn():
    return pytds.connect(
        server,
        database,
        user=username,
        password=password,
        encrypt=True,
        validate_host=False
    )

# =========================
# API CONSULTA PEDIDO
# =========================
@app.get("/pedido/{codigo_tracking}")
def get_pedido(codigo_tracking: str):
    try:
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("""
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
            WHERE codigo_tracking = %s
        """, (codigo_tracking,))

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

        return {"erro": "não encontrado"}

    except Exception as e:
        return {"erro": str(e)}