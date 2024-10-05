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
                file_content = json.dumps(json.load(f))
        except Exception as e:
            error_message = f"Error reading file: {str(e)}"

    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>JSON Viewer</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism.min.css" rel="stylesheet" />
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            input[type="text"] { width: 300px; }
            select, button { margin: 10px 0; }
            pre { white-space: pre-wrap; word-wrap: break-word; background-color: #f0f0f0; padding: 10px; }
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/prism.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-json.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/json-formatter-js@2.3.4/dist/json-formatter.umd.min.js"></script>
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
            <div id="json-output"></div>
            <script>
                var json = {{ file_content | safe }};
                var formatter = new JSONFormatter(json, 2, {
                    hoverPreviewEnabled: true,
                    hoverPreviewArrayCount: 100,
                    hoverPreviewFieldCount: 5,
                    theme: '',
                    animateOpen: true,
                    animateClose: true
                });
                document.getElementById('json-output').appendChild(formatter.render());

                // Apply Prism.js highlighting
                Prism.highlightAll();
            </script>
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
