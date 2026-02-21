import os
import json
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastmcp import Client
from fastmcp.client.transports import NodeStdioTransport
from dotenv import load_dotenv
from google.genai import types
from google import genai
# from gemini_excalidraw import gemini_to_excalidraw_no_mcp

transport = NodeStdioTransport("/home/codespace/nvm/current/bin/npx", ["-y", "@iflow-mcp/mcp-mermaid"])
mcp_client = Client(transport)
app = FastAPI(title="Gemini AI Service")

# Initialize the Gemini Client
# It will automatically look for the GEMINI_API_KEY environment variable
load_dotenv()
GEMINI_MODEL=os.getenv('GEMINI_MODEL3')
client = genai.Client()

# Define the request body structure
class Query(BaseModel):
    prompt: str

@app.get("/", response_class=HTMLResponse)
async def index():
    # Serves the frontend (code in section 3 below)
    with open("index.html", "r") as f:
        return f.read()

# @app.post("/generate_text")
# async def generate_text(query: Query):
#     try:
#         # We use client.aio for asynchronous calls in FastAPI
#         response = await client.aio.models.generate_content(
#             model=GEMINI_MODEL,
#             contents=query.prompt
#         )
#         return {"response": response.text}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.get("/generate_text", response_class=HTMLResponse)    
async def create_diagram():
    async with mcp_client:
        # Gemini will see the tools provided by the mermaid_mcp session
        # (e.g., 'render_mermaid', 'save_diagram')
        # response = await client.aio.models.generate_content(
        #     model="gemini-2.0-flash",
        #     contents="Create a high-level flowchart of a user ordering coffee and render it.",
        #     config=types.GenerateContentConfig(
        #         tools=[mermaid_mcp.session], # Connects the "Tool" to Gemini
        #         temperature=0.1
        #     ),
        # )
        try:

            response = await client.aio.models.generate_content(
                model=GEMINI_MODEL,
                contents="Create a high-level flowchart of a user ordering coffee and render it.",
                config=types.GenerateContentConfig(
                    tools=[mermaid_mcp.session], # Connects the "Tool" to Gemini
                    temperature=0.1
                ),
            )
            return response.text
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        # Gemini executes the tool call automatically. 
        # The response will contain the result of the rendering.
        # print(f"Gemini Response: {response.text}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)