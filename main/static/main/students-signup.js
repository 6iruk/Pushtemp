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

function submit(){
  var pass = 	$("#password").val();
  var repass = $("#repass").val();

  if(pass.trim() != "" && pass === repass){
    $("#signup-button").attr("disabled",false);
  }

  else{
    $("#signup-button").attr("disabled",true);
  }
}
