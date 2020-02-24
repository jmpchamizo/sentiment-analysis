$(document).ready(function(){
  $("#btn").click(function(){
    var username = $("#user").val();
    if (username == "") {
        alert("Name must be filled out");
        return false;
    }
    $.get("http://localhost:5000/user/create/"+username, function(data, status){
        if (status == "success"){
            $(window.location).attr('href', 'chats.html?user='+data);
        }
    });
  });
});