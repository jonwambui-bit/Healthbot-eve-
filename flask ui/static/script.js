document.addEventListener("DOMContentLoaded", () => {
  const chatContainer = document.getElementById('chat-container');
  const userInput = document.getElementById('user-input');
  const sendButton = document.getElementById('send-button');

  sendButton.addEventListener('click', (e) => {
    e.preventDefault();
    const userInputValue = userInput.value.trim();
    if (userInputValue !== '') {
      displayMessage({ sender: 'You', text: userInputValue });
      userInput.value = '';
      sendUserInput(userInputValue);
    }
  });

  function displayMessage(message) {
    const messageHTML = `
      <div class="${message.sender === 'You' ? 'user-message' : 'ai-message'}">
        <strong>${message.sender}:</strong> <p>${message.text}</p>
      </div>
    `;
    chatContainer.innerHTML += messageHTML;
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function sendUserInput(input) {
    fetch('/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({ user_input: input }),
    })
    .then(response => response.text())
    .then(data => {
      // Parse the response to extract messages and display them
      const parser = new DOMParser();
      const doc = parser.parseFromString(data, 'text/html');
      const messages = doc.querySelectorAll('#chat-container .message');
      chatContainer.innerHTML = '';
      messages.forEach(msg => chatContainer.appendChild(msg));
      chatContainer.scrollTop = chatContainer.scrollHeight;
    })
    .catch(error => console.error('Error:', error));
  }
});