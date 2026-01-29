@app.get("/")
async def root():
    return {"mensagem": "API de Vendas está Online!", "docs": "/docs"}
