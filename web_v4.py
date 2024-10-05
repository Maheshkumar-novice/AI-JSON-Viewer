from flask import Flask, render_template_string, request
import os
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    current_folder = request.form.get('folder', os.getcwd())
    json_files = []
    error_message = None
    selected_file = None
    file_content = None

    try:
        json_files = [f for f in os.listdir(current_folder) if f.endswith('.json')]
    except Exception as e:
        error_message = f"Error accessing folder: {str(e)}"

    if request.method == 'POST' and 'file' in request.form:
        selected_file = request.form.get('file')
        try:
            with open(os.path.join(current_folder, selected_file), 'r') as f:
                file_content = json.dumps(json.load(f))  # No indentation here
        except Exception as e:
            error_message = f"Error reading file: {str(e)}"

    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>JSON Viewer</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            input[type="text"] { width: 300px; }
            select, button { margin: 10px 0; }
            pre { white-space: pre-wrap; word-wrap: break-word; background-color: #f0f0f0; padding: 10px; }
            .string { color: green; }
            .number { color: darkorange; }
            .boolean { color: blue; }
            .null { color: magenta; }
            .key { color: red; }
        </style>
        <script>
            function syntaxHighlight(json) {
                json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
                    var cls = 'number';
                    if (/^"/.test(match)) {
                        if (/:$/.test(match)) {
                            cls = 'key';
                        } else {
                            cls = 'string';
                        }
                    } else if (/true|false/.test(match)) {
                        cls = 'boolean';
                    } else if (/null/.test(match)) {
                        cls = 'null';
                    }
                    return '<span class="' + cls + '">' + match + '</span>';
                });
            }

            function formatJSON() {
                var input = document.getElementById('json-input').textContent;
                var output = document.getElementById('json-output');
                try {
                    var obj = JSON.parse(input);
                    var formattedJSON = JSON.stringify(obj, null, 4);
                    output.innerHTML = syntaxHighlight(formattedJSON);
                } catch (error) {
                    output.textContent = "Invalid JSON: " + error.message;
                }
            }
        </script>
    </head>
    <body>
        <h1>JSON Viewer</h1>
        <form method="post">
            <label for="folder">Folder path:</label><br>
            <input type="text" id="folder" name="folder" value="{{ current_folder }}">
            <button type="submit">Change Folder</button>
        </form>
        {% if error_message %}
            <p style="color: red;">{{ error_message }}</p>
        {% endif %}
        {% if json_files %}
            <form method="post">
                <input type="hidden" name="folder" value="{{ current_folder }}">
                <select name="file">
                    {% for file in json_files %}
                        <option value="{{ file }}" {% if file == selected_file %}selected{% endif %}>{{ file }}</option>
                    {% endfor %}
                </select>
                <button type="submit">View JSON</button>
            </form>
        {% endif %}
        {% if file_content %}
            <h2>{{ selected_file }}</h2>
            <pre id="json-input" style="display: none;">{{ file_content }}</pre>
            <pre id="json-output"></pre>
            <script>formatJSON();</script>
        {% endif %}
    </body>
    </html>
    '''

    return render_template_string(html, 
        current_folder=current_folder,
        json_files=json_files,
        selected_file=selected_file,
        file_content=file_content,
        error_message=error_message
    )

if __name__ == '__main__':
    app.run(debug=True)
