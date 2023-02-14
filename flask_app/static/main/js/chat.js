var socket;
    $(document).ready(function(){
        
        socket = io.connect('https://' + document.domain + ':' + location.port + '/chat');
        socket.on('connect', function() {
            socket.emit('joined', {});
            console.log("socket emit");
        });

        socket.on('status', function(data) {     
            let tag  = document.createElement("p");
            
            let text = document.createTextNode(data.msg);
            let element = document.getElementById("chat2");
            
            tag.appendChild(text);
            tag.style.cssText = data.style;
            element.appendChild(tag);
            $('#chat').scrollTop($('#chat')[0].scrollHeight);
        });   

        socket.on('leave', function(data){
            let tag = document.createElement("p");
            let text = document.createTextNode(data.msg);
            let element = document.getElementById("chat2");

            tag.appendChild(text);
            tag.style.cssText = data.style;
            element.appendChild(tag);
            $('#chat').scrollTop($('#chat')[0].scrollHeight);
            socket.disconnect();

        });

        socket.on('messageToChat', function(data){
            let tag = document.createElement("p");
            let text = document.createTextNode(data.msg);
            let element = document.getElementById("chat2");
         

            tag.appendChild(text);
            tag.style.cssText = data.style;
            element.appendChild(tag);
            $('#chat').scrollTop($('#chat')[0].scrollHeight);
        });

        var leaveButton = document.querySelectorAll("#leaveChatB");
        
        for(i = 0; i<leaveButton.length; i += 1){
            leaveButton[i].addEventListener("click", leaveMessage);
        }

        function leaveMessage(){
            socket.emit('leaveChat', {});
            
        };

        function sendMessageFunc(e){
            if(e.keyCode === 13){
                var userMsg = document.querySelector("#msgInput").value;
                socket.emit('sendMessage', userMsg);
                document.querySelector("#msgInput").value = "";
            }
        };

        document.addEventListener('keydown', function sendMessage(e){ sendMessageFunc(e); });
    });