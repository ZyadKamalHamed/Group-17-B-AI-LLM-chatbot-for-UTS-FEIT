const chatToggle = document.getElementById("chat-toggle");
const chatWidget = document.getElementById("chat-widget");
const chatClose = document.getElementById("chat-close");
const sendBtn = document.getElementById("send-btn");
const chatInput = document.getElementById("chat-input");
const chatMessages = document.getElementById("chat-messages");

const API_URL = "http://127.0.0.1:8000/chat";

chatToggle.addEventListener("click", () => {
  chatWidget.classList.remove("hidden");
});

chatClose.addEventListener("click", () => {
  chatWidget.classList.add("hidden");
});

sendBtn.addEventListener("click", sendMessage);

chatInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
});

function addMessage(text, sender, sources = []) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender);

  const textDiv = document.createElement("div");
  textDiv.textContent = text;
  messageDiv.appendChild(textDiv);

  if (sender === "bot" && sources.length > 0) {
    const sourcesDiv = document.createElement("div");
    sourcesDiv.classList.add("sources");

    const title = document.createElement("div");
    title.textContent = "Sources:";
    sourcesDiv.appendChild(title);

    sources.forEach((source) => {
      const link = document.createElement("a");
      link.href = source;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = source;

      const line = document.createElement("div");
      line.appendChild(link);
      sourcesDiv.appendChild(line);
    });

    messageDiv.appendChild(sourcesDiv);
  }

  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addTypingIndicator() {
  const typingDiv = document.createElement("div");
  typingDiv.classList.add("message", "bot", "typing");
  typingDiv.id = "typing-indicator";
  typingDiv.textContent = "Typing...";
  chatMessages.appendChild(typingDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
  const typingDiv = document.getElementById("typing-indicator");
  if (typingDiv) {
    typingDiv.remove();
  }
}

async function sendMessage() {
  const question = chatInput.value.trim();

  if (!question) return;

  addMessage(question, "user");
  chatInput.value = "";
  addTypingIndicator();

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      throw new Error("Failed to get response from backend");
    }

    const data = await response.json();

    removeTypingIndicator();
    addMessage(data.answer, "bot", data.sources || []);
  } catch (error) {
    removeTypingIndicator();
    addMessage("Sorry, something went wrong while contacting the backend.", "bot");
    console.error(error);
  }
}