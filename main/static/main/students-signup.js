function password_checker(){
  var pass = 	$("#password").val();
  var repass = $("#repass").val();

  if(pass.trim() != "" && pass === repass){
    $("#signup-button").attr("disabled",false);
  }

  else{
    $("#signup-button").attr("disabled",true);
  }
}

function get_sections() {
    var year = $("select#year-select").children("option:selected").val();

    $.get("http://aaupush.com/json/Section?by-year=" + year, function (result,status) {
        if(status == "success"){
          if(result.status == 1) {
             $("select#section-select").html(result.html);
          }
        }
        else {
          $("#sign-up-form-notif").html("<p>Sorry, couldn't load sections</p>");
        }
      });
}

function sign_up(){
  $.post("http://aaupush.com/json/signup/", $( "#sign-up-form" ).serialize(), function (result,status) {
       if(status == "success") {
         if(result.status == 1) {
           document.location.href='/login/';
         }

         else {
           $("#sign-up-form-notif").html("<p>" + result.remark + "</p>");
         }
       }

       else {
         $("#sign-up-form-notif").html("<p>Couldn't reach server</p>");
       }
     });
}
