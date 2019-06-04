base_url = "http://localhost:8000";

$(document).ready(function(){
    
    var csrftoken = Cookies.get('csrftoken');
    
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        async: false,
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    //Fetch user forum
    function forumTitle(forum){
        console.log("In forumTitleForum: ", forum);
        var title = document.createElement("div");
        title.innerHTML = "<a>" + forum.name + "</a>"
        title.setAttribute("class", "link font-weight-bold mt-2 forum-name");
        title.setAttribute("id", "Forum"+forum.id);
        title.setAttribute("forumid", forum.id);
        return title;
    }

    $.get(base_url+"/api/forum/forumlist", function(data){
        $("#push-loader").show();
        $.each(data, function(index, value){
            $("#user-forums").append(forumTitle(value));
        });
    })
    .done(function(){
        $("#push-loader").hide();
    })
    .fail(function(jqxhr, status, exception) {
            alert( exception );
        });

    //Fetch trending forum
    $.get(base_url+"/api/forum/trendingforums/", function(data){
        $("#push-loader").show();
        $.each(data, function(index, value){
            $("#trending-forums").append(forumTitle(value));
        });
    })
    .done(function(){
        $("#push-loader").hide();
    })
    .fail(function(jqxhr, status, exception) {
        alert( exception );
      });
    
    $("#forum-home").slideDown("slow");



    //Open Forum

    function messageFetch(forumid){

        $("#forum-messages").empty(); //clear the messages area

        function forumMessage(value){
            var message = document.createElement("p");
            message.innerText = value.content;
            return message;
        }

        $.get(base_url+"/api/forum/forummessages", {'forum-id': forumid},function(data){
            console.log("Forum data: ",data)
            $("#push-loader").show();
            $.each(data, function(index, value){
                $("#forum-messages").append(forumMessage(value));
            });
            $("#forum-message-id").attr("value", forumid);
            $("#leave-forum-button").attr("forumid", forumid)
        })
        .done(function(){
            $("#push-loader").hide();
        })
        .fail(function(jqxhr, status, exception) {
                alert( exception );
            });
    }

    $(".forum-name").click(function(){
        $("#push-loader").show();
        $(".forum-content").hide();

        //fetch and render messages here
        forumid = this.getAttribute("forumid")
        console.log("forumid: ", forumid)
        messageFetch(forumid);

        $("#forum-feed").slideDown("slow");
        $("#push-loader").hide();
    });

    //Send Message
    $("#forum-send").on("submit", function(){
        var form = $(this);
        var formdata = false;
        if (window.FormData){
            formdata = new FormData(form[0]);
        }
        var formAction = form.attr('action');
        $.ajax({
            url         : base_url+"/api/forum/sendmessage/",
            data        : formdata ? formdata : form.serialize(),
            cache       : false,
            contentType : false,
            processData : false,
            type        : 'POST',
            success     : function(data, textStatus, jqXHR){
                alert("success");
            },
            fail: function(data, textStatus, jqXHR){
                alert("failed");
            }
        });
        form.trigger("reset");
        messageFetch(forumid);
    })

    //Leave Forum
    $("#leave-forum-button").click(function(){

        forumid = this.getAttribute("forumid");

        $.get( base_url+"/api/forum/leaveforum", {'forum-id': forumid}, function(){
            alert("Successfully left Forum");
        });
    });


    $(".forum-home-button").click(function(){
        $.get(base_url+"/api/forum/forumlist", function(data, status){
            alert("Data: " + data + "\nStatus: " + status);
          });
        $(".forum-content").hide();
        $("#forum-home").slideDown("slow");
    });

    $(".create-forum-button").click(function(){
        $("#push-loader").show();
        $(".forum-content").hide();
        $("#create-forum").slideDown("slow");
        $("#push-loader").hide();
    });

    $(".search-forum-button").click(function(){
        $(".forum-content").hide();
        $("#search-forum").slideDown("slow");
    });

    $(".forum-feed-button").click(function(){
        $("#push-loader").show();
        $(".forum-content").hide();
        //fetch messages here
        $("#forum-feed").slideDown("slow");
        $("#push-loader").hide();
    });

});
