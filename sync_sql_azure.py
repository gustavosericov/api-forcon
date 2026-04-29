import pyodbc
import time
from datetime import datetime

# =========================
# SQL SERVER INTERNO
# =========================

sql_conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=10.1.1.4;"
    "DATABASE=FORCON_ESTOQUE;"
    "UID=forcon_powerbi;"
    "PWD=PowerBi2026@#Forcon;"
)

sql_cursor = sql_conn.cursor()

# =========================
# AZURE SQL
# =========================

azure_conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=forcon-sql-server-demo.database.windows.net;"
    "DATABASE=free-sql-db-1455719;"
    "UID=forconadmin;"
    "PWD=Forcon@2026!;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

azure_cursor = azure_conn.cursor()

print("======================================")
print("SYNC SQL → AZURE INICIADO")
print("Chave principal: codigo_tracking")
print("Executando a cada 5 segundos...")
print("======================================")


def sync_data():
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Sincronizando...")

    sql_cursor.execute("""
        SELECT
            codigo_tracking,
            numero_nf,
            numero_pedido,
            cliente,
            cnpj_cliente,
            transportadora,
            tipo_frete,
            numero_coleta,
            data_pedido,
            data_coleta,
            data_saida_forcon,
            data_faturamento,
            status_atual,
            etapa_atual,
            previsao_entrega,
            ultima_atualizacao,
            observacao
        FROM portal_cliente_status_nf
    """)

    rows = sql_cursor.fetchall()

    for row in rows:
        azure_cursor.execute("""
            MERGE portal_cliente_status_nf AS target
            USING (
                SELECT ? AS codigo_tracking
            ) AS source
            ON target.codigo_tracking = source.codigo_tracking

            WHEN MATCHED THEN
                UPDATE SET
                    numero_nf = ?,
                    numero_pedido = ?,
                    cliente = ?,
                    cnpj_cliente = ?,
                    transportadora = ?,
                    tipo_frete = ?,
                    numero_coleta = ?,
                    data_pedido = ?,
                    data_coleta = ?,
                    data_saida_forcon = ?,
                    data_faturamento = ?,
                    status_atual = ?,
                    etapa_atual = ?,
                    previsao_entrega = ?,
                    ultima_atualizacao = ?,
                    observacao = ?

            WHEN NOT MATCHED THEN
                INSERT (
                    codigo_tracking,
                    numero_nf,
                    numero_pedido,
                    cliente,
                    cnpj_cliente,
                    transportadora,
                    tipo_frete,
                    numero_coleta,
                    data_pedido,
                    data_coleta,
                    data_saida_forcon,
                    data_faturamento,
                    status_atual,
                    etapa_atual,
                    previsao_entrega,
                    ultima_atualizacao,
                    observacao
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                );
        """,
            # MATCH
            row.codigo_tracking,

            # UPDATE
            row.numero_nf,
            row.numero_pedido,
            row.cliente,
            row.cnpj_cliente,
            row.transportadora,
            row.tipo_frete,
            row.numero_coleta,
            row.data_pedido,
            row.data_coleta,
            row.data_saida_forcon,
            row.data_faturamento,
            row.status_atual,
            row.etapa_atual,
            row.previsao_entrega,
            row.ultima_atualizacao,
            row.observacao,

            # INSERT
            row.codigo_tracking,
            row.numero_nf,
            row.numero_pedido,
            row.cliente,
            row.cnpj_cliente,
            row.transportadora,
            row.tipo_frete,
            row.numero_coleta,
            row.data_pedido,
            row.data_coleta,
            row.data_saida_forcon,
            row.data_faturamento,
            row.status_atual,
            row.etapa_atual,
            row.previsao_entrega,
            row.ultima_atualizacao,
            row.observacao
        )

    azure_conn.commit()
    print(f"{len(rows)} registros sincronizados com sucesso.")


while True:
    try:
        sync_data()
    except Exception as e:
        print(f"Erro durante sync: {e}")

    time.sleep(5)