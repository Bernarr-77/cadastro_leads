from fastapi import FastAPI
from schemas import LeadInput, LeadsProcess
from database import start_bank,save_lead

app = FastAPI()

@app.post("/leads")
def post_leads(payload: LeadInput):

    lead_complete = LeadsProcess(**payload.model_dump())
    data_for_save = lead_complete.model_dump(exclude={"id"}, mode="json")
    save_lead(**data_for_save)

    return{"Mensage": "Criado com sucesso", "dados": lead_complete}
