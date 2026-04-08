from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import subprocess
import json

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Adaptive Shortlisting Env</title>
    </head>
    <body style="font-family:sans-serif; background:#0f172a; color:#e2e8f0; padding:20px;">
        <h1>🚀 Adaptive Shortlisting Environment</h1>

        <form action="/run" method="post">
            <label>Select Difficulty:</label>
            <select name="difficulty">
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
            </select>
            <br><br>
            <button type="submit">Run Simulation</button>
        </form>
    </body>
    </html>
    """


@app.post("/run", response_class=HTMLResponse)
async def run(request: Request):
    form = await request.form()
    difficulty = form.get("difficulty")

    output = subprocess.check_output(
        ["python", "inference.py", difficulty]
    ).decode()

    data = json.loads(output)

    steps_html = ""
    for i, step in enumerate(data["steps"], start=1):
        # Color coding
        if step["reward"] > 0.8:
            color = "#16a34a"  # green
        elif step["reward"] > 0.5:
            color = "#eab308"  # yellow
        else:
            color = "#ef4444"  # red

        steps_html += f"""
        <div style="background:#1e293b; padding:15px; margin:10px 0; border-radius:10px; border-left:5px solid {color};">
            <h3>🔹 Step {i}</h3>
            <p><b>Candidate:</b> {step['action']}</p>
            <p>📉 Reduction: {step['reward'] * 100:.1f}%</p>
            <p>👥 Remaining: {step['remaining']}</p>
        </div>
        """

    return f"""
    <html>
    <body style="font-family:sans-serif; background:#0f172a; color:#e2e8f0; padding:20px;">
        <h1>🚀 Adaptive Shortlisting</h1>
        <h2>Task: {data['task']}</h2>

        {steps_html}

        <h2>🏁 Final Score: {data['score']}</h2>

        <br>
        <a href="/" style="color:#38bdf8;">⬅ Run Again</a>
    </body>
    </html>
    """
