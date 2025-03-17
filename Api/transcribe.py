import whisper
import os

# Charger le modèle Whisper (version "base")
model = whisper.load_model("base")

def transcribe_audio(file_path):
    """Transcrit un fichier audio en texte"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} est introuvable.")
    
    result = model.transcribe(file_path)
    return result["text"]

if __name__ == "__main__":
    # Exemple d'utilisation avec un fichier audio
    file_path = "temp_audio.mp3"  # Chemin absolu
    try:
        transcription = transcribe_audio(file_path)
        print("Transcription:", transcription)
    except Exception as e:
        print(f"Erreur lors de la transcription : {str(e)}")
