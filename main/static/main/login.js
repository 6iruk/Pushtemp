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

function feedback(message) {
  $('#error-feedback').html(message);
  $('#feedback-box').modal('show')    //'show' or 'hide' are also possible instead of 'toggle'
  setTimeout( function() {
    $('#feedback-box').modal('hide')    //'show' or 'hide' are also possible instead of 'toggle'
  },7000);
}


$( document ).ready(function() {

  $(".userLoginForm").show()
  $(".userForgotPasswordForm").hide()
  $(".userForgotPasswordContinue").hide()
  $(".studentForgotPasswordContinue").hide()
  $(".staffForgotPasswordContinue").hide()
  $(".userResetPasswordForm").hide()
  $(".userResetPasswordSuccess").hide()

  $('.forgotPasswordButton').click(function(){
    var elem = $( this );
    var usertype = elem.attr( "user-type" )
    if (usertype == "student"){
      //nothing here for now
    }
    else if (usertype=='staff'){
      $(".userLoginForm").hide()
      $(".userForgotPasswordForm").show()
    }
  })
  
  $("#resetAccountStaff").click(function( event ) {
    form = document.forms.namedItem("resetAccountStaffForm");
    formdata =  new FormData(form);

    $("#push-loader").css("display", "block");
    $.ajax({
    url: base_url + '/json/getrecovery/',
    data: formdata,
    processData: false,
    contentType: false,
    type: 'POST',
    dataType:'json',
    success: function (result) {
            $("#push-loader").css("display", "none");
            if(result.status == 1) {
              $("#push-loader").css("display", "none");
              $(".userForgotPasswordContinue").show()
              $(".staffForgotPasswordContinue").show()
            }

            else if(result.status == 0)  {
              $("#push-loader").css("display", "none");
              feedback('Reminder edit failed' + result.remark)
            }
        },
    error: () => {
      console.log('in error')
      $("#push-loader").css("display", "none");
      feedback('Failed please try again.')
      // $(".userForgotPasswordForm").hide() //remove at integration
      // $(".userForgotPasswordContinue").show()
      // $(".staffForgotPasswordContinue").show()
    }
      })
    })

    $(".staffForgotPasswordContinueButton").click(function( event ) {
      $(".staffForgotPasswordContinue").hide()
      $(".userResetPasswordForm").show()
    })
    
      
    $("#newPasswordButton").click(function( event ) {
      form = document.forms.namedItem("newPasswordForm");
      formdata =  new FormData(form);
      if ($("input[name='new-password']").val() == $("input[name='confirm-password']").val()){
        $("#push-loader").css("display", "block");
        $.ajax({
        url: base_url + '/json/recoverpassword/',
        data: formdata,
        processData: false,
        contentType: false,
        type: 'POST',
        dataType:'json',
        success: function (result) {
                $("#push-loader").css("display", "none");
                if(result.status == 1) {
                  $("#push-loader").css("display", "none");
                  $(".userResetPasswordForm").hide()
                  $(".userResetPasswordSuccess").show()
                }
    
                else if(result.status == 0)  {
                  $("#push-loader").css("display", "none");
                  feedback('Failed to reset password. Please try again.')
                }
            },
        error: () => {
          console.log('in error')
          $("#push-loader").css("display", "none");
          feedback('Failed. Please try again.')
          // $(".userResetPasswordForm").hide() //remove at integration
          // $(".userResetPasswordSuccess").show()
        }
          })
      }
      else {
        feedback('Passwords do not match')
      }
      })
    
})
