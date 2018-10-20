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
      var url = "http://localhost:8000/json/Post?by-type=miscellaneous";
    }

    else {
      var url = "http://localhost:8000/json/Post?by-type=class-post-list&by-class=";
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
      var url = "http://localhost:8000/json/Post?by-type=miscellaneous";
    }

    else {
      var url = "http://localhost:8000/json/Post?by-type=class-post-list&by-class=";
      url += class_id;
    }

    files.load(url);
  }
}


var add_drop_notif_timer;

function add_course() {
    $.post("http://localhost:8000/json/add_drop", $( "#add-courses-form" ).serialize(), function (result,status) {
         if(status == "success") {
           if(result.status == 1) {
             $("#course-table > tbody").append(result.html);
             clearTimeout(add_drop_notif_timer);
             $("#add-courses-form-notif > h3").html("You have added " + result.count + " courses");
             $("#add-courses-form-notif").css("display","block");

             add_drop_notif_timer = setTimeout( function() {
               $("#add-courses-form-notif").css("display", "none");
             },7000);
           }

           else {
             clearTimeout(add_drop_notif_timer);
             $("#add-courses-form-notif > h3").html(result.remark);
             $("#add-courses-form-notif").css("display","block");

             add_drop_notif_timer = setTimeout( function() {
               $("#add-courses-form-notif").css("display", "none");
             },7000);
           }
         }

         else {
           clearTimeout(add_drop_notif_timer);
           $("#add-courses-form-notif > h3").html("Action Failed");
           $("#add-courses-form-notif").css("display","block");

           add_drop_notif_timer = setTimeout( function() {
             $("#add-courses-form-notif").css("display", "none");
           },7000);
         }
       });
}



function drop_course(class_id) {
    $.post("http://localhost:8000/json/add_drop", { action_type : "drop", class : class_id, csrfmiddlewaretoken :  $( "#add-courses-form > input[name='csrfmiddlewaretoken']" ).val()}, function (result,status) {
         if(status == "success") {
           if(result.status == 1) {
             $(".row-" + result.class_id).css("display", "none");
             clearTimeout(add_drop_notif_timer);
             $("#add-courses-form-notif > h3").html("You have dropped the course " + result.course);
             $("#add-courses-form-notif").css("display","block");

             add_drop_notif_timer = setTimeout( function() {
               $("#add-courses-form-notif").css("display", "none");
             },7000);
           }

           else {
             clearTimeout(add_drop_notif_timer);
             $("#add-courses-form-notif > h3").html(result.remark);
             $("#add-courses-form-notif").css("display","block");

             add_drop_notif_timer = setTimeout( function() {
               $("#add-courses-form-notif").css("display", "none");
             },7000);
           }
         }

         else {
           clearTimeout(add_drop_notif_timer);
           $("#add-courses-form-notif > h3").html("Action Failed");
           $("#add-courses-form-notif").css("display","block");

           add_drop_notif_timer = setTimeout( function() {
             $("#add-courses-form-notif").css("display", "none");
           },7000);
         }
       });
}



function account_update(page) {
    $.post("http://localhost:8000/json/account_update", $( "#profile-update-form" ).serialize(), function (result,status) {
         if(status == "success") {
           if(result.status == 1) {
             $("#profile-form-notif > h3").html("Update Successful");
             $("#profile-form-notif").css("display", "block");

             setTimeout( function() {
               $("#profile-form-notif").css("display", "none");
             },7000);
           }

           else {
             $("#profile-form-notif > h3").html("Incorrect Password");
             $("#profile-form-notif").css("display", "block");

             setTimeout( function() {
               $("#profile-form-notif").css("display", "none");
             },7000);
           }
         }

         else {
           $("#profile-form-notif > h3").html("Update Failed");
           $("#profile-form-notif").css("display", "block");

           setTimeout( function() {
             $("#profile-form-notif").css("display", "none");
           },7000);
         }
       });
}
