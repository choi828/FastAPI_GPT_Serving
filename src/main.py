# app/main.py
from fastapi import FastAPI, HTTPException
from src.schemas import EntityLinkingRequest, EntityLinkingResponse
from src.entity_linker import main as process_text
from src.neo4j_connector import neo4j_connector

app = FastAPI()

@app.post("/entity_linking", response_model=EntityLinkingResponse)
async def entity_linking(request: EntityLinkingRequest):
    try:
        results = process_text(request.text)
        mentions = {result['Entity']: [{
            "Question": result["Question"],
            "Disambiguated ID": result["Disambiguated ID"]
        }] for result in results}
        return EntityLinkingResponse(mentions=mentions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

