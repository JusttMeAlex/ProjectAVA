from flask import Flask, render_template, request, jsonify
import spacy
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import speech_recognition as sr
import pyttsx3
import random
import nltk

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

def process_input(user_input):
    doc = nlp(user_input)
    named_entities = [ent.text for ent in doc.ents]
    tokens = word_tokenize(user_input)
    return named_entities, tokens

def predict_task(processed_input):
    return "Perform a task based on " + str(processed_input)

def custom_responses(user_input):
    if "i'm home" in user_input:
        return "Welcome home, sir."
    elif "are you there" in user_input:
        return "For you sir, always."
    elif "hello ava" in user_input:
        return "Hello sir."
    elif "who are you" in user_input:
        return "Hello I am AVA, a multipurpose ai assistant coded by Lex."
    elif "thank you" in user_input:
        return "As always you are welcome sir."
    elif "who is hitler" in user_input:
        return "Fuck Hitler."
    elif "what does ava mean" in user_input:
        return "Avamis stands for Advanced Virtual Assistant Managing Intelligent Systems."
    else:
        return None

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your commands...")
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio)
        print(f"You: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Can you please repeat?")
        return ""

def speak(response):
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()

def generate_human_like_response(tokens):
    pos_tags = pos_tag(tokens)
    verbs = [word for word, pos in pos_tags if pos.startswith('VB')]
    nouns = [word for word, pos in pos_tags if pos.startswith('NN')]
    response = "Certainly, I can help you with "
    if verbs:
        response += ", ".join(verbs)
    elif nouns:
        response += ", ".join(nouns)
    else:
        response += "various tasks"
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask_avamis', methods=['POST'])
def ask_avamis():
    user_input = request.form.get('command')
    custom_response = custom_responses(user_input)
    if custom_response:
        speak(custom_response)
        return jsonify({'response': custom_response})
    else:
        named_entities, tokens = process_input(user_input)
        task_prediction = predict_task(tokens)
        human_like_response = generate_human_like_response(tokens)
        speak(human_like_response)
        return jsonify({'response': human_like_response})

if __name__ == "__main__":
    print("Initializing AI System...")  
    print("AI System is online and ready! Listening for your commands...")
    app.run(debug=True)
