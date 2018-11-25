function login(user){
  if(user == "student") {
    $.post("http://www.aaupush.com/json/login/", $( "#student-login" ).serialize(), function (result,status) {
         if(status == "success") {
           if(result.status == 0) {
             $(".error").css("display", "none");
             $("#student-form-error").html("<p>Incorrect Registration ID or password</p>");
             $("#student-form-error").css("display", "block");
           }

           if(result.status == 1) {
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
    $.post("http://www.aaupush.com/json/login/", $( "#staff-login" ).serialize(), function (result,status) {
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
         }

         else {
           $("#staff-form-error").html("<p>Couldn't reach server</p>");
           $("#staff-form-error").css("display", "block");
         }
       });
  }
}
