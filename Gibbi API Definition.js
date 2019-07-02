//Login Request [IMPLEMENTED]
fetch(URL+'login', 
    {
        method: 'POST',
        headers:{
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'reg-id': 'reg-id',
            password: 'password',
            'user-type': 'student',
        }),
    })
    
//Login Reponse
{
	success: 0, 							//0 if failed, 1 if successful
	userToken: 'xxxxxxx'			//null if failed, user token is sent if successful
}

//Signup Request [IMPLEMENTED]
fetch(URL+'signup',{
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: {
          department: 'Computer Science',
          firstname: 'Addismiraph',
          lastname: 'Abebe',
          'reg-id': 'NSR/2009/08',
          email: 'genioaddis@gmail.com',
          year: 1,
          section: 1,
          phone: '0913350082',
          password: 'aaupush123'
        }
      })

//Signup Response
{
	success: 0,								//0 if failed, 1 if successful
	error: 'error message',				//send this if needed (optional)
	userToken: '23yiu4hjkrhfdi',		//send user's token is login is successful
}

//Your Push Posts Request [IMPLEMENTED]
fetch(URL+'posts',{
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: {
          userToken: '23yiu4hjkrhfdi',
          latestPostId: -1						//this is the ID of the last post I have
          												//-1 means I have nothing yet
        }
      })
      
//Your Push Posts Response
{
	posts: [						//a list of posts 
        {
          id: 0,
          content: "This is a trial post.",
          read: true, 			//part of the ClickReadPost use case
          							//true if post has been read by user, false if post has not been read
          files: [
            {
              id: 1,
              name: 'Chapter 1',
              extension: 'PDF',
              size: '',
              uri: '../assets/images/openday.jpg'				//url of the file
            },
          ],
          images: [
            {
              id: 1,
              uri: '../assets/images/openday.jpg'				//url of the image
            },
            {
              id: 2,
              uri: '../assets/images/openday.jpg'
            },
            {
              id: 3,
              uri: '../assets/images/openday.jpg'
            },
          ],
          post_by: 'Dr. Dagmawi',
          post_course: 'Software Engineering',
          post_courseid: 32,
          pub_date: "10 AM, June 10, 2018"
        },
        {
          id: 1,
          content: "This is a trial post. This has a much more longer text so it has two lines. Let's see how this is handled",
          read: false, //for tracker
          files: [],
          images: [],
          post_by: 'Mr. Gashaw',
          post_course: 'Windows Programming',
          post_courseid: 21,
          pub_date: "10 AM, September 10, 2018"
        },
      ],
      latestPostId: 3,      //send back the id of the last post
}


//Notification when user clicks on 'Read' for a post [IMPLEMENTED]
//No response necessary
fetch(URL+'readpost',{
      method: 'POST',
      headers:{
          Accept: 'application/json',
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          userToken: userToken,			//I will send you the token of user
          postId: id,								//I will send you the id of the post so you can track that post
      }),
    })
    
    
    
//Push Board Posts Request
fetch(URL+'pushboard',{
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: {
          userToken: '23yiu4hjkrhfdi',
          latestPushboardId: -1			//this is the ID of the last post I have
          												//-1 means I have nothing yet
        }
      })
      
//Pushboard Posts Response
//Exactly the same as Your Push but these are Pushboard posts for the user AND name the post_course field as 'Pushboard'
{
	posts: [						//a list of posts 
        {
          id: 0,
          content: "This is a trial post.",
          read: true, 			//part of the ClickReadPost use case
          							//true if post has been read by user, false if post has not been read
          files: [
            {
              id: 1,
              name: 'Chapter 1',
              extension: 'PDF',
              size: '',
              uri: '../assets/images/openday.jpg'				//url of the file
            },
          ],
          images: [
            {
              id: 1,
              uri: '../assets/images/openday.jpg'				//url of the image
            },
            {
              id: 2,
              uri: '../assets/images/openday.jpg'
            },
            {
              id: 3,
              uri: '../assets/images/openday.jpg'
            },
          ],
          post_by: 'Dr. Dagmawi',
          post_course: 'Pushboard',             //have this for all posts
          pub_date: "10 AM, June 10, 2018"
        },
        {
          id: 1,
          content: "This is a trial post. This has a much more longer text so it has two lines. Let's see how this is handled",
          read: false, //for tracker
          files: [],
          images: [],
          post_by: 'Mr. Gashaw',
          post_course: 'Pushboard',
          pub_date: "10 AM, September 10, 2018"
        },
      ],
      latestPostId: 3,      //send back the id of the last post
}


//Reminders Request [IMPLEMENTED]
fetch(URL+'reminders', 
      {
        method: 'POST',
        headers:{
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            userToken: '23yiu4hjkrhfdi',
            latestReminderId: 13,       //this is the ID of the last post I have
          												//-1 means I have nothing yet
        }),
      })
      
//Reminder Response
{
    reminders: [            //a list of reminder objects
      {
        id: 11,
        name: "Assignment 1",
        content: "Your assignment is to build a space ship. Group numbers cannot exceed more than 5. ZIP photos and upload it here.",
        submitted: false, //whether or not the user has submitted their answer
        reminderType: "Assignment",   //"Assignment" assignment reminder and "Normal" or others like test and presentions
        file: {
            id: 1,
            name: 'Assignment 1',
            extension: 'PDF',
            size: '3 MB',
            uri: 'http://www.cheat-sheets.org/saved-copy/jsquick.pdf',				//url of the file
          },
        due_date: "July 10, 2018",
        due_time: "10:30 AM",
        post_by: 'Ms. Aynalem',
        post_course: 'Wireless Communication',
        post_courseid: 38,
        pub_date: "10 AM, June 10, 2018"
      },
    ],
    latestReminderId: 23,      //send back the id of the last reminder
}

//Courses Lists Request [IMPLEMENTED]
fetch(URL+'courses',{
      method: 'POST',
      headers:{
          Accept: 'application/json',
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          userToken: '23yiu4hjkrhfdi',
      }),
    })

//Courses Lists Response
//response is a list of objects
[
    {
      name: 'Introduction to Computer Science',
      id: 5
    },
    {
      name: 'Calculus Two',
      id: 6
    },
    {
      name: 'Advanced Algorithm',
      id: 7
    },
    {
      name: 'Civic and Ethical Education',
      id: 8
    },
    {
      name: 'Software Engineering',
      id: 1
    },
]
  
  
//List of My Forums request
//This is a list of the forums a user is in
fetch(URL+'myforums', 
    {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            userToken: '23yiu4hjkrhfdi',
            latestForumId: 3,       //that means I already have forums 2 and 1. If -1, it means I have nothing.
        }),
    })
    
//List of My Forums response
{
    forums: [       //list of forum objects
                    {
                        id: 1,
                        name: 'Complexity Theory',
                        desc: 'Forum for Q&A and class discussions',
                        thumbnail: '../assets/images/openday.jpg',
                        creator: true,      //true if the user request is the creator of the forum
                    },
                ],
    latestForumId: 23,
}


//Send message to forum request
fetch(URL+'forumsendmessage',{
            method: 'POST',
            headers:{
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                userToken: '23yiu4hjkrhfdi',
                forumId: 12,
                message: 'Hello this is my message.',
                latestForumPostId: 321
            }),
          })

//Send Message to forum response
{
    success: 1,             //success is 1 if message is recorded. 0 if there is a problem.
    error: 'User not found'     //the problem that could occur on server side
}


//Get University Data request
 fetch(URL+'uniData')

//Get University Data response
[
  {
    name: 'Computer Science',
    id: 0,
    years: [
      {
        year: 1,
        sections: ['1', '2']
      }, 
      {
        year: 2,
        sections: ['1', '2']
      },
      {
        year: 3,
        sections: ['1']
      },
      {
        year: 4,
        sections: ['1']
      },
    ],
  },
  {
    name: 'Biology',
    id: 1,
    years: [
      {
        year: 1,
        sections: ['1', '2','3']
      }, 
      {
        year: 2,
        sections: ['1', '2','3']
      },
      {
        year: 3,
        sections: ['1','2','3']
      },
    ],
  }
]

//Submit assignment
fetch(URL+'submitassignment/',{
            method: 'POST',
            headers:{
                Accept: 'application/json',
            },
            body: JSON.stringify({
                userToken: '23yiu4hjkrhfdi',
                comments: 'This is my comment.',
                file: {
                    name: 'My submission.pdf',
                    type: 'application/pdf',
                    uri: 'content://com.android.externalstorage.documents/document/primary%3ADownload%2FCities%20are%20like%20people%20%20This%20is%20Addis..pdf' 
                }
            }),
          })
//Submit assignment response
{
    success: 1,
    error: 'error message if needed',
}