$(document).ready(() => {
    $(".chat-btn").click(() => {
        $(".chat-box").slideToggle("slow")
    })
})

let btn = document.getElementById('sendButton');
document.getElementById('inputText').addEventListener('keydown', event => {
    if (event.keyCode === 13) {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        document.getElementById("sendButton").click();
    }
})

btn.addEventListener('click', sendToFlask);

function sendToFlask(e){
    
    let txt = document.getElementById('inputText');

    if(txt.value != ""){
        let line = txt.value;
        printText(line, true);
        txt.value = '';
    
        let availID = localStorage.getItem('availID');
        if (availID == null) availID = 1;
        else availID = parseInt(availID);
    
        let taskList = JSON.parse(localStorage.getItem('taskList'));
        if (taskList == null) taskList = [];

        let pack = {
            "line" : line,
            "availID" : availID,
            "taskList" : taskList
        };
    
        fetch(`${window.origin}/receive-data`,{
            method : "POST",
            credentials: "include",
            body: JSON.stringify(pack),
            cache: "no-cache",
            headers: new Headers({
                "content-type": "application/json"
            })
        }).then(response => response.json())
        .then(data =>
            processResponse(data[0]))
        .catch(error => console.error(error));
    }
}

function processResponse(pack){
    let availID = pack["availID"];
    let message = pack["message"];
    let taskList = pack["taskList"];

    localStorage.setItem('availID', JSON.stringify(availID));
    localStorage.setItem('taskList', JSON.stringify(taskList));
    
    printText(message, false);
}


function printText(e,isFromUs){
    //e.preventDefault(); //biar ga reload

    //let txt = document.getElementById("inputText");
    if (isFromUs){
        let message = `<div class="my-chat">${e}</div>`
        let chats = document.getElementById("chats");
        chats.innerHTML += message;
    } else {
        let message = `<div class="client-chat">${e}</div>`
        let chats = document.getElementById("chats");
        chats.innerHTML += message;
    }
    document.getElementById("chats").scrollTo(0,document.getElementById("chats").scrollHeight);
}