// A function to get new messages from the feed and then refresh
// the message feed.
function showNewMessages(results) {
    let newMessages = results;

    // Add something (if...) to change the scrollbar。
    // If user at the bottom of the scrollbar,
    // show the scroll to the bottom. 
    // setting display area to be.
    let displayer = $('#message-display');
    
    // define atBottom status. scrollHeight is the total displayer size.
    // scrollTop is the amount of scroll user has done.
    // clientHeight is the amount of displayer an user sees.
    // http://api.jquery.com/prop/
    let atBottom = displayer.scrollTop() === 
        displayer.prop('scrollHeight') - displayer.prop('clientHeight');
    // debugger;
    // Create a <div> in the html with this id to show all messages. 
    // And then add new messages to the <div>. 
    // Update the message.
    $('#message-display').html(newMessages);

    // make sure to show bottom. 
    if (atBottom) {
        displayer.scrollTop(displayer.prop('scrollHeight'));
    } 
}


// A function to get new messages from the chat feed. 
function refreshMessages() {
  $.get('/messages', showNewMessages);
}

// Set interval to request new messages every 5 seconds with now timeout.
// A page can't be manipulated safely until the document is "ready." 
// jQuery detects this state of readiness for you. .ready() to make sure Jquery is ready.
// Code included inside $( document ).ready() will only run once the page 
// Document Object Model (DOM) is ready for JavaScript code to execute.
// See more explaination here: http://learn.jquery.com/using-jquery-core/document-ready/ 
$(document).ready(function() {
    // Call refreshMessage to make better user experience so that there's no 5
    // seconds delay.
    refreshMessages();
    setInterval(refreshMessages, 5000);
    // Anything reference Jquery has to be called under the .ready() function. 
    $("#add-message").on("submit", submitMessage);
});


// add event onSubmit to call add user sent message to feedpage without reload
// feedpage. Bug#1: feedpage route return an empty "". It made feedpage show
// blank as well. However, message is successfully added to database, as well 
// as added to the page when reload. 

function showSentText() {
    // Clear textarea.
    refreshMessages(); 
    $("#new_message").val("");
}

function submitMessage(evt) {
    evt.preventDefault();
    let formInput={
        "message": $("#new_message").val()
  };
    // This is to not allow user to send empty message.  
    if ($("#new_message").val() !== "") {
        $.post('/feedpage', formInput, showSentText);}
}



