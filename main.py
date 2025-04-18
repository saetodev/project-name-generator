import json

from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

app.debug = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True
app.jinja_env.cache = {}

client = OpenAI()


@app.route("/gen", methods=["POST"])
def gen():
    pdesc = request.form.get("pdesc", type=str)

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": "Analyze the project description and come up with a project name."},
            {"role": "system",
                "content": "Try comming up with unique names, and be creative."},
            {"role": "system", "content": "Generate a JSON object with fields: name."},
            {"role": "system", "content": "Respond only with JSON. Do NOT wrap in code fences or markdown."},
            {"role": "user", "content": pdesc}
        ],
    )

    return jsonify(json.loads(response.output_text))


@ app.route("/")
def index():
    return render_template("index.html")
