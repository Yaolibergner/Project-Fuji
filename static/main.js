// A function to get new messages from the feed and then append it to
// the message feed.
function showNewMessages(results) {
    let newMessages = results;

    // The message-display is temperory id. The idea here is to create a <div>
    // in the html with this id to show all messages. And then append new messages
    // to the <div>. 
    $('#message-display').html(newMessages);
    // Add something (if...) to change the scrollbar。If user at the bottom of the scrollbar,
    // show the scroll to the bottom. 
}

// A function to get new messages from the chat feed. 
function refreshMessages() {
  $.get('/messages', showNewMessages);
}

// Set interval to request new messages every 5 seconds with now timeout.
// A page can't be manipulated safely until the document is "ready." 
// jQuery detects this state of readiness for you. 
// Code included inside $( document ).ready() will only run once the page 
// Document Object Model (DOM) is ready for JavaScript code to execute.
// See more explaination here: http://learn.jquery.com/using-jquery-core/document-ready/ 
$(document).ready(function() {
    refreshMessages();
    setInterval(refreshMessages, 5000);
});

