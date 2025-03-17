import os
import whisper

whisper_model = whisper.load_model("base")

file_path = "C:/Min-Project/Development/chatbot/Api/temp_audio.mp3"  # Fichier audio à la racine du projet

if not os.path.exists(file_path):
    print(f"Erreur: Le fichier {file_path} est introuvable.")
else:
    result = whisper_model.transcribe(file_path)
    print("Transcription:", result["text"])
