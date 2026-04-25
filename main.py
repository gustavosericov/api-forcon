from fastapi import FastAPI
import pyodbc

app = FastAPI()

# Configuração de conexão com SQL Server
server = '10.1.1.4\\forcon'
database = 'FORCON_ESTOQUE'
username = 'forcon_admin'
password = 'Admin2026@#Forcon'

connection_string = f"""
DRIVER={{ODBC Driver 17 for SQL Server}};
SERVER={server};
DATABASE={database};
UID={username};
PWD={password};
TrustServerCertificate=yes;
"""

@app.get("/pedido/{nf}")
def get_pedido(nf: int):
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        query = """
            SELECT numero_nf, cliente, status
            FROM controle_nf_demo
            WHERE numero_nf = ?
        """

        cursor.execute(query, (nf,))
        row = cursor.fetchone()

        conn.close()

        if row:
            return {
                "numero_nf": row.numero_nf,
                "cliente": row.cliente,
                "status": row.status
            }
        else:
            return {
                "numero_nf": nf,
                "cliente": "Não encontrado",
                "status": "NF não localizada"
            }

    except Exception as e:
        return {
            "erro": str(e)
        }