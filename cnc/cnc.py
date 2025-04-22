from fastapi import FastAPI, Request
from pathlib import Path
import json

app = FastAPI(title="FastAPI Project", version="1.0.0")


@app.get("/api/commands")
def read_root():
    contents = Path("commands.json").read_text()
    response = json.loads(contents)
    return response


@app.post("/api/commands_output")
async def output(request: Request):
    commands_output = await request.json()  # Read raw JSON from the request
    Path("output.json").write_text(json.dumps(commands_output, indent=4))
    return {"message": "Output saved successfully"}
