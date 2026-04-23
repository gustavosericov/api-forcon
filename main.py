from fastapi import FastAPI

app = FastAPI()

@app.get("/pedido/{nf}")
def get_pedido(nf: int):
    return {
        "numero_nf": nf,
        "cliente": "Cliente Exemplo",
        "status": "Pedido registrado"
    }