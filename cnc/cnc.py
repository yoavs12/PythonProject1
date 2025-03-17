import fastapi
from fastapi.responses import PlainTextResponse
from fastapi import UploadFile, File
from pathlib import Path
import datetime

SCREENSHOT_PATH = "./collected_files/"
app = fastapi.FastAPI()

@app.post("/")
async def root(file: UploadFile = File(...)):
    contents = await file.read()
    print(contents.decode())
    return PlainTextResponse(contents.decode("utf-8"))

@app.post("/screenshot")
async def receive_screenshot(screenshot_sent: UploadFile = File(...)):
    file_name = screenshot_sent.filename
    file_content = await screenshot_sent.read()

    saved_file = Path(SCREENSHOT_PATH + file_name)
    saved_file.open("w")
    saved_file.write_bytes(file_content)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
