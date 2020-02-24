$(document).ready(function(){
  var sPageURL = window.location.search.substring(1);
  user_id = sPageURL.split("=")[1].substr(3, 24)
  $.get("http://localhost:5000/chat/"+user_id+"/list", function(data, status){
    $('div').append($('<ul>'));
    i = 0
    for (chat in JSON.parse(data)){
      $('ul').append($('<li><a href="chat.html?chat='+chat+'&user='+user_id+'">'+Object.values(JSON.parse(data))[i]+'</a></li>'));
      i++;
    }
  });
  $("#btn").click(function(){
    var chatname = $("#chat").val();
    if (chatname == "") {
        alert("Name must be filled out");
        return false;
    }
    $.get("http://localhost:5000/chat/create/"+chatname+"?users="+user_id, function(data, status){
        if (status == "success"){
          location.reload();
        }
    });
  });
});


