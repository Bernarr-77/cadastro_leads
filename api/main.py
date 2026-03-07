from fastapi import FastAPI, HTTPException
from schemas import LeadInput, LeadsProcess,LeadUpdate
from database import save_lead,get_lead_email,delete_lead_id, update_lead,get_lead_id
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
def get_clients_mail(lead_mail: Optional[EmailStr] = None, lead_phone: Optional[PhoneNumber] = None, 
                     lead_name: Optional[str] = None, lead_id:Optional[int] = None):

    if lead_mail is None and lead_phone is None and lead_name is None and lead_id is None:
        raise HTTPException(status_code=400, detail= "Você precisa mandar pelo menos um dado para fazer a busca ")
    try:
        get_leads = get_lead_email(lead_mail, lead_phone, lead_name,lead_id)

    except Exception as error_500:
        raise HTTPException(status_code=500, detail= f"Erro desconhecido: {str(error_500)}")
    
    if get_leads is None:
        raise HTTPException(status_code=400, detail= "Não existe ninguem com esse email ou telefone ")
    return {"Message": "Encontrado com sucesso!", "dados": get_leads}


@app.delete("/leads/{lead_id}")
def del_clients(lead_id: int):
    try:
        lines = delete_lead_id(lead_id)
    except Exception as error_500:
        raise HTTPException(status_code=500, detail= f"Erro desconhecido: {str(error_500)}")
    if lines == 0:
        raise HTTPException(status_code=404, detail= "Não existe ninguém com esse ID.")
    return {"Message": f"Lead com ID {lead_id} foi deletado do sistema."}

@app.patch("/leads/{lead_id}")
def update_lead_id(lead_id: int, payload: LeadUpdate):

    get_client = get_lead_id(lead_id)
    if get_client is None:
        raise HTTPException(status_code=404, detail= "Não existe ninguem com esse ID")
    
    new_data = payload.model_dump(exclude_unset=True)

    if not new_data:
        return {"message": "Nenhum dado enviado para atualização.", "dados": new_data}
    
    get_client.update(new_data)

    try:
        update_lead(
            lead_id= lead_id,
            name= get_client["name"],
            email= get_client["email"],
            phone= get_client["phone"],
            status= get_client["status"]
        )
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Este e-mail ou telefone já está em uso por outro lead.")
    except Exception as error_500:
        raise HTTPException(status_code=500, detail= f"Erro desconhecido: {str(error_500)}")
    
    return {"message": "Atualizado com sucesso", "dados": get_client}


        
