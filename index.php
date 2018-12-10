<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Chatbot</title>
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <script src="script/script.js" type="text/javascript" charset="utf-8" async defer></script>

    <!-- NLP -->
    <script src="https://unpkg.com/compromise"></script>
</head>
<body>
    <div id='bodybox'>
        <center><h3>LORT - CHATBOT</h3></center>
        <div id='chatlog'>
            <p class="chatlogBot">Hi, what I can do for you?</p>
            <!-- Conversation here -->
        </div>
        <div class="form-wrapper cf">
            <input type="text" name="chat" id="chatbox" placeholder="Hi! Type here to ask me." onfocus="placeHolder()">
            <button onclick="newEntry()">Send</button>
        </div>
    </div>
</body>
</html>