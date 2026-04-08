from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import subprocess

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def run_inference():
    output = subprocess.check_output(["python", "inference.py"]).decode()

    return f"""
    <html>
        <head>
            <title>Adaptive Shortlisting Env</title>
        </head>
        <body style="font-family: monospace; background-color: #0f172a; color: #e2e8f0; padding: 20px;">
            <h1>🚀 Adaptive Shortlisting Environment</h1>
            <pre>{output}</pre>
        </body>
    </html>
    """
