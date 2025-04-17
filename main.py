from flask import Flask, request, jsonify
import google.generativeai as genai
import datetime

app = Flask(__name__)

# Configure Google Generative AI
genai.configure(api_key="AIzaSyD2wwJeg6vIQUTH1TTqUr\")  # Replace with your actual API key
model = genai.GenerativeModel("gemini-1.5-pro")

# Predefined responses
predefined_responses = {
    "what should we know about your life story": 
        "I have a strong background in AI, machine learning, and software development. My journey has been about continuous learning and solving real-world problems using technology.",
    "what's your number one superpower": 
        "My number one superpower is problem-solving. I love tackling complex challenges and finding efficient solutions, especially in AI and software engineering.",
    "what are the top three areas you’d like to grow in": 
        "I want to grow in three key areas: Artificial Intelligence, Machine Learning, and Python for Large Language Models (LLMs). I aim to enhance my expertise in fine-tuning LLMs, optimizing AI models, and deploying scalable ML solutions.",
    "what misconception do your coworkers have about you": 
        "A common misconception is that I always prefer automation over manual work. While I love automation, I also understand the importance of human intuition and creativity in problem-solving.",
    "how do you push your boundaries and limits": 
        "I push my boundaries by continuously learning, taking on challenging projects, and staying updated with the latest advancements in AI and technology."
}

# Greeting based on time
def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        return "Good morning, sir. Hello, I am AI Bot, your voice assistant. How can I help you today?"
    elif 12 <= hour < 18:
        return "Good afternoon, sir. Hello, I am AI Bot, your voice assistant. How can I help you today?"
    else:
        return "Good evening, sir. Hello, I am AI Bot, your voice assistant. How can I help you today?"

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/greet', methods=['GET'])
def greet():
    return jsonify({"response": wish_me()})

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    text = data.get('text', '').lower()

    # Exit command handling
    exit_commands = ["exit", "quit", "bye"]
    if any(command in text for command in exit_commands):
        return jsonify({"response": "Goodbye! Have a great day."})

    # Check predefined responses
    for key in predefined_responses:
        if key in text:
            return jsonify({"response": predefined_responses[key]})

    # Fallback to generative AI
    try:
        response = model.generate_content(contents=[text])
        answer = response.text.strip()
        short_answer = answer[:150]  # Limit response length
        return jsonify({"response": short_answer + "..."})
    except Exception as e:
        return jsonify({"response": "Sorry, I couldn't process that."})

if __name__ == '__main__':
    app.run(debug=True)
