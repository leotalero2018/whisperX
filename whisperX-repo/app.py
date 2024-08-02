from fastapi import FastAPI, File, UploadFile, HTTPException
from starlette.responses import FileResponse
from fastapi.responses import JSONResponse
import subprocess
import os
import shutil
import uvicorn
import multipart
from zipfile import ZipFile

app = FastAPI()


@app.get('/health')
async def health():
    print("-------------- OK --------------------")
    return {"status": "ok"}


@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...), language: str = 'en', compute_type: str = None):
    output_dir = "output-whisperx"

    temp_path = f"temp_{file.filename}"

    # Save temporary audio file
    with open(temp_path, "wb") as audio_file:
        content = await file.read()
        audio_file.write(content)

    zip_path = f"{output_dir}.zip"

    try:
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Construct the command for whisperx
        command = ['whisperx', '--language', language, '--output_dir', output_dir, temp_path]
        if compute_type:
            command.extend(['--compute_type', compute_type])

        print("COMMAND", command)
        # Call whisperx with the saved audio file and additional parameters
        result = subprocess.run(command, capture_output=True, text=True)

        # Check for errors in subprocess
        if result.returncode != 0:
            raise Exception(result.stderr)

        # Zip the output directory
        with ZipFile(zip_path, 'w') as zipf:
            for root, _, files in os.walk(output_dir):
                for file in files:
                    zipf.write(os.path.join(root, file),
                               os.path.relpath(os.path.join(root, file), os.path.join(output_dir, '..')))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Clean up temporary files
        os.remove(temp_path)
        shutil.rmtree(output_dir)

    return FileResponse(zip_path, media_type='application/zip', filename=zip_path)


if __name__ == "__main__":
    print("Into FastAPI")
    uvicorn.run(app, host="0.0.0.0", port=9080)
