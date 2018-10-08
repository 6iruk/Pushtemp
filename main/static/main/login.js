function user_type_click(user){
  if(user == 'student'){
    $("#sta-form").css("display", "none");
    $("#stu-form").css("display", "inherit");
    $("#button-1 > button").css("background-color", "#555555");
    $("#button-2 > button").css("background-color", "buttonface");
  }

  if(user == 'staff'){
    $("#stu-form").css("display", "none");
    $("#sta-form").css("display", "inherit");
    $("#button-2 > button").css("background-color", "#555555");
    $("#button-1 > button").css("background-color", "buttonface");
  }
}
