//https://howtocreateapps.com/fetch-and-display-json-html-javascript/
//fetch('http://localhost:4500/TOP?name=PS5&ranking=5')
fetch('http://localhost:4500/TOP?name=PS5&ranking=10', {mode: 'cors'})
    .then(function (response) {
        console.log(response)
        return response.json();
    })
    .then(function (data) {
        console.log("my data",data)
        appendData(data);
    })
    .catch(function (err) {
        console.log(err);
    });

function appendData(data) {
    var mainContainer = document.getElementById("myData");
    for (var i = 0; i < data.length; i++) {
        var div = document.createElement("div");
        div.innerHTML = data[i];
        mainContainer.appendChild(div);
    }

}

fetch('http://localhost:4500/TOP?name=XBOX&ranking=5', {mode: 'cors'})
    .then(function (response) {
        console.log(response)
        return response.json();
    })
    .then(function (data2) {
        console.log("my data",data2)
        appendData2(data2);
    })
    .catch(function (err) {
        console.log(err);
    });

function appendData2(data2) {
    var mainContainer = document.getElementById("myData2");
    for (var i = 0; i < data2.length; i++) {
        var div = document.createElement("div");
        div.innerHTML = data2[i];
        mainContainer.appendChild(div);
    }

}

fetch('http://localhost:4500/TOP?name=PC&ranking=1', {mode: 'cors'})
    .then(function (response) {
        console.log(response)
        return response.json();
    })
    .then(function (data3) {
        console.log("my data",data3)
        appendData3(data3);
    })
    .catch(function (err) {
        console.log(err);
    });





function appendData3(data3) {
    var mainContainer = document.getElementById("myData3");
    for (var i = 0; i < data3.length; i++) {
        var div = document.createElement("div");
        div.innerHTML = data3[i];
        mainContainer.appendChild(div);
    }

}

function removeData3() {

    /*Tout effacer*/
    var data_div = document.getElementById("myData3");

    // As long as <ul> has a child node, remove it
    while (data_div.hasChildNodes()) {  
        data_div.removeChild(data_div.firstChild);

    }
}

document.querySelector("#search_box3").addEventListener("click", getDataFromCustomURL)

function getDataFromCustomURL() {

    removeData3()

    let InputConsoleName = document.querySelector("#console_id");
    const console_id_value = InputConsoleName.value;
    let rankingId = document.querySelector("#ranking_id");
    const ranking_id_value = rankingId.value;


    fetch(`http://localhost:4500/TOP?name=${console_id_value}&ranking=${ranking_id_value}`, {mode: 'cors'})
    .then(function (response) {
        console.log(response)
        return response.json();
    })
    .then(function (data3) {
        console.log("my data",data3)
        appendData3(data3);
    })
    .catch(function (err) {
        console.log(err);
    });
}
//https://httpbin.org/get