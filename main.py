from fastapi import FastAPI
import pymssql

app = FastAPI()

server = "10.1.1.4\\forcon"
database = "FORCON_ESTOQUE"
username = "forcon_admin"
password = "Admin2026@#Forcon"

@app.get("/pedido/{nf}")
def get_pedido(nf: int):
    try:
        conn = pymssql.connect(
            server=server,
            user=username,
            password=password,
            database=database
        )

        cursor = conn.cursor(as_dict=True)

        query = """
            SELECT numero_nf, cliente, status
            FROM controle_nf_demo
            WHERE numero_nf = %s
        """

        cursor.execute(query, (nf,))
        row = cursor.fetchone()

        conn.close()

        if row:
            return {
                "numero_nf": row["numero_nf"],
                "cliente": row["cliente"],
                "status": row["status"]
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