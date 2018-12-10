// NLP
var nlp = window.nlp_compromise;

var requestURL = 'data/qa.json';
var request = new XMLHttpRequest();

request.open('GET', requestURL);
request.responseType = 'json';
request.send();

var messages = [],
  lastUserMessage = "",
  botMessage = "",
  botName = 'Chatbot',
  talking = false;

function chatbotResponse() {
  talking = false;
  //message when don't know answer
  botMessage = "I don't know";

  if (lastUserMessage === 'hi' || lastUserMessage === 'hello') {
    botMessage = 'Hi!';
  }
  if (lastUserMessage === 'what is your name') {
    botMessage = 'My name is ' + botName;
  }
}

function newEntry() {
  if (document.getElementById("chatbox").value != "") {
    lastUserMessage = document.getElementById("chatbox").value;
    document.getElementById("chatbox").value = "";

    //push user msg
    messages.push(lastUserMessage);
    var parU = document.createElement("p");
    parU.setAttribute("class", "chatlogUser");
    var msgU = document.createTextNode(lastUserMessage);
    parU.appendChild(msgU);
    document.getElementById("chatlog").appendChild(parU);


    // //get answer
    // chatbotResponse();
    // messages.push("<b>" + botName + ":</b> " + botMessage);
    
    // //push bot msg
    // var parB = document.createElement("p");
    // parB.setAttribute("class", "chatlogBot");
    // var msgB = document.createTextNode(botMessage);
    // parB.appendChild(msgB);
    // document.getElementById("chatlog").appendChild(parB);



    // var sentence = nlp(lastUserMessage);
    // var output = ''; 
    // for (var i = 0; i < sentence.terms().length; i++) {
    //   var nounWord = sentence.terms(i).nouns().out();
    //   if (nounWord != '') {
    //     nounWord = nlp(nounWord).nouns().toPlural().out()
    //     output += nounWord;
    //   } 
    //     output += sentence.terms(i).out();
    // }

    // output = sentence.nouns().toPlural().all().out();
    // output = nlp(output).verbs().toFutureTense().all().out();

    // var parB = document.createElement("p");
    // parB.setAttribute("class", "chatlogBot");
    // var msgB = document.createTextNode(output);
    // parB.appendChild(msgB);
    // document.getElementById("chatlog").appendChild(parB);


    //Test DB
    var data = request.response;

    for (var i = 0; i < data.length; i++) {
      if (data[i]["question"] == lastUserMessage) {
        botMes = data[i]["answer"];
        break;
      } else {
        botMes = "I don't know";
      }
    }
    var parB = document.createElement("p");
    parB.setAttribute("class", "chatlogBot");
    var msgB = document.createTextNode(botMes);
    parB.appendChild(msgB);
    document.getElementById("chatlog").appendChild(parB);

    //scroll to bottom
    var objDiv = document.getElementById("chatlog");
    objDiv.scrollTop = objDiv.scrollHeight;
  }
}

document.onkeypress = keyPress;

function keyPress(e) {
  var x = e || window.event;
  var key = (x.keyCode || x.which);
  if (key == 13) {
    newEntry();
  }
}

function placeHolder() {
  document.getElementById("chatbox").placeholder = "";
}


