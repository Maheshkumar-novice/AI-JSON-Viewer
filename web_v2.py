import os
import json
from flask import Flask, render_template_string, request
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    current_folder = request.form.get('folder', os.getcwd())
    json_files = [f for f in os.listdir(current_folder) if f.endswith('.json')]
    selected_file = None
    formatted_json = None

    if request.method == 'POST':
        if 'folder' in request.form:
            current_folder = request.form.get('folder')
            json_files = [f for f in os.listdir(current_folder) if f.endswith('.json')]
        elif 'file' in request.form:
            selected_file = request.form.get('file')
            if selected_file:
                file_path = os.path.join(current_folder, selected_file)
                with open(file_path, 'r') as f:
                    json_content = json.load(f)
                    json_str = json.dumps(json_content, indent=2)
                    formatted_json = highlight(json_str, JsonLexer(), HtmlFormatter())

    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>JSON Viewer</title>
        <style>
            {{ pygments_css }}
            body { font-family: Arial, sans-serif; margin: 20px; }
            select, input, button { margin-bottom: 10px; }
            pre { white-space: pre-wrap; word-wrap: break-word; }
        </style>
    </head>
    <body>
        <h1>JSON Viewer</h1>
        <form method="post">
            <label for="folder">Folder:</label>
            <input type="text" id="folder" name="folder" value="{{ current_folder }}" style="width: 300px;">
            <button type="submit">Change Folder</button>
        </form>
        <form method="post">
            <input type="hidden" name="folder" value="{{ current_folder }}">
            <select name="file">
                {% for file in json_files %}
                    <option value="{{ file }}" {% if file == selected_file %}selected{% endif %}>{{ file }}</option>
                {% endfor %}
            </select>
            <button type="submit">View JSON</button>
        </form>
        {% if formatted_json %}
            <h2>{{ selected_file }}</h2>
            <pre>{{ formatted_json | safe }}</pre>
        {% endif %}
    </body>
    </html>
    '''

    return render_template_string(html, 
        current_folder=current_folder,
        json_files=json_files, 
        selected_file=selected_file, 
        formatted_json=formatted_json,
        pygments_css=HtmlFormatter().get_style_defs('.highlight')
    )

if __name__ == '__main__':
    app.run(debug=True)
