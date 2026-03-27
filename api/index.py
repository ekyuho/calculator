from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>Calculator</title>
</head>
<body>
  <h2>Calculator</h2>
  <form id="calcForm">
    <input type="number" id="a" placeholder="숫자 1" required>
    <select id="op">
      <option value="add">+</option>
      <option value="sub">-</option>
      <option value="mul">×</option>
      <option value="div">÷</option>
    </select>
    <input type="number" id="b" placeholder="숫자 2" required>
    <button type="submit">계산</button>
  </form>
  <p id="result"></p>
  <script>
    document.getElementById("calcForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const a = document.getElementById("a").value;
      const b = document.getElementById("b").value;
      const op = document.getElementById("op").value;
      const res = await fetch(`/api/calc?a=${a}&b=${b}&op=${op}`);
      const data = await res.json();
      document.getElementById("result").textContent =
        data.error ? `오류: ${data.error}` : `결과: ${data.result}`;
    });
  </script>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
def index():
    return HTML

@app.get("/api/calc")
def calc(a: float = Query(...), b: float = Query(...), op: str = Query("add")):
    ops = {
        "add": a + b,
        "sub": a - b,
        "mul": a * b,
        "div": a / b if b != 0 else None,
    }
    if op not in ops:
        return {"error": "invalid operator"}
    if ops[op] is None:
        return {"error": "division by zero"}
    return {"result": ops[op]}
