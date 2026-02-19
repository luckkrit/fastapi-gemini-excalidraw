import os
import json
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

# System prompt to force Gemini to output perfect Excalidraw JSON
SYSTEM_PROMPT = """
You are an Excalidraw expert. Convert the user's text into an array of Excalidraw JSON elements.
Rules:
1. Return ONLY the valid JSON array of elements. No markdown backticks.
2. Include basic shapes: 'rectangle', 'ellipse', 'arrow', or 'text'.
3. Set logical x, y coordinates and sizes. 
Example element: {"type": "rectangle", "x": 100, "y": 100, "width": 100, "height": 50, "strokeColor": "#000000"}
"""


# Load your API key from a .env file
load_dotenv()
GEMINI_MODEL=os.getenv('GEMINI_MODEL')
app = FastAPI(title="Gemini AI Service")

# Initialize the Gemini Client
# It will automatically look for the GEMINI_API_KEY environment variable
client = genai.Client()

# Define the request body structure
class Query(BaseModel):
    prompt: str

@app.get("/", response_class=HTMLResponse)
async def index():
    # Serves the frontend (code in section 3 below)
    with open("index.html", "r") as f:
        return f.read()

@app.post("/generate_text")
async def generate_text(query: Query):
    try:
        # We use client.aio for asynchronous calls in FastAPI
        response = await client.aio.models.generate_content(
            model=GEMINI_MODEL,
            contents=query.prompt
        )
        return {"response": response.text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/generate_excalidraw")
async def generate_diagram(prompt: str = Form(...)):
    try:
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash",
            config={"system_instruction": SYSTEM_PROMPT},
            contents=prompt
        )
        # Clean the response in case the AI added markdown
        clean_json = response.text.strip().replace("```json", "").replace("```", "")
        elements = json.loads(clean_json)
        return {"elements": elements}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)