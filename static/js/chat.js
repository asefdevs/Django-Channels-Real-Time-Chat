const roomName = JSON.parse(document.getElementById('room-name').textContent);
const chatSocket = new WebSocket('ws://'+ window.location.host+ '/ws/chat/'+ roomName+ '/');

chatSocket.onmessage = function(e){
    const data = JSON.parse(e.data);

    console.log(data.messagge);
    // const message = data['message'];
    // document.querySelector('#chat-log').value += (message + '\n');
}