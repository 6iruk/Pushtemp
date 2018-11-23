function nav_click(page) {
  if(page == 'push-board') {
    $(".content").css("display","none");
    $("#push-board-content").css("display","block");
    $(".side-nav-sections").css("background-color","inherit");
    $("#nav-push-board").css("background-color","#ffffff");
  }

  else if(page == 'your-wall') {
    $(".content").css("display","none");
    $("#your-wall-content").css("display","block");
    $(".side-nav-sections").css("background-color","inherit");
    $("#nav-your-wall").css("background-color","#ffffff");
  }

  else if(page == 'course-bucket') {
    $(".content").css("display","none");
    $("#course-bucket-content").css("display","block");
    $(".side-nav-sections").css("background-color","inherit");
    $("#nav-course-bucket").css("background-color","#ffffff");
  }

  else if(page == 'add-drop') {
    $(".content").css("display","none");
    $("#add-drop-content").css("display","block");
    $(".side-nav-sections").css("background-color","inherit");
    $("#nav-add-drop").css("background-color","#ffffff");
  }

  else if(page == 'account-setting') {
    $(".content").css("display","none");
    $("#account-setting-content").css("display","block");
    $(".side-nav-sections").css("background-color","inherit");
    $("#nav-account-setting").css("background-color","#ffffff");
  }

  else if(page == 'log-out') {
    document.location.href='/login/'
  }
}



function click_hidden(page) {
  var list = $("#" + page);

  if(list.css("display") == "none") {
    list.css("display", "block");
  }

  else {
    list.css("display", "none");
  }
}



function course_click(page,class_id) {
  var files = $("#" + page);

  $(".course-files").css("display", "none");
  files.css("display", "block");

  if(!files.hasClass("populated")) {
    files.html("<div><img src='/static/main/loading_image.gif'/></div>");

    if( page == "miscellaneous-files") {
      var url = "http://www.aaupush.com/json/Post?by-type=miscellaneous";
    }

    else {
      var url = "http://www.aaupush.com/json/Post?by-type=class-post-list&by-class=";
      url += class_id;
    }

    files.load(url, function (result,status) {
      if(status == "success"){
        files.addClass("populated");
      }

      else {
        files.html("<div>Sorry couldnt load files. Try again</div>");
      }
    });
  }

  else {
    if( page == "miscellaneous-files") {
      var url = "http://www.aaupush.com/json/Post?by-type=miscellaneous";
    }

    else {
      var url = "http://www.aaupush.com/json/Post?by-type=class-post-list&by-class=";
      url += class_id;
    }

    files.load(url);
  }
}


var add_notif_timer;

function add_course() {
    $.post("http://www.aaupush.com/json/add_drop/", $( "#add-courses-form" ).serialize(), function (result,status) {
         if(status == "success") {
           if(result.status == 1) {
             $("#course-table > tbody").append(result.html);
             clearTimeout(add_notif_timer);
             $("#add-courses-form-notif > span").html("You have added " + result.count + " courses");
             $("#add-courses-form-notif").css("display","block");

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
    $.post("http://www.aaupush.com/json/add_drop/", { action_type : "drop", class : class_id, csrfmiddlewaretoken :  $( "#add-courses-form > input[name='csrfmiddlewaretoken']" ).val()}, function (result,status) {
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



function account_update(page) {
    $.post("http://www.aaupush.com/json/account_update/", $( "#profile-update-form" ).serialize(), function (result,status) {
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

function read(post) {
  $.post("http://www.aaupush.com/json/student_read/", { post : post, csrfmiddlewaretoken :  $( "#add-courses-form > input[name='csrfmiddlewaretoken']" ).val()}, function (result,status) {
       if(status == "success") {
         if(result.status == 1) {
           $(".read-post-" + post).css("display", "none");
         }
       }
     });
}
