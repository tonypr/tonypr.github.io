from flask import Flask, request, jsonify, render_template
import requests
import re

LITGPT_URL = "http://127.0.0.1:8000/predict"
app = Flask(__name__)


def convert_to_html(text):
    # Convert bold text
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)

    # Convert new lines to <br> tags
    text = text.replace("\n", "<br>")

    return text


def llm_generate(prompt):
    try:
        litgpt_response = requests.post(LITGPT_URL, json={"prompt": prompt})
        litgpt_response.raise_for_status()
        output = litgpt_response.json().get("output")
        return {"output": output}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process_prompt():
    data = request.json
    if not data or "prompt" not in data:
        return jsonify({"error": "No prompt provided"}), 400

    prompt = data["prompt"]
    response = llm_generate(prompt)

    if "error" in response:
        return jsonify(response), 500

    response["output"] = convert_to_html(response["output"])
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
