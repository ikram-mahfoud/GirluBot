document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat");
    const inputField = document.getElementById("input");
    const sendButton = document.getElementById("button");
    const micButton = document.querySelector(".mic-button");

    let voices = [];
    const selectedLanguage = 'en-US'; // Langue par défaut (anglais)

    // Charger les voix disponibles
    function loadVoices() {
        voices = speechSynthesis.getVoices();
        console.log("Available voices:", voices);
    }

    if ('speechSynthesis' in window) {
        speechSynthesis.onvoiceschanged = loadVoices;
    }

    // Fonction pour filtrer les emojis
    function filterEmojis(text) {
        return text.replace(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{2300}-\u{23FF}\u{2B50}\u{2764}\u{1F004}-\u{1F0CF}\u{25AA}\u{25FE}\u{2B06}\u{2194}\u{2B05}\u{2934}\u{2199}\u{1F004}\u{1F0CF}]/gu, "");
    }

    // Fonction pour la synthèse vocale
    function speakResponse(text) {
        if (!('speechSynthesis' in window)) {
            console.error('Speech synthesis is not supported in this browser.');
            return;
        }

        const filteredText = filterEmojis(text);

        const speech = new SpeechSynthesisUtterance(filteredText);
        let selectedVoice = voices.find(voice => voice.lang === selectedLanguage); // Sélection de la voix en fonction de la langue
        if (selectedVoice) {
            speech.voice = selectedVoice;
        }

        speech.lang = selectedLanguage; // Définit la langue
        speech.rate = 1;
        speech.volume = 1;
        speech.pitch = 1;

        speechSynthesis.speak(speech);
    }

    function recordAndSendAudio() {
        navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            let audioChunks = [];

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append("audio", audioBlob, "audio.wav");

                try {
                    const response = await fetch("http://127.0.0.1:5000/transcribe", {
                        method: "POST",
                        body: formData
                    });

                    const data = await response.json();
                    if (data.transcription) {
                        inputField.value = data.transcription;
                        sendMessage(); // Envoyer automatiquement le message transcrit
                    }
                } catch (error) {
                    console.error("Error:", error);
                }
            };

            mediaRecorder.start();

            setTimeout(() => {
                mediaRecorder.stop();
            }, 5000); 
        }).catch(error => {
            console.error("Microphone access error:", error);
        });
    }

    // Fonction pour envoyer le message
    function sendMessage() {
        const userMessage = inputField.value.trim();
        if (!userMessage) return;

        appendMessage("user", userMessage);
        inputField.value = "";

        fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage("bot", data.response);
            speakResponse(data.response);
        })
        .catch(error => {
            console.error("Error:", error);
            appendMessage("bot", "Sorry, something went wrong.");
        });
    }

    // Fonction pour ajouter le message dans la boîte de chat
    function appendMessage(sender, message) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender);

        const avatar = document.createElement("div");
        avatar.classList.add("avatar");

        const text = document.createElement("div");
        text.classList.add("text");
        text.textContent = message;

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(text);
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    sendButton.addEventListener("click", sendMessage);
    inputField.addEventListener("keypress", (event) => {
        if (event.key === "Enter") sendMessage();
    });
    micButton.addEventListener("click", recordAndSendAudio);
});
