from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def run_inference():
    output = subprocess.check_output(["python", "inference.py"]).decode()
    return {"result": output}
