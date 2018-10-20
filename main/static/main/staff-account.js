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
}

function click_hidden(page) {
  var list = $("#" + page);

  if(list.css("display") == "none")
    list.css("display", "block");
  else {
    list.css("display", "none");
  }
}

function course_click(page) {
  var files = $("#" + page);

  if(files.html() == "") {

  }

  $(".course-files").css("display", "none");
  files.css("display", "inherit");

}
