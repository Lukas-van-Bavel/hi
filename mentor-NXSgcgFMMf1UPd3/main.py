# app.py
from flask import Flask, request, session, jsonify, render_template_string
import io
import contextlib
import os

app = Flask(__name__)
app.secret_key = "geheim123"

def mijn_script(get_input, output):
    output("Voer de geheime code in om verder te gaan:")
    code = '1234'
    while True:
        code_in = get_input("input_code")
        if code_in == 'BT':
            return "Beëindigd."
        if code_in == code:
            break

    output("Dat is de correcte code!")
    leeftijd = 14

    while True:
        output(f"\nMijn naam is Lukas van Bavel en ik ben {leeftijd} jaar oud.")
        output("Zoals je ziet hou ik van dingen maken en dus programmeren.")
        output("Wat wil je weten:")
        output("1. Mijn schoolcarrière")
        output("2. Mijn hobby's")
        output("3. Mijn familie")
        output("Typ 1, 2, 3 of BT om te stoppen")

        keuze = get_input("input_choice")
        if keuze == 'BT':
            return "Beëindigd."
        elif keuze == '1':
            output("Ik zit op het gymnasium en ik hou van wiskunde en informatica.")
        elif keuze == '2':
            output("Mijn hobby's zijn programmeren, gamen en muziek maken.")
        elif keuze == '3':
            output("Ik heb een broer en een zus. Mijn ouders steunen mij in alles wat ik doe.")
        else:
            output("Ongeldige keuze, probeer opnieuw.")

@app.route("/")
def index():
    session.clear()
    html = """
    <html><head>
    <style>
    body { font-family: monospace; padding: 30px; background: white; color: black; }
    body.dark { background: #121212; color: #e0e0e0; }
    #theme-toggle, #stop-button { position: fixed; padding: 6px 10px; font-size: 14px; cursor: pointer; border-radius: 4px; z-index: 1000; }
    #theme-toggle { top: 10px; right: 10px; }
    #stop-button { bottom: 10px; left: 10px; background: red; color: white; border: none; }
    input, button { font-size: 16px; margin-top: 10px; }
    .output-box { white-space: pre-wrap; word-wrap: break-word; margin-bottom: 1em; }
    </style>
    </head><body>
    <button id="theme-toggle">🌗 Thema</button>
    <button id="stop-button">⛔️ Stop</button>
    <div class="output-box" id="output"></div>
    <input id="user_input" autofocus autocomplete="off" placeholder="> typ hier..."/>
    <button onclick="sendInput()">Geef input</button>
    <script>
    if (localStorage.getItem("theme") === "dark") document.body.classList.add("dark");
    document.getElementById("theme-toggle").onclick = () => {
        document.body.classList.toggle("dark");
        localStorage.setItem("theme", document.body.classList.contains("dark") ? "dark" : "light");
    };
    document.getElementById("stop-button").onclick = () => {
        if (confirm("Weet je zeker dat je de pagina wilt sluiten?")) {
            window.open('', '_self'); window.close();
        }
    };
    async function sendInput() {
        const input = document.getElementById("user_input").value;
        const res = await fetch("/api/run", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_input: input })
        });
        const data = await res.json();
        document.getElementById("output").innerText = data.output;
        document.getElementById("user_input").value = "";
    }
    </script>
    </body></html>
    """
    return render_template_string(html)

@app.route("/api/run", methods=["POST"])
def run_api():
    user_input = request.json.get("user_input")
    inputs = session.get("inputs", [])
    output_log = []
    if user_input:
        inputs.append(user_input)
    session["inputs"] = inputs

    input_iter = iter(inputs)
    session["input_needed"] = False

    def fake_input(prompt=""):
        try:
            return next(input_iter)
        except StopIteration:
            session["input_needed"] = True
            raise EOFError(prompt)

    try:
        with contextlib.redirect_stdout(io.StringIO()):
            result = mijn_script(fake_input, lambda x: output_log.append(x))
    except EOFError:
        pass
    except Exception as e:
        output_log.append(f"Fout: {e}")
    else:
        if result:
            output_log.append(result)

    return jsonify(output="\n".join(output_log))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 81))
    app.run(host="0.0.0.0", port=port, debug=True)
