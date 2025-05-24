const messageContainer = document.getElementById("message-container");

function typeMessage(message) {
  messageContainer.textContent = message;
}

const socket = new WebSocket("ws://localhost:8000/ws");
socket.onmessage = function (event) {
  const data = event.data;
  console.log(data);
  typeMessage(data);
};
