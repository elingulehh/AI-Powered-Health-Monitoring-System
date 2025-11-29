from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Initialize ChatBot
chatbot = ChatBot('HealthBot')

# Train the chatbot with English corpus
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

# Health-specific responses (extend as needed)
health_responses = {
    "symptoms": "Please describe your symptoms in detail.",
    "fever": "A fever might indicate an infection. Monitor your temperature and stay hydrated.",
    "headache": "Headaches can be caused by stress or dehydration. Rest and drink water.",
    "chest pain": "Chest pain is serious. Seek medical attention immediately.",
    "default": "I'm here to help with health questions. Please provide more details."
}

def get_response(user_input):
    response = str(chatbot.get_response(user_input))
    # Add health-specific logic
    input_lower = user_input.lower()
    if "symptom" in input_lower:
        response += " " + health_responses["symptoms"]
    elif "fever" in input_lower:
        response += " " + health_responses["fever"]
    elif "headache" in input_lower:
        response += " " + health_responses["headache"]
    elif "chest pain" in input_lower:
        response += " " + health_responses["chest pain"]
    else:
        response += " " + health_responses["default"]
    return response
