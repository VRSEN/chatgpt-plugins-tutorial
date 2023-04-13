import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from typing import Any
from pydantic import BaseModel
import json

# additional packages
from openai.embeddings_utils import get_embedding
import openai
import pinecone

pinecone.init(api_key=os.environ["PINECONE_API_KEY"],
              environment=os.environ["PINECONE_ENVIRONMENT"]
              )
index = pinecone.Index("huberman-podcast-1")

openai.api_key = os.environ["OPENAI_API_KEY"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    text: str


@app.post("/query", summary="Search for any health related information within the podcast episodes of Andrew Huberman's podcast.")
async def query(query: Query) -> Any:
    text = query.text
    embedding = get_embedding(text, engine='text-embedding-ada-002')

    res = index.query([embedding], top_k=10, include_metadata=True)

    i = 0
    chosen_docs = []
    tokens = 0
    while tokens < 800 and len(res['matches']) > i:
        match = res['matches'][i]
        if int(match['metadata']['tokens']) + tokens > 800:
            break
        chosen_docs.append({
            'content': match['metadata']['content'],
            'episode': match['metadata']['episode'],
        })
        tokens += int(match['metadata']['tokens'])

    return chosen_docs


@app.get("/image")
async def image():
    image_path = os.path.join(os.path.dirname(__file__), "./huberman_lab_podcast_image.jpeg")
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)


@app.get("/.well-known/ai-plugin.json", include_in_schema=False)
async def ai_plugin_json():
    json_path = os.path.join(os.path.dirname(__file__), "ai-plugin.json")
    if not os.path.exists(json_path):
        raise HTTPException(status_code=404, detail="ai-plugin.json not found")
    with open(json_path, "r") as json_file:
        data = json.load(json_file)
    return JSONResponse(content=data)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
