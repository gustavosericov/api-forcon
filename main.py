from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()

server = "forcon-sql-server-demo.database.windows.net"
database = "free-sql-db-1455719"
username = "forconadmin"
password = "Forcon@2026!"

connection_string = (
    "mssql+pyodbc://{user}:{pwd}@{host}/{db}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&encrypt=yes"
    "&trustServerCertificate=yes"
).format(
    user=username,
    pwd=password,
    host=server,
    db=database
)

engine = create_engine(connection_string)

@app.get("/pedido/{codigo_tracking}")
def get_pedido(codigo_tracking: str):
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
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
            """), {"codigo": codigo_tracking})

            row = result.fetchone()

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