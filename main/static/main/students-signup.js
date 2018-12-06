base_url = "https://www.aaupush.com";

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
    $("#push-loader").css("display", "block");
    $.get(base_url + "/json/Section?by-year=" + year, function (result,status) {
        $("#push-loader").css("display", "none");

        if(status == "success"){
          if(result.status == 1) {
             $("select#section-select").html(result.html);
          }
        }
        else {
          $("#sign-up-form-notif").html("<p>Sorry, couldn't load sections</p>");
          $("#sign-up-form-notif").css("display","block");
        }
      });
}

function sign_up(){
  var pass = 	$("#password").val();
  var repass = $("#repass").val();

  if(pass.trim() != "" && pass === repass) {
  $("#push-loader").css("display", "block");
  $.post(base_url + "/json/signup/", $( "#sign-up-form" ).serialize(), function (result,status) {
       $("#push-loader").css("display", "none");

       if(status == "success") {
         if(result.status == 1) {
           document.location.href='/login/';
         }

         else {
           $("#sign-up-form-notif").html("<p>" + result.remark + "</p>");
           $("#sign-up-form-notif").css("display","block");
         }
       }

       else {
         $("#sign-up-form-notif").html("<p>Couldn't reach server</p>");
         $("#sign-up-form-notif").css("display","block");
       }
     });
   }

   else {
     $("#password-notif").html("Passwords don't match");
   }
}
