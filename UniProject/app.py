from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

def call_api(url, headers=None, method="GET"):
    try:
        if method.upper() == "POST":
            response = requests.post(url, headers=headers)
        else:
            response = requests.get(url, headers=headers)
        return response.text
    except Exception as exception:
        return f"Error: {exception}"

@app.route("/", methods=["GET", "POST"])
def home():
    api_result = None
    if request.method == "POST":
        url = request.form.get("url")
        headers_text = request.form.get("headers")
        method = request.form.get("method", "GET")
        headers = {}
        if headers_text:
            try:
                headers = json.loads(headers_text)
            except json.JSONDecodeError:
                api_result = "Invalid headers JSON"
        if url and not api_result:
            api_result = call_api(url, headers, method)
    return render_template("index.html", name="World", api_result=api_result)

if __name__ == "__main__":
    app.run(debug=True)