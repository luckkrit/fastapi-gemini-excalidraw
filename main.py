import os
import json
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from dotenv import load_dotenv
from gemini_excalidraw import gemini_to_excalidraw_no_mcp


app = FastAPI(title="Gemini AI Service")

# Initialize the Gemini Client
# It will automatically look for the GEMINI_API_KEY environment variable
# client = genai.Client()

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
    
@app.post("/generate_excalidraw")
async def generate_diagram(prompt: str = Form(...)):
    # try:
    #     response = await client.aio.models.generate_content(
    #         model="gemini-2.0-flash",
    #         config={"system_instruction": SYSTEM_PROMPT},
    #         contents=prompt
    #     )
    #     # Clean the response in case the AI added markdown
    #     clean_json = response.text.strip().replace("```json", "").replace("```", "")
    #     elements = json.loads(clean_json)
    #     return {"elements": elements}
    # except Exception as e:
    #     # return {"error": str(e)}
    #     print("============= error "+str(e)+" ==============")
    #     elements = mock_elements()
    #     return {"elements": elements}
    diagram_type = gemini_to_excalidraw_no_mcp.detect_diagram_type(prompt) 
    system_prompt = gemini_to_excalidraw_no_mcp.get_system_prompt(diagram_type)
    return await gemini_to_excalidraw_no_mcp.generate_diagram(prompt,system_prompt)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)