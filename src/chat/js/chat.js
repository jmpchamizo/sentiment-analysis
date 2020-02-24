$(document).ready(function(){
  var sPageURL = window.location.search.substring(1);
  chat_id = sPageURL.split("&")[0].split("=")[1]
  user_id = sPageURL.split("&")[1].split("=")[1]
  uploadMessages()
  window.setInterval(uploadMessages, 1000);

  $.get("http://localhost:5000/chat/"+chat_id, function(data,status){
    $('body').prepend($('<label>'+data+'</label><br>'));
  });

  $.get("http://localhost:5000/user/"+user_id, function(data,status){
    $('body').prepend($('<label>'+data+'</label><br>'));
  });


  $("#btnAdd").click(function(){
    var username = $("#username").val();
    if (username == "") {
        alert("User must be filled out");
        return false;
    }
    newUser = $("#username").val()
    $.get("http://localhost:5000/username/"+newUser, function(data,status){
      new_user_id = data
      $.get("http://localhost:5000/chat/"+chat_id+"/adduser?user="+new_user_id, function(data,status){
        console.log(data)
        console.log("################")
        if (data == "The user is already in the chat"){
          alert(data)
        }
      });
    });
    
  });
  $("#btnSend").click(function(){
    var text = $("#message").val();
      $.ajax({
          url: "http://localhost:5000/chat/"+chat_id+"/addmessage",
          type: "POST",
          contentType: "application/json",
          data: JSON.stringify({"text": text, "user": user_id})
      }).done(function(data) {
          uploadMessages();
      });
    });
  });

function uploadMessages(){
  $.get("http://localhost:5000/chat/"+chat_id+"/messages", function(data,status){
    $("#area").empty()  
    for (d of JSON.parse(data)){
      $("#area").append(Object.values(d)[0][0]+": "+ Object.values(d)[0][1]+"\n")
    }
  });
}
