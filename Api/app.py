from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os
import whisper

# Ajouter le dossier chatbot au path
sys.path.append(os.path.join(os.path.dirname(__file__), '../chatbot'))

# Importer la fonction du chatbot
from chat import get_response

app = Flask(__name__, static_folder="../Frontend/static", template_folder="../Frontend/templates")
CORS(app)

# Charger le modèle Whisper (version "base" pour la performance)
whisper_model = whisper.load_model("base")

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"response": "Please enter a message."})

        bot_response = get_response(user_message)
        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"Error: {e}")  # Log error for debugging
        return jsonify({"response": "An error occurred while processing your request."}), 500

# 🆕 Nouvelle route pour traiter l'audio et convertir en texte avec Whisper
@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    try:
        # Vérifier si un fichier audio est présent dans la requête
        if "audio" not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        audio_file = request.files["audio"]
        
        # Vérification du type de fichier
        if not audio_file.filename.endswith((".mp3", ".wav")):
            return jsonify({"error": "Invalid file type. Please upload a .mp3 or .wav file."}), 400

        # Sauvegarder le fichier temporairement
        file_path = os.path.join(os.getcwd(), "temp_audio" + os.path.splitext(audio_file.filename)[1])
        audio_file.save(file_path)

        print(f"Audio file saved to: {file_path}")  # Log pour vérifier la sauvegarde

        # Transcrire l'audio avec Whisper
        result = whisper_model.transcribe(file_path)
        text_transcribed = result["text"]

        # Supprimer le fichier temporaire après transcription
        os.remove(file_path)

        return jsonify({"transcription": text_transcribed})

    except Exception as e:
        print(f"Error during transcription: {e}")
        return jsonify({"error": "An error occurred during transcription"}), 500

if __name__ == "__main__":
    app.run(debug=True)
