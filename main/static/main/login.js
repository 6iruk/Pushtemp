base_url = "http://localhost:8000";

function login(user){
  if(user == "student") {
    $("#push-loader").css("display", "block");
    $.post(base_url + "/json/login/", $( "#student-login" ).serialize(), function (result,status) {
         $("#push-loader").css("display", "none");

         if(status == "success") {
           if(result.status == 0) {
             $(".error").css("display", "none");
             $("#student-form-error").html("<p>Incorrect Registration ID or password</p>");
             $("#student-form-error").css("display", "block");
           }

           else if(result.status == 1) {
             $(".error").css("display", "none");
              document.location.href='/student/account/';
           }

           else if(result.status == 2){
             $(".error").css("display", "none");
             $("#" + result.id).html(result.html);
             $("#" + result.id).css("display", "block");
           }

           else if(result.status == 3) {
             $(".error").css("display", "none");
             $("#student-form-error").html("<p>Account not active</p>");
             $("#student-form-error").css("display", "block");
           }

           else if(result.status == 4) {
             $(".error").css("display", "none");
             $("#student-form-error").html("<p>User type not found</p>");
             $("#student-form-error").css("display", "block");
           }
         }

         else {
           $("#student-form-error").html("<p>Couldn't reach server</p>");
           $("#student-form-error").css("display", "block");
         }
       });
  }

  else if(user == "staff") {
    $("#push-loader").css("display", "block");
    $.post(base_url + "/json/login/", $( "#staff-login" ).serialize(), function (result,status) {
         $("#push-loader").css("display", "none");

         if(status == "success") {
           if(result.status == 0) {
             $(".error").css("display", "none");
             $("#staff-form-error").html("<p>Incorrect Email or password</p>");
             $("#staff-form-error").css("display", "block");
           }

           else if(result.status == 1) {
             $(".error").css("display", "none");
              document.location.href='/staff/account/'
           }

           else if(result.status == 2){
             $(".error").css("display", "none");
             $("#" + result.id).html(result.html);
             $("#" + result.id).css("display", "block");
           }

           else if(result.status == 3) {
             $(".error").css("display", "none");
             $("#staff-form-error").html("<p>Account not active</p>");
             $("#staff-form-error").css("display", "block");
           }

           else if(result.status == 4) {
             $(".error").css("display", "none");
             $("#staff-form-error").html("<p>User type not found</p>");
             $("#staff-form-error").css("display", "block");
           }

           else if(result.status == 5) {
             $(".error").css("display", "none");
             document.location.href='/first_login/'
           }
         }

         else {
           $("#staff-form-error").html("<p>Couldn't reach server</p>");
           $("#staff-form-error").css("display", "block");
         }
       });
  }
}
