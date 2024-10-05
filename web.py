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
            body, html { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                padding: 0; 
                height: 100%; 
                display: flex; 
                flex-direction: column;
            }
            .container {
                display: flex;
                flex-direction: column;
                height: 100%;
                padding: 20px;
                box-sizing: border-box;
            }
            .header { margin-bottom: 20px; }
            .content { 
                display: flex; 
                flex-direction: column;
                flex-grow: 1;
                overflow: hidden;
            }
            .folder-selection { margin-bottom: 20px; }
            .json-view {
                display: flex;
                flex-direction: column;
                flex-grow: 1;
                overflow: hidden;
            }
            #json-output, #raw-json { 
                flex-grow: 1; 
                overflow: auto; 
                border: 1px solid #ccc; 
                padding: 10px; 
                margin-top: 10px;
            }
            #raw-json { 
                white-space: pre-wrap; 
                word-wrap: break-word; 
                display: none; 
            }
            input[type="text"] { 
                width: 100%; 
                box-sizing: border-box; 
                margin-bottom: 10px;
            }
            select { 
                width: 100%; 
                margin-bottom: 10px; 
            }
            button { margin-right: 10px; }
            .view-toggle { margin-bottom: 10px; }
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/prism.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-json.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/json-formatter-js@2.3.4/dist/json-formatter.umd.min.js"></script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>JSON Viewer</h1>
            </div>
            <div class="content">
                <div class="folder-selection">
                    <form method="post">
                        <label for="folder">Folder path:</label>
                        <input type="text" id="folder" name="folder" value="{{ current_folder }}">
                        <button type="submit">Change Folder</button>
                    </form>
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
                    {% if error_message %}
                        <p style="color: red;">{{ error_message }}</p>
                    {% endif %}
                </div>
                <div class="json-view">
                    {% if file_content %}
                        <h2>{{ selected_file }}</h2>
                        <div class="view-toggle">
                            <button onclick="toggleView('formatted')">Formatted View</button>
                            <button onclick="toggleView('raw')">Raw View</button>
                        </div>
                        <div id="json-output"></div>
                        <pre id="raw-json"></pre>
                    {% endif %}
                </div>
            </div>
        </div>
        {% if file_content %}
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
                document.getElementById('raw-json').textContent = JSON.stringify(json, null, 2);

                function toggleView(view) {
                    if (view === 'formatted') {
                        document.getElementById('json-output').style.display = 'block';
                        document.getElementById('raw-json').style.display = 'none';
                    } else {
                        document.getElementById('json-output').style.display = 'none';
                        document.getElementById('raw-json').style.display = 'block';
                    }
                }

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
