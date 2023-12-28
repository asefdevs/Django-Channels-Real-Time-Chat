const roomName = JSON.parse(document.getElementById('room-name').textContent);
const user = JSON.parse(document.getElementById('user').textContent);
const conversation = document.getElementById('conversation');
const sendButton = document.querySelector("#send");
const commentInputDom = document.querySelector("#comment");

const chatSocket = new WebSocket('ws://'+ window.location.host+ '/ws/chat/'+ roomName+ '/');

chatSocket.onmessage = function(e){
    const data = JSON.parse(e.data)

    if ( user === data.user){
        var message = `
                <div class="row message-body">
                <div class="col-sm-12 message-main-sender">
                <div class="sender">
                    <div class="message-text">
                    
                    ${data['message']}

                    </div>
                    <span class="message-time pull-right">
                    ${data['created_at']}
                    </span>
                </div>
                </div>
            </div> 
    `

    }
    else{
        var message = `
                <div class="row message-body">
                <div class="col-sm-12 message-main-receiver">
                <div class="receiver">
                    <div class="message-text">
                    
                    ${data['message']}

                    </div>
                    <span class="message-time pull-right">
                    ${data['created_at']}
                    </span>
                </div>
                </div>
            </div> 
    `
    }
    
    
    conversation.innerHTML += message;
};

chatSocket.onclose = function(e){
    console.error('Chat socket closed unexpectedly');
}

commentInputDom.focus();
commentInputDom.onkeyup = function(e){
    if(e.keyCode === 13){
        sendButton.click();
    }
}

sendButton.onclick = function(e){
    const message = commentInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    commentInputDom.value = '';
}

