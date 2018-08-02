/// A function to get new messages from the feed and then append it to
/// the message feed.
function showNewMessages(results) {
    let newMessages = results;

    /// The message-display is temperory id. The idea here is to create a <div>
    /// in the html with this id to show all messages. And then append new messages
    /// to the <div>. 
    $('#message-display').append(newMessages);
}

/// A function to get new messages from the chat feed. 
function refreshMessages() {
  $.get('/messages', showNewMessages);
}

/// Set interval to request new messages every 5 seconds with now timeout.
setInterval(refreshMessages, 5000);