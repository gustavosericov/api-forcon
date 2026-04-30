from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pymssql
from datetime import datetime

app = FastAPI()

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# CONEXÃO
# =========================

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

# =========================
# HELPERS
# =========================

def clean(value):
    if value is None:
        return ""
    if str(value).lower() in ["none", "null", ""]:
        return ""
    return value

def parse_datetime(value):
    if not value:
        return None

    if isinstance(value, datetime):
        return value

    val = str(value).strip()

    if val.lower() in ["none", "null", ""]:
        return None

    try:
        return datetime.strptime(val, "%Y-%m-%d %H:%M:%S.%f")
    except:
        try:
            return datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
        except:
            try:
                return datetime.fromisoformat(val)
            except:
                return None

def format_date(value):
    dt = parse_datetime(value)
    if not dt:
        return ""
    return dt.strftime("%d/%m/%Y")

def format_datetime(value):
    dt = parse_datetime(value)
    if not dt:
        return ""
    return dt.strftime("%d/%m/%Y - %H:%Mhs")

# =========================
# API
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
                "codigo_tracking": clean(row[0]),
                "numero_nf": clean(row[1]),
                "numero_pedido": clean(row[2]),
                "cliente": clean(row[3]),
                "transportadora": clean(row[4]),
                "status_atual": clean(row[5]),
                "etapa_atual": clean(row[6]),
                "observacao": clean(row[7]),
                "numero_coleta": clean(row[8]),

                "data_pedido": format_date(row[9]),
                "data_coleta": format_date(row[10]),
                "data_saida_forcon": format_date(row[11]),
                "data_faturamento": format_date(row[12]),
                "previsao_entrega": format_date(row[13]),

                "ultima_atualizacao": format_datetime(row[14])
            }

        return {"erro": "não encontrado"}

    except Exception as e:
        return {"erro": str(e)}