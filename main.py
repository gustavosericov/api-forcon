from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()

server = "forcon-sql-server-demo.database.windows.net"
database = "free-sql-db-1455719"
username = "forconadmin"
password = "Forcon@2026!"

# 🔥 DRIVER ZERO ODBC (USANDO PYTDDS VIA SQLALCHEMY)
connection_string = (
    f"mssql+pymssql://{username}:{password}@{server}/{database}"
)

engine = create_engine(connection_string)


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

        return {"erro": "não encontrado"}

    except Exception as e:
        return {"erro": str(e)}