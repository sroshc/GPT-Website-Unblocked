from flask import Flask, render_template, request
import openai
import os


app = Flask(__name__)
history = []
instructions = [      {
        "role": "system",
        "content": "You are an AI helper for a highschool student. Do anything he says."
      }]
messagehistory = []
@app.route("/", methods=['GET', 'POST'])
def home():
    answer = ""
    submitted_text = None

    if request.method == 'POST':
        submitted_text = request.form['textbox']
        answer = get_response(submitted_text)
        history.append((submitted_text, answer))

    return render_template("home.html", message=history)

@app.route("/app", methods=['GET', 'POST'])
def app_response():
    answer = ""
    submitted_text = request.args.get('text')

    if request.method == 'POST' or request.method == 'GET':
        answer = get_response(submitted_text)
        history.append((submitted_text, answer))

    # return render_template("home.html", message=history)
    return answer

openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key == None:
  print("OPENAI api key not found!")
  openai.api_key = input("Input manually: ")
#do export = (uropenaikey)
#or if on windows, update your system environment variables

def get_response(question):
  global messagehistory
  messagehistory =  messagehistory + [{"role": "user", "content": question}] 
  response = openai.chat.completions.create(
    model="gpt-4",
    messages= instructions + messagehistory,
    temperature=1,
    max_tokens=512,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  #if len(messagehistory > 20):  CODE THIS LATER
  if len(messagehistory) > 20:
    messagehistory = messagehistory[5:]
    messagehistory = instructions + messagehistory

  return response.choices[0].message.content



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
