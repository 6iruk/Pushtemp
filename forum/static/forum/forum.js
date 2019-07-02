base_url = "http://localhost:8000";

$(document).ready(function(){

    var myforums = []
    var trendingforums =[]

    //Fetch my forums as soon as page has loaded
    // $.ajax({
    // url: base_url + '/json/myforums/',
    // processData: false,
    // contentType: false,
    // type: 'GET',
    // dataType:'json',
    // success: function (result) {

    //         if(result.status == 1) {
    //           //render the forums
    //           for ( forum in result.forums){
    //             forumcode = renderMyForum(forum)
    //             $('#my-forums-list').append(forumcode)
    //           }
    //         }

    //         else if(result.status == 0)  {
    //           feedback('Could not get your forums')
    //         }
    //     },
    // error: () => {
    //   $("#push-loader").css("display", "none");
    //   feedback('failed')
    // }
    // })

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

    // Handling buttons for navigation
    $('.createForumArea').hide()
    $('.searchForumArea').hide()
    $('.openForumArea').hide()
    $('.joinForumArea').hide()
    $('.joinClosedForumArea').hide()

    $('#createForumArea').click(function(){
        $('.myForumsArea').hide()
        $('.trendingForumsArea').hide()
        $('.createForumArea').show()
    })

    $('#backCreateForumArea').click(function(){
        $('.myForumsArea').show()
        $('.trendingForumsArea').show()
        $('.createForumArea').hide()
    })

    $('#searchForumAreaButton').click(function(){
        $('.myForumsArea').hide()
        $('.trendingForumsArea').hide()
        $('.searchForumArea').show()
    })

    $('#backsearchForumArea').click(function(){
        $('.myForumsArea').show()
        $('.trendingForumsArea').show()
        $('.searchForumArea').hide()
    })

    $('.backToForumLists').click(function(){
        $('.ForumArea').hide()
        $('.myForumsArea').show()
        $('.trendingForumsArea').show()
    })

    //Create Forum Post Request
    $('#createForumForm').submit(function(event){
        event.preventDefault();

        form = document.forms.namedItem("createForumForm");
        formdata =  new FormData(form);

        console.log(formdata)

        $("#push-loader").css("display", "block");
        $.ajax({
        url: base_url + '/api/forum/createforum/',
        data: formdata,
        processData: false,
        contentType: false,
        type: 'POST',
        dataType:'json',
        success: function (result) {
                $("#push-loader").css("display", "none");
                if(result.status == 1) {
                $("#push-loader").css("display", "none");
                feedback('Your forum has been created successfully! Refresh to update.')
                form.reset()
                $('.myForumsArea').show()
                $('.trendingForumsArea').show()
                $('.createForumArea').hide()
                }

                else if(result.status == 0)  {
                    $("#push-loader").css("display", "none");
                    feedback('Forum creation failed')
                }
            },
        error: () => {
                $("#push-loader").css("display", "none");
                feedback('Failed, please try again.')
            }
        })
    })

    //Search Forum Request
    $('#searchForumButton').click(function(event){

        form = document.forms.namedItem("search-forum-form");
        formdata =  new FormData(form);

        $("#push-loader").css("display", "block");
        $.ajax({
        url: base_url + '/api/forum/search/',
        data: formdata,
        processData: false,
        contentType: false,
        type: 'POST',
        dataType:'json',
        success: function (result) {
                $('#search-result-list').empty()
                $("#push-loader").css("display", "none");
                result.forEach(function (forum, index) {
                    $('#search-result-list').append(renderTrendingForum(forum, index))
                });
                console.log('Search result',result)
            },
        error: () => {
                $("#push-loader").css("display", "none");
                feedback('Search failed, please try again.')
            }
        })
    })

    //Fetch, store and render myforums
    $.ajax({
        url: base_url + '/api/forum/forumlist',
        processData: false,
        contentType: false,
        type: 'GET',
        dataType:'json',
        success: function (result) {
                // myforums = result
                myforums = [        //remove at integration
                    {
                        id: 0,
                        title: 'Hello',
                        description: 'hi!',
                        thumbnail: '',
                        creator: true
                    },
                    {
                        id: 1,
                        title: 'Hello',
                        description: 'hi!',
                        thumbnail: '',
                        creator: false
                    }
                ]
                myforums.forEach(function (forum, index) {
                    console.log(forum)
                    $('#my-forums-list').append(renderMyForum(forum, index))
                });
                console.log('My Forums: ', myforums)
            },
        error: () => {

            }
        })

    //Fetch, store and render trendingforums
    $.ajax({
        url: base_url + '/api/forum/trendingforums/',
        processData: false,
        contentType: false,
        type: 'GET',
        dataType:'json',
        success: function (result) {
                // trendingforums = result
                trendingforums = [ //remove at integration
                    {
                        id: 0,
                        title: 'Hello',
                        description: 'hi!',
                        thumbnail: '',
                        joincode: false,
                    },
                    {
                        id: 1,
                        title: 'Hello',
                        description: 'hi!',
                        thumbnail: '',
                        joincode: true,
                    }
                ]
                trendingforums.forEach(function (forum, index) {
                    console.log(forum)
                    $('#trending-forums-list').append(renderTrendingForum(forum, index))
                });

                console.log('Trending Forums: ', trendingforums)
            },
        error: () => {
            
            }
        })

    //My forum title has been pressed. This opens that forum
    $('.openMyForumLink').click(function(){
        console.log('in here')
        var elem = $( this );
        var index = elem.attr( "index" )
        var forum = myforums[index] //the forum that is opened

        var forummessages = []

        //get messages
        $.ajax({
            url: base_url + '/api/forum/forummessages/?forum-id='+forum.id,
            processData: false,
            contentType: false,
            type: 'GET',
            dataType:'json',
            success: function (result) {
                    
                },
            error: () => { //move to success at integration
                    form = document.forms.namedItem("forumSendMessageForm");
                    form.reset()


                    $('#deleteForum').hide()
                    //check if its a creator
                    if (forum.creator){
                        $('#deleteForum').show()
                        $('#deleteForum').attr('forum-id', forum.id)
                    }
                    $('#leaveForum').attr('forum-id', forum.id)

                    $('.myForumsArea').hide()
                    $('.trendingForumsArea').hide()
                    $('.openForumArea').show()

                    $('#openForumTitle').text(forum.title)
                    $('#openForumThumbnail').attr('src',forum.thumbnail)
                    $('#openForumTitle').text(forum.title)

                    $('#forum_id').text(forum.id)   //save this for when message is sent
                    //forummessages = result
                    var forummessages = [ //remove at integration
                        {
                            id: 0,
                            content: 'Hello',
                            self: false,
                            file:
                                {
                                    id: 1,
                                    name: 'Hello.pdf',
                                    extension: 'PDF',
                                    post_by: 'Mr. Biruk',
                                    url: ''
                                },
                            image:
                                {
                                    id: 1,
                                    post_by: 'Mr. Biruk',
                                    url: ''
                                },
                            post_type: '',
                            post_by: 'Mr. Biruk',
                            pub_date: 'July 10, 2019',
                        },
                        {
                            id: 1,
                            content: 'This is another message. This is me.',
                            self: true,
                            file:
                                {
                                    id: 1,
                                    name: 'Hello.pdf',
                                    extension: 'PDF',
                                    post_by: 'Mr. Addis',
                                    url: ''
                                },
                            image:
                                {
                                    id: 1,
                                    post_by: 'Mr. Addis',
                                    url: ''
                                },
                            post_type: '',
                            post_by: 'Mr. Addis',
                            pub_date: 'July 10, 2019',
                        }
                    ]
                    $('#openForumMessages').empty()
                    forummessages.forEach(function (message) {
                        $('#openForumMessages').append(renderForumMessage(message))
                    });
    
                    console.log('Forum messages: ', forummessages)
                }
            })

    })

    //delete forum
    $('#deleteForum').click(function(){
        var elem = $( this );
        var forumid = elem.attr( "forum-id" )
        console.log('About to delete:', forumid)
    
        $("#push-loader").css("display", "block");
        $.ajax({
        url: base_url + '/api/forum/deleteforum/?forum-id='+forumid,
        processData: false,
        contentType: false,
        type: 'GET',
        dataType:'json',
        success: function (result) {
                $("#push-loader").css("display", "none");
                if(result.status == 1) {
                  $("#push-loader").css("display", "none");
                  feedback('Your forum has been deleted. Refresh to update.')
                  location.reload()
                }
    
                else if(result.status == 0)  {
                  $("#push-loader").css("display", "none");
                  feedback('Forum delete failed')
                }
            },
        error: () => {
          $("#push-loader").css("display", "none");
          feedback('Connection failed')
        }
          })
      })

      //leave forum
    $('#leaveForum').click(function(){
        var elem = $( this );
        var forumid = elem.attr( "forum-id" )
        console.log('About to leave:', forumid)
    
        $("#push-loader").css("display", "block");
        $.ajax({
        url: base_url + '/api/forum/leaveforum/?forum-id='+forumid,
        processData: false,
        contentType: false,
        type: 'GET',
        dataType:'json',
        success: function (result) {
                $("#push-loader").css("display", "none");
                if(result.status == 1) {
                  $("#push-loader").css("display", "none");
                  feedback('You have left the forum. Refresh to update.')
                  //location.reload()
                }
    
                else if(result.status == 0)  {
                  $("#push-loader").css("display", "none");
                  feedback('Forum delete failed')
                }
            },
        error: () => {
          $("#push-loader").css("display", "none");
          feedback('Connection failed')
        }
          })
      })


    //Send messge from forum
    $("#sendForumMessage").click(function( event ) {

        form = document.forms.namedItem("forumSendMessageForm");
        var formdata =  new FormData(form);

        console.log(formdata)
    
        $("#push-loader").css("display", "block");
        $.ajax({
        url: base_url + '/api/forum/sendmessage/',
        data: formdata,
        processData: false,
        contentType: false,
        type: 'POST',
        dataType:'json',
        success: function (result) {
                $("#push-loader").css("display", "none");
                if(result.status == 1) {
                  $("#push-loader").css("display", "none");
                  //append the sent message
                  
                }

                else if(result.status == 0)  {
                  $("#push-loader").css("display", "none");
                  feedback('Send message failed')
                }
            },
        error: () => {
            console.log(formdata)
            $('#openForumMessages').append(renderForumMessage(formdata))
          $("#push-loader").css("display", "none");
          feedback('failed')
        }
          })
      })
    

});


function renderMyForum(forum, index){
    html=''
    html+="<div class=\"row mt-3 no-gutters\">"
    html+="        <div class=\"col-auto\">"
    html+="            <img src=\"" + forum.thumbnail + "\" width=\"60\" height=\"60\">"
    html+="        </div>"
    html+="        <div class=\"col ml-3\">"
    html+="             <span index=\""+ index +"\" class=\"link d-block openMyForumLink\">"+ forum.title +"</span>"
    html+="             <p>"+ forum.description +"</p>"
    html+="        </div>"
    html+="</div>"
  
    return html
  }

function renderTrendingForum(forum, index){
    lock=''
    if (forum.joincode){
        lock = "<i class=\"fa fa-lock ml-1\" aria-hidden=\"true\"></i>"
    }
    html=''
    html+="<div class=\"row mt-3 no-gutters\">"
    html+="        <div class=\"col-auto\">"
    html+="            <img src=\"" + forum.thumbnail + "\" width=\"60\" height=\"60\">"
    html+="        </div>"
    html+="        <div class=\"col ml-3\">"
    html+="             <span index=\""+ index +"\" class=\"link d-block openTrendingForumLink\">"+ forum.title + lock + "</span>"
    html+="             <p>"+ forum.description +"</p>"
    html+="        </div>"
    html+="</div>"

    return html
}

function renderForumMessage(message){
    self = ''
    if (message.self){
        self = "align-self-end"
    }
    html=''
    html+="<div class=\"card card-body push-corners mb-3 w-75 "+ self + " \">"
    html+="<div class=\"flex-container\">"
    html+="    <p class=\"body font-weight-bold\">"+ message.post_by +"</p>"
    html+="    <p class=\"meta\">"+ message.pub_date +"</p>"
    html+="</div>"
    if (message.image){
        html+="<div>"
        html+="    <img src=\"" + message.image.url + "\" class=\"img-fluid mb-3\">"
        html+="</div>"
    }
    html+="<div>"
    html+="    <p class=\"body\">"+ message.content +"</p>"
    html+="</div>"
    html+="<div>"
    if (message.file){
        html+="    <a href=\"" + message.file.url + "\" class=\"link font-weight-bold\">" + message.file.name + " [" + message.file.extension + "]</a>"
    }
    html+="</div>"
    html+="</div>"
    

    return html
}







      // //Fetch user forum
    // function forumTitle(forum){
    //     console.log("In forumTitleForum: ", forum);
    //     var title = document.createElement("div");
    //     title.innerHTML = "<a>" + forum.name + "</a>"
    //     title.setAttribute("class", "link font-weight-bold mt-2 forum-name");
    //     title.setAttribute("id", "Forum"+forum.id);
    //     title.setAttribute("forumid", forum.id);
    //     return title;
    // }

    // console.log('in forum JS')

    // $.get(base_url+"/api/forum/forumlist", function(data){
    //     $("#push-loader").show();
    //     console.log('in forumlist', data)
    //     $.each(data, function(index, value){
    //         $("#user-forums").append(forumTitle(value));
    //     });
    // })
    // .done(function(){
    //     $("#push-loader").hide();
    // })
    // .fail(function(jqxhr, status, exception) {
    //         alert( exception );
    //     });

    // //Fetch trending forum
    // $.get(base_url+"/api/forum/trendingforums/", function(data){
    //     $("#push-loader").show();
    //     $.each(data, function(index, value){
    //         $("#trending-forums").append(forumTitle(value));
    //     });
    // })
    // .done(function(){
    //     $("#push-loader").hide();
    // })
    // .fail(function(jqxhr, status, exception) {
    //     alert( exception );
    //   });
    
    // $("#forum-home").slideDown("slow");



    // //Open Forum

    // function messageFetch(forumid){

    //     $("#forum-messages").empty(); //clear the messages area

    //     function forumMessage(value){
    //         var message = document.createElement("p");
    //         message.innerText = value.content;
    //         return message;
    //     }

    //     $.get(base_url+"/api/forum/forummessages", {'forum-id': forumid},function(data){
    //         console.log("Forum data: ",data)
    //         $("#push-loader").show();
    //         $.each(data, function(index, value){
    //             $("#forum-messages").append(forumMessage(value));
    //         });
    //         $("#forum-message-id").attr("value", forumid);
    //         $("#leave-forum-button").attr("forumid", forumid)
    //     })
    //     .done(function(){
    //         $("#push-loader").hide();
    //     })
    //     .fail(function(jqxhr, status, exception) {
    //             alert( exception );
    //         });
    // }

    // $(".forum-name").click(function(){
    //     $("#push-loader").show();
    //     $(".forum-content").hide();

    //     //fetch and render messages here
    //     forumid = this.getAttribute("forumid")
    //     console.log("forumid: ", forumid)
    //     messageFetch(forumid);

    //     $("#forum-feed").slideDown("slow");
    //     $("#push-loader").hide();
    // });

    // //Send Message
    // $("#forum-send").on("submit", function(){
    //     var form = $(this);
    //     var formdata = false;
    //     if (window.FormData){
    //         formdata = new FormData(form[0]);
    //     }
    //     var formAction = form.attr('action');
    //     $.ajax({
    //         url         : base_url+"/api/forum/sendmessage/",
    //         data        : formdata ? formdata : form.serialize(),
    //         cache       : false,
    //         contentType : false,
    //         processData : false,
    //         type        : 'POST',
    //         success     : function(data, textStatus, jqXHR){
    //             alert("success");
    //         },
    //         fail: function(data, textStatus, jqXHR){
    //             alert("failed");
    //         }
    //     });
    //     form.trigger("reset");
    //     messageFetch(forumid);
    // })

    // //Leave Forum
    // $("#leave-forum-button").click(function(){

    //     forumid = this.getAttribute("forumid");

    //     $.get( base_url+"/api/forum/leaveforum", {'forum-id': forumid}, function(){
    //         alert("Successfully left Forum");
    //     });
    // });


    // $(".forum-home-button").click(function(){
    //     $.get(base_url+"/api/forum/forumlist", function(data, status){
    //         alert("Data: " + data + "\nStatus: " + status);
    //       });
    //     $(".forum-content").hide();
    //     $("#forum-home").slideDown("slow");
    // });

    // $(".create-forum-button").click(function(){
    //     $("#push-loader").show();
    //     $(".forum-content").hide();
    //     $("#create-forum").slideDown("slow");
    //     $("#push-loader").hide();
    // });

    // $(".search-forum-button").click(function(){
    //     $(".forum-content").hide();
    //     $("#search-forum").slideDown("slow");
    // });

    // $(".forum-feed-button").click(function(){
    //     $("#push-loader").show();
    //     $(".forum-content").hide();
    //     //fetch messages here
    //     $("#forum-feed").slideDown("slow");
    //     $("#push-loader").hide();
    // });