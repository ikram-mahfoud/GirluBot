import torch
from transformers import BertTokenizer, BertModel
from torch.nn.functional import cosine_similarity
import json
import random
import speech_recognition as sr
import pyttsx3
import re

# Charger BERT pré-entraîné
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

# Initialisation de pyttsx3 (text-to-speech)
engine = pyttsx3.init()

def clean_text(text):
    """Nettoie le texte en enlevant la ponctuation et en mettant en minuscule."""
    text = text.lower()  # Convertir en minuscule
    text = re.sub(r"[^\w\s]", "", text)  # Supprimer la ponctuation
    return text

def encode_sentence(sentence):
    """Transforme une phrase en vecteur avec BERT."""
    sentence = clean_text(sentence)  # Normaliser le texte avant encodage
    tokens = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        output = model(**tokens)
    return output.last_hidden_state[:, 0, :]  # Utilise le token [CLS] comme représentation

# Charger les intents
with open("C:/Min-Project/Development/chatbot/data/intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)

# Encoder toutes les phrases des intents
intent_patterns = []
intent_tags = []
intent_responses = {}

for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        clean_pattern = clean_text(pattern)  # Normaliser les patterns
        intent_patterns.append(clean_pattern)
        intent_tags.append(intent["tag"])
    intent_responses[intent["tag"]] = intent["responses"]

pattern_vectors = torch.cat([encode_sentence(p) for p in intent_patterns])

def get_response(user_input):
    """Trouve la réponse la plus pertinente en utilisant la similarité BERT."""
    user_input = clean_text(user_input)  # Nettoyage du texte

    input_vector = encode_sentence(user_input)
    similarities = cosine_similarity(input_vector, pattern_vectors)

    # Debugging : Affichage des similarités
    print(f"🔹 User input: {user_input}")
    print(f"🔹 Similarities: {similarities.tolist()}")

    best_match_idx = similarities.argmax().item()
    best_tag = intent_tags[best_match_idx]

    return random.choice(intent_responses[best_tag])

def speak(text):
    """Fait parler le robot."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Écoute ce que l'utilisateur dit et convertit le son en texte."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Je vous écoute...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        user_input = recognizer.recognize_google(audio, language="en-US")  # Utiliser la reconnaissance vocale
        user_input = clean_text(user_input)  # Normaliser après reconnaissance
        print(f"Vous avez dit: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("Désolé, je n'ai pas compris.")
        return None
    except sr.RequestError:
        print("Erreur de service de reconnaissance vocale.")
        return None

if __name__ == "__main__":
    while True:
        user_input = listen()  # Écouter ce que l'utilisateur dit
        if user_input:
            bot_response = get_response(user_input)  # Obtenir la réponse du chatbot
            print(f"Robot: {bot_response}")
            speak(bot_response)  # Faire parler le robot
