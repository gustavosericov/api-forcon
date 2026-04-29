import pyodbc

# =========================
# CONEXÃO FORCON (ORIGEM)
# =========================
conn_forcon = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=10.1.1.4\\forcon;'
    'DATABASE=FORCON_ESTOQUE;'
    'UID=forcon_admin;'
    'PWD=Admin2026@#Forcon'
)

cursor_forcon = conn_forcon.cursor()

cursor_forcon.execute("""
    SELECT TOP 5
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
        observacao
    FROM portal_cliente_status_nf
""")

rows = cursor_forcon.fetchall()

# =========================
# CONEXÃO AZURE
# =========================
conn_azure = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=forcon-sql-server-demo.database.windows.net;'
    'DATABASE=free-sql-db-1455719;'
    'UID=forconadmin;'
    'PWD=Forcon@2026!;'
    'Encrypt=yes;'
    'TrustServerCertificate=yes;'
)

cursor_azure = conn_azure.cursor()

print("🔥 ENVIANDO PARA AZURE (VERSÃO FINAL CORRIGIDA) 🔥")

# =========================
# INSERT CORRETO
# =========================
for row in rows:
    cursor_azure.execute("""
        INSERT INTO portal_cliente_status_nf (
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
            observacao,
            ultima_atualizacao
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE())
    """,
    row[0],
    row[1],
    row[2],
    row[3],
    row[4],
    row[5],
    row[6],
    row[7],
    row[8],
    row[9],
    row[10],
    row[11],
    row[12],
    row[13],
    row[14],
    row[15]
    )

conn_azure.commit()

print("✅ ESPÉLHO FINAL CONCLUÍDO COM SUCESSO")