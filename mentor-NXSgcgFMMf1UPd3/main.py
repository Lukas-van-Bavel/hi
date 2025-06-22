from flask import Flask, request, session, render_template_string
import io
import contextlib

app = Flask(__name__)
app.secret_key = "geheim123"

def mijn_script():
    print("Voer de geheime code in om verder te gaan:")
    code = '1234'
    code_in = ''
    while code_in != code:
        
        print("> ", end="")
        code_in = input()

    print("dat is de corecte code!")


    while True :
        leeftijd = 14
        print(f"Mijn naam is Lukas van Bavel en ik ben {leeftijd} jaar oud.")
        print("Zoals je ziet hou ik van dingen maken en dus programmeren.")
        print(f'wat wil he weten .')
        print(f'1 ')
        print(f'2 ')
        while True:
            

@app.route("/", methods=["GET", "POST"])
def run_script():
    if request.method == "GET":
        session.clear()

    inputs = session.get("inputs", [])
    if request.method == "POST":
        user_input = request.form["user_input"]
        inputs.append(user_input)
        session["inputs"] = inputs

    input_iter = iter(inputs)

    def fake_input(prompt=""):
        try:
            return next(input_iter)
        except StopIteration:
            session["input_needed"] = True
            raise EOFError(prompt)

    f = io.StringIO()
    session["input_needed"] = False

    try:
        with contextlib.redirect_stdout(f):
            exec(mijn_script.__code__, {"input": fake_input, "print": print})
    except EOFError as e:
        output = f.getvalue() + str(e)
    except Exception as e:
        output = f"Fout: {e}"
    else:
        output = f.getvalue()

    html_template = """
    <html>
    <head>
    <style>
    body {
        font-family: monospace;
        padding: 30px;
        background: white;
        color: black;
        transition: background 0.3s, color 0.5s;
    }
    input, button {
        background: white;
        color: black;
        border: 1px solid #ccc;
    }
    body.dark {
        background: #121212;
        color: #e0e0e0;
    }
    body.dark input,
    body.dark button {
        background: #1e1e1e;
        color: #e0e0e0;
        border: 1px solid #555;
    }
    #theme-toggle {
        position: fixed;
        top: 10px;
        right: 10px;
        padding: 6px 10px;
        font-size: 14px;
        cursor: pointer;
        border-radius: 4px;
        z-index: 1000;
    }
    #stop-button {
        position: fixed;
        bottom: 10px;
        left: 10px;
        padding: 6px 10px;
        font-size: 14px;
        cursor: pointer;
        border-radius: 4px;
        background: red;
        color: white;
        border: none;
        z-index: 1000;
    }
        
    }
    .output-box {
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    </style>
    </head>
    <body>
    <button id="theme-toggle">🌗 Thema</button>
    <button id="stop-button">⛔ Stop</button>
    <div class="output-box">{{ output }}</div>
    {% if session.input_needed %}
        <form method="post">
            <label>> <input name="user_input" autofocus autocomplete="on"/></label>
            <button type="submit">Geef input</button>
        </form>
    {% endif %}
    <script>
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark");
    }
    document.getElementById("theme-toggle").onclick = () => {
        document.body.classList.toggle("dark");
        localStorage.setItem("theme", document.body.classList.contains("dark") ? "dark" : "light");
    };
    document.getElementById("stop-button").onclick = () => {
        if (confirm("Weet je zeker dat je de pagina wilt sluiten?")) {
            window.open('', '_self', '');
            window.close();
        }
    };
    </script>
    <head>
    <meta charset="UTF-8" />
    <title>Niet-interactief tekstblok</title>
    <style>
      .tekstblok {
        position: absolute;
        bottom: 10px;
        right: 50px;
        user-select: none;
        pointer-events: none;
        background-color: none;
        padding: none;
        border: none;;
      }
    </style>
    </head>
    <body>

    <div class="tekstblok">
        <p>klik op stop als je <p>
        <p>deze pagina wil af sluiten<p>
        <p>en typ BT <p>
    </div>
    </body>
    </html>
    """

    return render_template_string(html_template, output=output)

app.run(host="0.0.0.0", port=81)