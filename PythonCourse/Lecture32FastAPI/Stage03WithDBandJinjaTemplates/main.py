from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from database import items_ref
from models import Item

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    docs = items_ref.stream()
    items = [{"id": d.id, **d.to_dict()} for d in docs]
    return templates.TemplateResponse("index.html", {"request": request, "items": items})

@app.get("/add")
def add_form(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})

@app.post("/add")
def add_item(name: str = Form(...), description: str = Form(None), price: float = Form(...)):
    item = Item(name=name, description=description, price=price)
    doc_ref = items_ref.document()
    doc_ref.set(item.dict())
    return RedirectResponse("/", status_code=303)

@app.get("/edit/{item_id}")
def edit_form(request: Request, item_id: str):
    doc = items_ref.document(item_id).get()
    if not doc.exists:
        return RedirectResponse("/", status_code=303)
    item = {"id": doc.id, **doc.to_dict()}
    return templates.TemplateResponse("edit.html", {"request": request, "item": item})

@app.post("/edit/{item_id}")
def edit_item(item_id: str, name: str = Form(...), description: str = Form(None), price: float = Form(...)):
    items_ref.document(item_id).update({"name": name, "description": description, "price": price})
    return RedirectResponse("/", status_code=303)

@app.get("/delete/{item_id}")
def delete_item(item_id: str):
    items_ref.document(item_id).delete()
    return RedirectResponse("/", status_code=303)
