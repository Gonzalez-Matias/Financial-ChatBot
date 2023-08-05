import os
from flask import Flask, render_template, request
from utils.ask import get_context
from utils.rol_prompt import SYSTEM_ROL
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

chat_messages = [{'role': 'system', 'content': SYSTEM_ROL}]

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    return get_openai_response(msg)

def get_openai_response(question):
    cont = get_context(question)
    input = "Q: '"+question+"', T:'"+cont+"'"
    chat_messages.append({'role': 'user', 'content': input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_messages,
        max_tokens=350,
    )['choices'][0]['message']['content']
    chat_messages.append({"role": "assistant", "content" : response})
    return response



if __name__ == '__main__':
    app.run()
