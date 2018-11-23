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
  else if(page == 'account-setting') {
    $(".content").css("display","none");
    $("#account-setting").css("display","block");
    $(".side-nav-sections").css("background-color","inherit");
    $("#nav-account-setting").css("background-color","#ffffff");
  }
  
  else if(page == 'log-out') {
    document.location.href='/login/'
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

      $.ajax({
      url: 'http://aaupush.com/json/post_action/',
      data: formdata,
      processData: false,
      contentType: false,
      type: 'POST',
      dataType:'json',
      success: function (result) {
             if(result.status == 1) {
               $("#chat-post-list").append(result.html);
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

    $.ajax({
    url: 'http://aaupush.com/json/post_action/',
    data: formdata,
    processData: false,
    contentType: false,
    type: 'POST',
    dataType:'json',
    success: function (result) {
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
        $("#post-form-notif > span").html("Post Failed");
        $("#post-form-notif").css("display", "block");

        setTimeout( function() {
          $("#post-form-notif").css("display", "none");
        },7000);
      }
     });
}

var add_notif_timer;

function add_course() {
    $.post("http://aaupush.com/json/add_drop/", $( "#add-courses-form" ).serialize(), function (result,status) {
         if(status == "success") {
           if(result.status == 1) {
             $("#class-table > tbody").append(result.html);
             clearTimeout(add_notif_timer);
             $("#add-courses-form-notif > span").html("You have added " + result.count + " courses");
             $("#add-courses-form-notif").css("display","block");
             $("#add-class-form-reset").click();

             add_notif_timer = setTimeout( function() {
               $("#add-courses-form-notif").css("display", "none");
             },7000);
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
  $.post("http://aaupush.com/json/add_drop/", { action_type : "drop", class : class_id, csrfmiddlewaretoken :  $( "#add-courses-form > input[name='csrfmiddlewaretoken']" ).val()}, function (result,status) {
       if(status == "success") {
         if(result.status == 1) {
           $(".row-" + result.class_id).css("display", "none");
           clearTimeout(drop_notif_timer);
           if(result.class_id == '-1') {
             $("#drop-courses-form-notif > span").html("You don't take that course");
           }

           else {
             $("#drop-courses-form-notif > span").html("You have dropped the course " + result.course);
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
    $.post("http://aaupush.com/json/account_update/", $( "#profile-update-form" ).serialize(), function (result,status) {
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

          setTimeout( function() {
            $("#profile-form-notif").css("display", "none");
          },7000);
        }

        else if(result.status == 2) {
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
