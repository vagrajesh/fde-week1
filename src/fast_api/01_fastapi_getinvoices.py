from fastapi import FastAPI

app = FastAPI()

invoices =[{"id": 1, "amount": 100.0, "status": "paid"},
           {"id": 2, "amount": 200.0, "status": "unpaid"}]

@app.get("/invoices")
def get_invoices():
    return {"invoices": invoices}

@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: int):
    for invoice in invoices:
        if invoice["id"] == invoice_id:
            return {"invoice": invoice}
    return {"error": "Invoice not found"}