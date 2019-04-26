base_url = "http://localhost:8000";

function load_forums(){
    //const data={name="addis", id:23}
    $.ajax({
        url: base_url + '/api/forums/',
        type: "GET", //or POST
        //data: data, //if type is POST
        //dataType: JSON or HTML, XML or TXT, jsonp
        success: function(result){

        },
        error: function(result){

        }
    })
}

function search_forum(){
    $.getJSON(base_url, function(result){

    });
}

function create_forum(){
    $.getJSON(base_url, function(result){

    });
}

function load_forum_messages(){
    $.getJSON(base_url, function(result){

    });
}

function send_forum_message(){
    $.getJSON(base_url, function(result){

    });
}
