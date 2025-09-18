from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_socketio import SocketIO, emit
import google.generativeai as genai
import pymongo
from datetime import datetime
import re
import os

app = Flask(__name__, template_folder='../templates')
socketio = SocketIO(app)

# Configure the API key (Replace with your actual API key)
genai.configure(api_key="AIzaSyAWtuRFSqCxNTMCLFqdmQQm4f6fEHb7j8A")

# MongoDB Connection Setup
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "codeanalyzer"
COLLECTION_NAME = "history"

def analyze_code(code):
    model = genai.GenerativeModel('gemini-1.5-flash')
    language_prompt = f"""
        Determine the programming language of the following code snippet. Respond with just the language name (e.g., python, javascript, java), nothing more:

{code}

    """
    language_response = model.generate_content(language_prompt)
    programming_language = language_response.text.strip()

    prompt = f"""
        You are an expert code reviewer. Analyze the following code written in {programming_language} for potential errors, suggest code optimizations, and provide a general conclusion about the code's quality and approach. Also, provide the corrected code after applying the suggestions in a code block.

       Here is the code:

{code}

       Expected Output:
        * Errors: List any syntax errors, logical errors, or runtime issues identified, along with suggestions on how to fix them. If no errors are found, explicitly state "No errors found"
        * Optimization Suggestions: Suggest ways to improve the code, making it more efficient, readable, or maintainable. If no optimization needed, explicitly state "No optimization needed"
        * Conclusion: Give an overall assessment of the code, covering its strengths, weaknesses, and any general observations.
       * Corrected Code: Give the corrected code after applying the suggestion
    """

    response = model.generate_content(prompt)
    return response.text, programming_language

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        code = request.form['code']
        if not code:
            return render_template('result.html', result="Please enter code.")
        socketio.emit('analysis_start', {'message': 'Analyzing...'})
        try:
            analysis_result, programming_language = analyze_code(code)
            corrected_code = extract_corrected_code(analysis_result)
            store_analysis(code, analysis_result, corrected_code, programming_language)
            socketio.emit('analysis_complete', {'result': analysis_result, 'corrected_code': corrected_code})
            return render_template('result.html', result=analysis_result, corrected_code=corrected_code)
        except Exception as e:
            return render_template('result.html', result=f"Error during analysis: {str(e)}")
    return render_template('input.html')

@app.route('/result')
def result():
    result_text = request.args.get('result', '')
    corrected_code = request.args.get('corrected_code', '')
    return render_template('result.html', result=result_text, corrected_code=corrected_code)

@app.route('/corrected_code')
def corrected_code():
    corrected_code = request.args.get('corrected_code', '')
    return render_template('corrected_code.html', corrected_code=corrected_code)

@app.route('/history')
def history():
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        history_collection = db[COLLECTION_NAME]
        all_history_entries = list(history_collection.find())
        client.close()
        return render_template('history.html', history=all_history_entries)
    except Exception as e:
        return render_template('history.html', error=str(e))

def extract_corrected_code(analysis_result):
    match = re.search(r'```(?:\w+)?\n(.*?)\n```', analysis_result, re.DOTALL)
    if match:
        corrected_code = match.group(1).strip()
        corrected_code = re.sub(r'[^\x20-\x7E]', '', corrected_code)
        corrected_code = corrected_code.replace('#', '').replace('*', '').strip()
        return corrected_code
    return "No corrected code found"

def store_analysis(code, result, corrected_code, programming_language):
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        history_collection = db[COLLECTION_NAME]
        timestamp = datetime.now()
        document = {
            "code": code,
            "date": timestamp.strftime("%Y-%m-%d"),
            "time": timestamp.strftime("%H:%M:%S"),
            "result": result,
            "corrected_code": corrected_code,
            "programming_language": programming_language
        }
        history_collection.insert_one(document)
        client.close()
    except Exception as e:
        print(f"Error storing data: {e}")

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
