function sendToFlask(e){
    let btn = document.getElementById('submitbtn');
    let txt = document.getElementById('txt');
    
    btn.addEventListener('click', sendToFlask);

    let line = txt.value;
    let availID = parseInt(localStorage.getItem('availID'));
    let taskList = JSON.parse(localStorage.getItem('taskList'));

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
    .then(data => console.log(processResponse(data[0])))
    .catch(error => console.error(error));
}

function processResponse(pack){
    let availID = pack["availID"];
    let message = pack["message"];
    let taskList = pack["taskList"];

    localStorage.setItem('availID', JSON.stringify(availID));
    localStorage.setItem('taskList', JSON.stringify(taskList));
    return message
}