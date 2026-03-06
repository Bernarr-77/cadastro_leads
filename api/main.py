from fastapi import FastAPI, HTTPException
from schemas import LeadInput, LeadsProcess
from database import save_lead, get_lead_id,get_lead_email
import sqlite3
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional

app = FastAPI()

@app.post("/leads")
def post_leads(payload: LeadInput):

    lead_complete = LeadsProcess(**payload.model_dump())
    data_for_save = lead_complete.model_dump(exclude={"id"}, mode="json")
    try:
        save_lead(**data_for_save)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail= "Email ou telefone ja estão cadastrados no sistema, tente novamente")
    except Exception as error_500:
        raise HTTPException(status_code=500, detail= f"Erro desconhecido: {str(error_500)}")
    return{"Message": "Criado com sucesso", "dados": lead_complete}

@app.get("/leads/search")
def get_clients_mail(Lead_mail: Optional[EmailStr] = None, lead_phone: Optional[PhoneNumber] = None):

    if Lead_mail is None and lead_phone is None:
        raise HTTPException(status_code=400, detail= "Você precisa mandar pelo menos um dado para fazer a busca ")
    try:
        get_leads = get_lead_email(Lead_mail, lead_phone)

    except Exception as error_500:
        raise HTTPException(status_code=500, detail= f"Erro desconhecido: {str(error_500)}")
    
    if get_leads is None:
        raise HTTPException(status_code=400, detail= "Não existe ninguem com esse email ou telefone ")
    return {"Message": "Encontrado com sucesso!", "dados": get_leads}

@app.get("/leads/{lead_id}")
def get_clients_id(lead_id: int):
    try:
        lead_get = get_lead_id(lead_id)
    except Exception as error_500:
        raise HTTPException(status_code=500, detail= f"Erro desconhecido: {str(error_500)}")
    
    if lead_get is None:
        raise HTTPException(status_code=404, detail= "Não existe ninguem com esse ID")

    return {"Message": "Encontrado com sucesso!", "dados": lead_get}

