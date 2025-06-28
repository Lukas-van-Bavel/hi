# app.py
from flask import Flask, request, session, jsonify, render_template_string
import io
import contextlib
import os

app = Flask(__name__)
app.secret_key = "geheim123"

def mijn_script(get_input, output):
    output("Voer de geheime code in om verder te gaan:")
    code = '70767'
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
        output("Zoals u ziet hou ik van dingen maken en dus ook programmeren.")
        output("Wat wil u weten:")
        output("1. Mijn schoolcarrière")
        output("2. Mijn hobby's")
        output("3. Mijn familie")
        output("Typ 1, 2, 3 ")

        keuze = get_input("input_choice")
        if keuze == '1':
            output("welk stuk je wilt u weten.")
            output("eerst moet u weten dat ik ben in gestroomt afgelopen jaar en dat ik op beekvliet een tussen jaar heb gedaan in plaats van groep 8")
            output("1 basis school.")
            output(f"\n2 tussen jaar (intermezzo).") 
            output("3 middel bare school.")
            keuze = get_input(" ")
            if keuze == '1' :
                output(f"\n ik heb op 2 basisscholen gezeten de driestroom van groep 1 tot 5.5 en het kindcentrum aan de oosterplas daar heb ik van groep eind 5 tot groep 7")
                output(f"\n(mijn school cariere is zo complex dat ik he graag eenkeer wil uit leggen maar voor nu is dat echt te veel")
                output("ik ben in plaatvan groep 8 ben ik naar intermezzo gegaan op beekvliet")
            elif keuze == '2' :
                output(f"\n ik heb de groep 8 overgeslagen of groep 7 en 8 in een ge daan dat is voor mij zelf niet eens duidelijk")
                output("intermetzzo eke IMZ is een tussen jaar voor lerlingen die al klaar zijn met de basis school maar nog niet klaar zijn voor de middelbare")
                output("het was een erg bijzondere klas want we begonen met 16 leerlingen en aan het eind waren er 2 af gevallen")
            elif keuze == '3' :
                output(f"\n nou ik heb op 2 middenbare scholen gezeeten eerst ben ik op beekvliet in de 1e gekomen om er daar na al gauw er achter te komen dat grieks en latijn toch wat et moelijk zijn")
                output(" ik moest dus van beekvliet omdat ze aleen gymnasium hebben ik kon toen gewoon naar atheneum maar er was geen ruimte op het roden borg toen moest ik naar een HA klas op het pierson om dat de A klassen vol zaten, dit vond ik erg jammer") 
                output("dit jaar is ook mijn frans er uit gegaan talen zijn niet mijn ding")
            
        elif keuze == '2':
            output("wat van mijn hobby's wil je weten")
            output("ik hou van dingen maken denk aan progameren enzo dat noem ik zelf altijd projecten")
            output("1 projecte")
            output(f"\n2 sport.") 
            keuze = get_input(" ")
            if keuze == '1' :
                output(f"\nik hou van het maken van dingen denk aan progameren, bouwen bedenken enz")
                output("ik heb erg wijde intreseses en dat zie je in mijn projecte zo ben ik nu bezig met een gimbal maar ben ik ooojk al 2 jaar met een sooort boot bezig die ik als onderzoek en project platvoorm wil gebruiken") 
                output("druk op de invoer knop om terug tegaan")
            elif keuze == '2' :
                output(f"\n ik hardloop en zijl echt atletiek ben ik me gestopt op dit moment")
                output("ik zijl op een open big dat is een soort surfplank maar dan is het nog wel een soort van boot")
                output("wij hebben thuis ook een miror dat is een helemaal houte zijl boot daar zijl ik aleen niet zo veel op")
                output("ik hard loop erg graag ikk heb een paar jaar aan atletiek gedaan maar daar ben ik vlak voor het eide van het school jaar me gestopt")
                output("ik ga me nu vooral op het lange afstands lopen richten ik heb laats de vesting loop me gedaan en daar heb ik de 10 km gelopen")
            elif keuze == '3' :
                output(f"\n                   hi dit was geen optie")
            else :
                output("dat is geen geldige keuze")
                output("of er is een foud op getreden")
        elif keuze == '3':
            output("Ik heb 2 broertjes en een zusje.")
            output("ik heb een vader en een moeder")
            output("ik heb ook de aller liefste hond van de hele wereld joep of joepie")
            output("ik heb een opa en 2 oma's mijn opa is helaas 1,5 jaar geleden overleden")
            output(f"\nik heb 9 neefjes en nichtjes")
        else:
            output("Ongeldige keuze, probeer opnieuw.")
            output("Of er is een fout op getreden")

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
