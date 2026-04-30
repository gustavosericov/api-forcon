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
# HELPERS (BLINDADO)
# =========================

def clean(value):
    if value is None:
        return ""
    if str(value).strip().lower() in ["none", "null", ""]:
        return ""
    return value


def safe_date(value):
    if value is None:
        return ""

    try:
        if isinstance(value, datetime):
            return value.strftime("%d/%m/%Y")

        val = str(value).strip()

        if val.lower() in ["none", "null", ""]:
            return ""

        for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(val, fmt).strftime("%d/%m/%Y")
            except:
                pass

        return val[:10] if len(val) >= 10 else val

    except:
        return ""


def format_datetime(value):
    if value is None:
        return ""

    try:
        if isinstance(value, datetime):
            dt = value
        else:
            dt = datetime.fromisoformat(str(value))
    except:
        return ""

    return dt.strftime("%d/%m/%Y - %H:%Mhs")

# =========================
# API
# =========================

@app.get("/pedido/{codigo_tracking}")
def get_pedido(codigo_tracking: str):
    try:
        conn = get_conn()
        cursor = conn.cursor(as_dict=True)  # 🔥 CORREÇÃO PRINCIPAL

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

        if not row:
            return {"erro": "não encontrado"}

        return {
            "codigo_tracking": clean(row["codigo_tracking"]),
            "numero_nf": clean(row["numero_nf"]),
            "numero_pedido": clean(row["numero_pedido"]),
            "cliente": clean(row["cliente"]),
            "transportadora": clean(row["transportadora"]),
            "status_atual": clean(row["status_atual"]),
            "etapa_atual": clean(row["etapa_atual"]),
            "observacao": clean(row["observacao"]),
            "numero_coleta": clean(row["numero_coleta"]),

            # 🔥 DATAS 100% SEGURAS
            "data_pedido": safe_date(row["data_pedido"]),
            "data_coleta": safe_date(row["data_coleta"]),
            "data_saida_forcon": safe_date(row["data_saida_forcon"]),
            "data_faturamento": safe_date(row["data_faturamento"]),
            "previsao_entrega": safe_date(row["previsao_entrega"]),

            "ultima_atualizacao": format_datetime(row["ultima_atualizacao"])
        }

    except Exception as e:
        return {"erro": str(e)}