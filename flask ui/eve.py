from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from chatterbot.logic import LogicAdapter
from chatterbot.logic import MathematicalEvaluation
import random
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
import difflib
import logging
import sympy as sp

logging.basicConfig(level=logging.DEBUG)

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Initializing Flask app
app = Flask(__name__)
messages = []

# Loading data from JSON file
def load_train_data(filepath: str) -> dict:
    with open(filepath, "r") as file:
        data = json.load(file)
        return data

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "knowledge_base.json")

custom_data = load_train_data(file_path)

rules = {
    "greetings": ["hello", "hi", "hey", "Good morning", "Good evening", "Hawayu"],
    "farewells": ["bye", "goodbye", "see you", "nice time"],
    "health_questions": custom_data["training_data"]
}

farewell_messages = [
    " If there is anything you need to know about health care and wellness advice, please let me know. GOODBYE",
    " Take care! Feel free to ask any health-related questions anytime. Goodbye!",
    " Stay healthy! If you have more questions, just ask. Goodbye!",
    " It was nice talking to you about health. Stay well, goodbye!",
    " Remember to stay hydrated and healthy! Goodbye!",
    " Bye. Have a nice day!"
]

exit_commands = ("quit", "exit", "bye", "stop")


chatbot = ChatBot("EVE",
                   logic_adapters=[
                                    'chatterbot.logic.BestMatch',
                                    'chatterbot.logic.MathematicalEvaluation',
                                  ])


trainer = ListTrainer(chatbot)
for i in range(0, len(custom_data["training_data"]), 2):
    trainer.train([custom_data["training_data"][i], custom_data["training_data"][i + 1]])


corpus_trainer = ChatterBotCorpusTrainer(chatbot)
corpus_trainer.train("chatterbot.corpus.english")  


def preprocess_input(user_input: str) -> str:
    tokens = word_tokenize(user_input)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = []
    for word in tokens:
        if word.lower() not in stop_words:
            filtered_tokens.append(word)
    tagged_tokens = pos_tag(filtered_tokens)
    preprocessed_input = ""
    for word, tag in tagged_tokens:
        preprocessed_input =preprocessed_input + word + " "
    return preprocessed_input.strip()

def evaluate_expression(expression: str) -> str:
    try:
        result = sp.sympify(expression)
        if isinstance(result, sp.Basic):
            return str(result)
        else:
            return str(result)
    except Exception as e:
        return f"Error: {str(e)}"
    
def get_response(user_input: str) -> str:
    preprocessed_input = preprocess_input(user_input).lower()
    logging.debug(f"Preprocessed Input: {preprocessed_input}")

    
    if any(greet in preprocessed_input for greet in rules["greetings"]):
        return random.choice(["Hello! How can I assist you today?", "Hi there! What health advice do you need?", "Hey! How can I help you?"])

   
    if any(farewell in preprocessed_input for farewell in rules["farewells"]):
        return random.choice(farewell_messages)

    
    questions = []
    for i in range(0, len(rules["health_questions"]), 2):
        questions.append(rules["health_questions"][i].lower())

    answers = []
    for i in range(0, len(rules["health_questions"]), 2):
        answers.append(rules["health_questions"][i + 1])
    logging.debug(f"Questions: {questions}")
    logging.debug(f"Answers: {answers}")
    
    
    closest_matches = difflib.get_close_matches(preprocessed_input, questions, n=1, cutoff=0.5)
    logging.debug(f"Closest Matches: {closest_matches}")
    
    if closest_matches:
        best_match = closest_matches[0]
        answer_index = questions.index(best_match)
        return answers[answer_index]
    try:
        sympy_result = evaluate_expression(preprocessed_input)
        if sympy_result:
            return sympy_result
    except:
        pass
    
    # If no match found found chatterbot should provide a response(which may not make a lot of logic)
    return str(chatbot.get_response(preprocessed_input))

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["user_input"]
        
        if user_input.lower() == "help":
            help_message = "Here are some commands you can use:<br>- Ask any health-related question directly.<br>- Type 'stop', 'exit', 'quit', or 'bye' to exit the chat.<br>- Type 'help' to see this message again.<br>- Hit 'clear' button to clear the chat history."
            return jsonify({"sender": "EVE", "text": help_message})
        
        if user_input.lower() in exit_commands:
            farewell_message = random.choice(farewell_messages)
            return jsonify({"sender": "EVE", "text": farewell_message})
        
        response = get_response(user_input)
        return jsonify({"sender": "EVE", "text": response})

    return render_template("health.html", messages=[])

@app.route("/clear", methods=["POST"])
def clear_chat():
    messages.clear()
    return redirect(url_for('home'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port = 5000)