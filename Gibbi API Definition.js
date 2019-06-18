//Login Request
fetch(URL+'login', 
    {
        method: 'POST',
        headers:{
            Accept: 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            reg_id: 'reg_id',
            password: 'password',
            'user-type': 'student',
        }),
    })
    
//Login Reponse
{
	success: 0, 							//0 if failed, 1 if successful
	userToken: 'xxxxxxx'			//null if failed, user token is sent if successful
}

//Signup Request
fetch(URL+'signup',{
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: {
          department: data.department,
          firstname: data.firstname,
          lastname: data.lastname,
          reg_id: data.reg_id,
          email: data.email,
          year: this.state.year,
          section: this.state.section,
          phone: this.state.phone,
          password: this.state.password
        }
      })

//Signup Response
{
	success: 0,								//0 if failed, 1 if successful
	error: 'error message',				//send this if needed (optional)
	userToken: '23yiu4hjkrhfdi',		//send user's token is login is successful
}

//Your Push Posts Request
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
          pub_date: "10 AM, September 10, 2018"
        },
      ]
}


//Notification when user clicks on 'Read' for a post
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
      ]
}
