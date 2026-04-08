from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Adaptive Shortlisting Env is running"}

@app.get("/run")
def run_inference():
    try:
        result = subprocess.run(
            ["python3", "inference.py"],
            capture_output=True,
            text=True,
            timeout=60
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        return {"error": str(e)}
