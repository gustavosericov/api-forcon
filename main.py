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
# HELPERS (FINAL ROBUSTO)
# =========================

def clean(value):
    if value is None:
        return ""
    if str(value).strip().lower() in ["none", "null", ""]:
        return ""
    return value

def parse_datetime(value):
    if value is None:
        return None

    if isinstance(value, datetime):
        return value

    val = str(value).strip()

    if val.lower() in ["none", "null", ""]:
        return None

    # formatos SQL Server mais comuns
    formats = [
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d"
    ]

    for f in formats:
        try:
            return datetime.strptime(val, f)
        except:
            continue

    # fallback ISO seguro
    try:
        return datetime.fromisoformat(val)
    except:
        return None

def format_date(value):
    dt = parse_datetime(value)
    if dt is None:
        return ""
    return dt.strftime("%d/%m/%Y")

def format_datetime(value):
    dt = parse_datetime(value)
    if dt is None:
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
	print("ROW DEBUG:", row)
        conn.close()

        if not row:
            return {"erro": "não encontrado"}

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

            "data_pedido": row[9].strftime("%d/%m/%Y") if row[9] else "",
"data_coleta": row[10].strftime("%d/%m/%Y") if row[10] else "",
"data_saida_forcon": row[11].strftime("%d/%m/%Y") if row[11] else "",
"data_faturamento": row[12].strftime("%d/%m/%Y") if row[12] else "",
"previsao_entrega": row[13].strftime("%d/%m/%Y") if row[13] else "",

"ultima_atualizacao": format_datetime(row[14])
        }

    except Exception as e:
        return {"erro": str(e)}