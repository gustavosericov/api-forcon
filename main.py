from fastapi import FastAPI
import pymssql

app = FastAPI()

server = "forcon-sql-server-demo.database.windows.net"
database = "free-sql-db-1455719"
username = "forconadmin"
password = "Forcon@2026!"

def get_conn():
    return pymssql.connect(
        server=server,
        user=username,
        password=password,
        database=database
    )

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
                observacao,
                numero_coleta,
                data_pedido,
                data_coleta,
                data_saida_forcon,
                data_faturamento,
                previsao_entrega,
                ultima_atualizacao
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
                "observacao": row[7],

                "numero_coleta": row[8],
                "data_pedido": row[9],
                "data_coleta": row[10],
                "data_saida_forcon": row[11],
                "data_faturamento": row[12],
                "previsao_entrega": row[13],
                "ultima_atualizacao": row[14]
            }

        return {"erro": "não encontrado"}

    except Exception as e:
        return {"erro": str(e)}