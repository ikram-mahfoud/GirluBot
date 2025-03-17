# GirlyBot - Chatbot avec Reconnaissance Vocale et Traitement de Texte
GirlyBot est un chatbot interactif basé sur Flask et utilisant la reconnaissance vocale avec Whisper pour convertir la parole en texte, en plus de la réponse textuelle générée avec BERT.

# Fonctionnalités principales :
Réponse à des messages textuels.
1-Transcription audio en texte via Whisper.
2-Génération de réponses avec BERT en utilisant la similarité cosinus.
3-Synthèse vocale pour rendre le chatbot plus interactif.

# Installez les dépendances nécessaires :
pip install -r requirements.txt

# Lancer l'application
Ouvrez votre terminal, allez dans le dossier du projet et lancez l'application Flask :
python app.py
Accédez à votre navigateur à l'adresse http://127.0.0.1:5000 pour interagir avec le chatbot.

# Fichiers principaux :
app.py : Contient la logique du serveur Flask, gestion des requêtes, et des endpoints pour la transcription audio.
chat.py : Contient la logique du chatbot, traitement des messages, utilisation de BERT pour la similarité de texte.
transcribe.py : Utilise Whisper pour la transcription audio en texte.
chat.js : Code JavaScript pour l'interface de chat (gestion des messages et de la synthèse vocale).
chat.css : Styles pour l'interface de chat.

# Dépendances
Les dépendances principales incluent :
Flask
Flask-Cors
whisper
transformers
torch
nltk
pyttsx3
speech_recognition

# Vous pouvez installer ces dépendances avec :
pip install flask flask-cors whisper transformers torch nltk pyttsx3 speech_recognition

# Utilisation de la Reconnaissance Vocale
Pour utiliser la fonctionnalité de reconnaissance vocale, cliquez sur le bouton "🎤" pour enregistrer votre message audio. Le chatbot le convertira en texte et répondra en utilisant la logique de traitement de texte.


