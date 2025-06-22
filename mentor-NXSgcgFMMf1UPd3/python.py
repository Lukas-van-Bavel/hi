from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <h1>Console Program Runner</h1>
        <button onclick="runCode()">Run Different Program</button>
        <pre id="output"></pre>
        <script>
            function runCode() {
                fetch("/run", { method: "POST" })
                    .then(response => response.json())
                    .then(data => { 
                        document.getElementById('output').innerText = data.output || data.errors;
                    });
            }
        </script>
    '''

@app.route('/run', methods=['POST'])
def run_code():
    # Replace this code block with the code you want to execute
    code = """
print('Running a different Python script!')
"""

    result = subprocess.run(['python3', '-c', code], capture_output=True, text=True)
    return jsonify({'output': result.stdout, 'errors': result.stderr})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)