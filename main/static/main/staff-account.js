base_url = "http://localhost:8000";

function nav_click(page) {
  if(page == 'post') {
    $(".content").css("display","none");
    $("#post-form").css("display","block");
    $(".side-nav-sections").css("background-color","inherit");
    $("#nav-post").css("background-color","#ffffff");
  }
  else if(page == 'tracker') {
    $(".content").css("display","none");
    $("#post-tracker").css("display","block");
    $(".side-nav-sections").css("background-color","inherit");
    $("#nav-tracker").css("background-color","#ffffff");
  }
  else if(page == 'forums') {
    $(".content").css("display","none");
    $("#forums").css("display","block");
    $(".side-nav-sections").css("background-color","inherit");
    $("#nav-tracker").css("background-color","#ffffff");
  }
  else if(page == 'message-department') {
    $(".content").css("display","none");
    $("#message-department").css("display","block");
    $(".side-nav-sections").css("background-color","inherit");
    $("#nav-group-chat").css("background-color","#ffffff");
  }
  else if(page == 'assignments') {
    $(".content").css("display","none");
    $("#assignments").css("display","block");
    $(".side-nav-sections").css("background-color","inherit");
    $("#nav-group-chat").css("background-color","#ffffff");
  }
  else if(page == 'group-chat') {
    $(".content").css("display","none");
    $("#group-chat").css("display","block");
    $(".side-nav-sections").css("background-color","inherit");
    $("#nav-group-chat").css("background-color","#ffffff");
  }
  else if(page == 'class-list') {
    $(".content").css("display","none");
    $("#class-list").css("display","block");
    $(".side-nav-sections").css("background-color","inherit");
    $("#nav-class-list").css("background-color","#ffffff");
  }
  else if(page == 'manage-department') {
    $(".content").css("display","none");
    $("#manage-department").css("display","block");
    $(".side-nav-sections").css("background-color","inherit");
    $("#nav-class-list").css("background-color","#ffffff");
  }
  else if(page == 'account-setting') {
    $(".content").css("display","none");
    $("#account-setting").css("display","block");
    $(".side-nav-sections").css("background-color","inherit");
    $("#nav-account-setting").css("background-color","#ffffff");
  }

  else if(page == 'log-out') {
    document.location.href='/login/';
  }
}

function click_hidden(page) {
  var list = $("#" + page);

  if(list.css("display") == "none")
    list.css("display", "block");
  else {
    list.css("display", "none");
  }
}

function post_action(action) {
    if(action == "chat") {
      form = document.forms.namedItem("group-chat-post-form");
      formdata =  new FormData(form);

      $("#push-loader").css("display", "block");
      $.ajax({
      url: base_url + '/json/post_action/',
      data: formdata,
      processData: false,
      contentType: false,
      type: 'POST',
      dataType:'json',
      success: function (result) {
              console.log(result)
             $("#push-loader").css("display", "none");
             if(result.status == 1) {
               $("#chat-post-list").prepend(result.html);
               $("#group-chat-post-notif").html("<span>Post Successful</span>");
               $("#group-chat-post-notif").css("display", "block");
               $(".error").css("display", "none");
               $("#group-chat-form-reset").click();

               setTimeout( function() {
                 $("#group-chat-post-notif").css("display", "none");
               },7000);
             }

             else if(result.status == 0)  {
               $(".error").css("display", "none");
               $(result.id).html(result.html);
               $(result.id).css("display", "block");
             }
         },
       error: function(result){
        console.log(result)
         $("#push-loader").css("display", "none");
         $("#group-chat-post-notif").html("<p>Post Failed</p>");
         $("#group-chat-post-notif").css("display", "block");

         setTimeout( function() {
           $("#group-chat-post-notif").css("display", "none");
         },7000);
       }});

         return;
    }

    form = document.forms.namedItem("post-form-form");
    formdata =  new FormData(form);;

    $("#push-loader").css("display", "block");
    $.ajax({
    url: base_url + '/json/post_action/',
    data: formdata,
    processData: false,
    contentType: false,
    type: 'POST',
    dataType:'json',
    success: function (result) {
           $("#push-loader").css("display", "none");
           if(result.status == 1) {
             $("#post-form-notif > span").html("Post Successful");
             $("#post-form-notif").css("display", "block");
             $(".error").css("display", "none");
             $("#post-form-reset").click();

             setTimeout( function() {
               $("#post-form-notif").css("display", "none");
             },7000);
           }

           else if(result.status == 0)  {
             $(".error").css("display", "none");
             $(result.id).html(result.html);
             $(result.id).css("display", "block");
           }
       },
      error: function (){
        $("#push-loader").css("display", "none");
        $("#post-form-notif > span").html("Post Failed");
        $("#post-form-notif").css("display", "block");

        setTimeout( function() {
          $("#post-form-notif").css("display", "none");
        },7000);
      }
     });
}

function set_reminder(){
    $("#push-loader").css("display", "block");
    $.post(base_url + "/json/setreminder/", $( "#set-reminder-form" ).serialize(), function (result,status) {
      $("#push-loader").css("display", "none");
      if(status == "success") {
        if(result.status == 0) {
          $(".error").css("display","none");
          $("#" + result.id).html(result.html);
          $("#" + result.id).css("display","block");
        }

         else if(result.status == 1) {
          $(".error").css("display","none");
          $("#profile-form-notif > span").html("Update Successful");
          $("#profile-form-notif").css("display", "block");
          document.location.href='/staff/account/';
        }
      }

      else {
        $("#profile-form-notif > span").html("Update Failed");
        $("#profile-form-notif").css("display", "block");

        setTimeout( function() {
          $("#profile-form-notif").css("display", "none");
        },7000);
      }
       });
}

var add_notif_timer;

function add_course() {
    $("#push-loader").css("display", "block");
    $.post(base_url + "/json/add_drop/", $( "#add-courses-form" ).serialize(), function (result,status) {
         $("#push-loader").css("display", "none");
         if(status == "success") {
           if(result.status == 1) {
             $("#class-table > tbody").append(result.html);
             clearTimeout(add_notif_timer);
             $("#add-courses-form-notif > span").html("You have added " + result.count + " courses");
             $("#add-courses-form-notif").css("display","block");
             document.location.href='/staff/account';

           }

           else {
             clearTimeout(add_notif_timer);
             $("#add-courses-form-notif > span").html(result.remark);
             $("#add-courses-form-notif").css("display","block");

             add_notif_timer = setTimeout( function() {
               $("#add-courses-form-notif").css("display", "none");
             },7000);
           }
         }

         else {
           clearTimeout(add_notif_timer);
           $("#add-courses-form-notif > span").html("Action Failed");
           $("#add-courses-form-notif").css("display","block");

           add_notif_timer = setTimeout( function() {
             $("#add-courses-form-notif").css("display", "none");
           },7000);
         }
       });
}

var drop_notif_timer;

function drop_course(class_id) {
  $("#push-loader").css("display", "block");
  $.post(base_url + "/json/add_drop/", { action_type : "drop", class : class_id, csrfmiddlewaretoken :  $( "#add-courses-form > input[name='csrfmiddlewaretoken']" ).val()}, function (result,status) {
       $("#push-loader").css("display", "none");
       if(status == "success") {
         if(result.status == 1) {
           $(".row-" + result.class_id).css("display", "none");
           clearTimeout(drop_notif_timer);
           if(result.class_id == '-1') {
             $("#drop-courses-form-notif > span").html("You don't take that course");
           }

           else {
             $("#drop-courses-form-notif > span").html("You have dropped the course " + result.course);
             $("#drop-courses-form-notif").css("display","block");
             document.location.href='/staff/account';
           }

           $("#drop-courses-form-notif").css("display","block");

           drop_notif_timer = setTimeout( function() {
             $("#drop-courses-form-notif").css("display", "none");
           },7000);
         }

         else {
           clearTimeout(drop_notif_timer);
           $("#drop-courses-form-notif > span").html(result.remark);
           $("#drop-courses-form-notif").css("display","block");

           drop_notif_timer = setTimeout( function() {
             $("#drop-courses-form-notif").css("display", "none");
           },7000);
         }
       }

       else {
         clearTimeout(drop_notif_timer);
         $("#drop-courses-form-notif > span").html("Action Failed");
         $("#drop-courses-form-notif").css("display","block");

         drop_notif_timer = setTimeout( function() {
           $("#drop-courses-form-notif").css("display", "none");
         },7000);
       }
     });
}



function account_update() {
    $("#push-loader").css("display", "block");
    $.post(base_url + "/json/account_update/", $( "#profile-update-form" ).serialize(), function (result,status) {
      $("#push-loader").css("display", "none");
      if(status == "success") {
        if(result.status == 0) {
          feedback('error')
          $(".error").css("display","none");
          $("#" + result.id).html(result.html);
          $("#" + result.id).css("display","block");
        }

         else if(result.status == 1) {
          feedback('success')
           $(".error").css("display","none");
          $("#profile-form-notif > span").html("Update Successful");
          $("#profile-form-notif").css("display", "block");
          document.location.href='/staff/account/';
        }

        else if(result.status == 2) {
          feedback('2')
          $(".error").css("display","none");
          $("#profile-form-notif > span").html(result.remark);
          $("#profile-form-notif").css("display", "block");

          setTimeout( function() {
            $("#profile-form-notif").css("display", "none");
          },7000);
        }
        else if(result.status == 3) {
          feedback('3')
          $(".error").css("display","none");
          $("#profile-form-notif > span").html(result.remark);
          $("#profile-form-notif").css("display", "block");

          setTimeout( function() {
            $("#profile-form-notif").css("display", "none");
          },7000);
        }
      }

      else {
        $("#profile-form-notif > span").html("Update Failed");
        $("#profile-form-notif").css("display", "block");

        setTimeout( function() {
          $("#profile-form-notif").css("display", "none");
        },7000);
      }
       });
}

function feedback(message) {
  $('#error-feedback').html(message);
  $('#feedback-box').modal('show')    //'show' or 'hide' are also possible instead of 'toggle'
  setTimeout( function() {
    $('#feedback-box').modal('hide')    //'show' or 'hide' are also possible instead of 'toggle'
  },7000);
}

$( document ).ready(function() {
  
  //Edit Post
  $(".submitEditPost").click(function( event ) {
    var elem = $( this );
    console.log('in submitEditPost ',elem.attr( "id" ))
    var postid = elem.attr( "id" )
    form = document.forms.namedItem("editModal"+postid);
    formdata =  new FormData(form);

    $("#push-loader").css("display", "block");
    $.ajax({
    url: base_url + '/json/edit_post/',
    data: formdata,
    processData: false,
    contentType: false,
    type: 'POST',
    dataType:'json',
    success: function (result) {
            $("#push-loader").css("display", "none");
            if(result.status == 1) {
              $("#push-loader").css("display", "none");
              feedback('Your post has been edited successfully! Refresh to update.')
            }

            else if(result.status == 0)  {
              $("#push-loader").css("display", "none");
              feedback('Post edit failed')
            }
        },
    error: () => {
      $("#push-loader").css("display", "none");
      feedback('failed')
    }
      })
  })

  //Delete Post
  $(".submitDeletePost").click(function( event ) {
    var elem = $( this );
    var postid = elem.attr( "id" )
    console.log('About to delete:', postid)

    $("#push-loader").css("display", "block");
    $.ajax({
    url: base_url + '/json/delete_post/?post-id='+postid,
    processData: false,
    contentType: false,
    type: 'GET',
    dataType:'json',
    success: function (result) {
            $("#push-loader").css("display", "none");
            if(result.status == 1) {
              $("#push-loader").css("display", "none");
              feedback('Your post has been deleted. Refresh to update.')
            }

            else if(result.status == 0)  {
              $("#push-loader").css("display", "none");
              feedback('Post delete failed')
            }
        },
    error: () => {
      $("#push-loader").css("display", "none");
      feedback('failed')
    }
      })
  })

  //Edit Reminder
  $(".submitEditReminder").click(function( event ) {
    var elem = $( this );
    console.log('in submitEditReminder ',elem.attr( "id" ))
    var postid = elem.attr( "id" )
    form = document.forms.namedItem("editReminderForm"+postid);
    formdata =  new FormData(form);

    $("#push-loader").css("display", "block");
    $.ajax({
    url: base_url + '/json/edit_reminder/',
    data: formdata,
    processData: false,
    contentType: false,
    type: 'POST',
    dataType:'json',
    success: function (result) {
            $("#push-loader").css("display", "none");
            if(result.status == 1) {
              $("#push-loader").css("display", "none");
              feedback('Your reminder has been edited successfully! Refresh to update.' + result.remark)
            }

            else if(result.status == 0)  {
              $("#push-loader").css("display", "none");
              feedback('Reminder edit failed' + result.remark)
            }
        },
    error: () => {
      $("#push-loader").css("display", "none");
      feedback('failed' + result.remark)
    }
      })
  })

  //Delete reminder
  $(".submitDeleteReminder").click(function( event ) {
    var elem = $( this );
    var postid = elem.attr( "id" )
    form = document.forms.namedItem("deleteReminderModal"+postid);
    formdata =  new FormData(form);

    $("#push-loader").css("display", "block");
    $.ajax({
    url: base_url + '/json/delete_reminder/?reminder-id='+postid,
    processData: false,
    contentType: false,
    type: 'GET',
    dataType:'json',
    success: function (result) {
            $("#push-loader").css("display", "none");
            if(result.status == 1) {
              $("#push-loader").css("display", "none");
              feedback('Your post has been deleted. Refresh to update.')
            }

            else if(result.status == 0)  {
              $("#push-loader").css("display", "none");
              feedback('Post delete failed')
            }
        },
    error: () => {
      $("#push-loader").css("display", "none");
      feedback('failed')
    }
      })
  })


  //submit dean message
  $(".submitDeanMessage").click(function( event ) {
    var elem = $( this );
    form = document.forms.namedItem("deanMessageDepartment");
    formdata =  new FormData(form);

    $("#push-loader").css("display", "block");
    $.ajax({
    url: base_url + '/json/post_action/',
    data: formdata,
    processData: false,
    contentType: false,
    type: 'POST',
    dataType:'json',
    success: function (result) {
            $("#push-loader").css("display", "none");
            if(result.status == 1) {
              $("#push-loader").css("display", "none");
              feedback('Your post has been edited successfully!')
            }

            else if(result.status == 0)  {
              $("#push-loader").css("display", "none");
              feedback('Post edit failed')
            }
        },
    error: () => {
      $("#push-loader").css("display", "none");
      feedback('failed')
    }
      })
  })

  //assignmment submit modal
  $(".submitAssignmentModal").click(function( event ) {
    var elem = $( this );
    var id = elem.attr('postid')
    form = document.forms.namedItem("submitAssignmentForm"+id);
    formdata =  new FormData(form);

    $("#push-loader").css("display", "block");
    $.ajax({
    url: base_url + '/json/submitassignment/',
    data: formdata,
    processData: false,
    contentType: false,
    type: 'POST',
    dataType:'json',
    success: function (result) {
            $("#push-loader").css("display", "none");
            if(result.status == 1) {
              $("#push-loader").css("display", "none");
              feedback('Your post has been edited successfully!')
            }

            else if(result.status == 0)  {
              $("#push-loader").css("display", "none");
              feedback('Post edit failed')
            }
        },
    error: () => {
      $("#push-loader").css("display", "none");
      feedback('failed')
    }
      })
  })

  //invite instructor
  $(".inviteInstructorButton").click(function( event ) {
    form = document.forms.namedItem("inviteInstructorForm");
    formdata =  new FormData(form);

    $("#push-loader").css("display", "block");
    $.ajax({
    url: base_url + '/json/inviteinstructor/',
    data: formdata,
    processData: false,
    contentType: false,
    type: 'POST',
    dataType:'json',
    success: function (result) {
      console.log("in success")
            $("#push-loader").css("display", "none");
            if(result.status == 0) {
              console.log("0")
              $("#push-loader").css("display", "none");
              console.log(result.remark)
              feedback(result.remark)
            }
            else if(result.status == 1)  {
              console.log("1")
              $("#push-loader").css("display", "none");
              console.log(result.remark)
            }
            else if(result.status == 2)  {
              console.log("2")
              $("#push-loader").css("display", "none");
              console.log(result.remark)
            }
            else if (result.status==3) {
              console.log("3")
              $("#push-loader").css("display", "none");
              console.log(result.remark)
            }
        },
    error: () => {
      $("#push-loader").css("display", "none");
      feedback('failed')
      console.log("error")
    }
      })
      console.log("sent request")
  })


  //recover password
  $(".inviteInstructorButton").click(function( event ) {
    form = document.forms.namedItem("inviteInstructorForm");
    formdata =  new FormData(form);

    $("#push-loader").css("display", "block");
    $.ajax({
    url: base_url + '/json/inviteinstructor/',
    data: formdata,
    processData: false,
    contentType: false,
    type: 'POST',
    dataType:'json',
    success: function (result) {
      console.log("in success")
            $("#push-loader").css("display", "none");
            if(result.status == 0) {
              console.log("0")
              $("#push-loader").css("display", "none");
              console.log(result.remark)
              feedback(result.remark)
            }
            else if(result.status == 1)  {
              console.log("1")
              $("#push-loader").css("display", "none");
              console.log(result.remark)
            }
            else if(result.status == 2)  {
              console.log("2")
              $("#push-loader").css("display", "none");
              console.log(result.remark)
            }
            else if (result.status==3) {
              console.log("3")
              $("#push-loader").css("display", "none");
              console.log(result.remark)
            }
        },
    error: () => {
      $("#push-loader").css("display", "none");
      feedback('failed')
      console.log("error")
    }
      })
      console.log("sent request")
  })

});

function email_exists(){
  var elem = $( this );
  var email = elem.attr('email')
  $.ajax({
    url: base_url + '/json/email_exists/?email='+email,
    data: formdata,
    processData: false,
    contentType: false,
    type: 'POST',
    dataType:'json',
    });

}
