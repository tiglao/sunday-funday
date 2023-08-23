8/15/23 - I drove and we worked on getting the database setup. We had been having problems figuring out the docker files. Lea drove in the am and we built out a few models of the endpoints. Lea and Ellie created the issues for us to work from. We then picked which issues we wanted to handle. After class i finished building out the api endpoints and getting the correct data in the correct places.

8/16/23 - I drove some today and we worked on the backend auth. It wasn't as hard as I thought it was going to be. We did two merge requests which was Leah's and then mine mine for the backend auth. Need to add more error handling to the endpoints and maybe reshape some of the data. I created a branch for the frontend auth issue and started working on that.

8/17/23 - I drove in the AM we were troubleshooting the login function from the frontend. We were unsuccessful and in the PM after re-reading all the jwt documentation and many google searches I got the login to authenticate and provide token.I couldn't get the bootstrap modal to work correctly yet. I want it to close on submit but stay ope with error if no token.

8/19/23 - Its the weekend but I really wanted to finish the login function on the front-end. I used a bootstrap modal for the popup. Created error handling that shows the user their input was wrong. Once the user logs in it takes them to the main dashboard. I committed and did a merge request. Ellie found an error in the useEffect on out loginModal that is causing the modal not to show. She removed the dependency and it now shows for her on her Mac

8/20/23 - I tested the code again after Ellie made changes and it is giving me a dependency error. I was able to use useRef in react to remove the need for the dependency. I committed and and pushed so Ellie can complete the merge request. Ellie has a merge request for the auth refactor. I tested and getting a 405 error.

8/21 I finished trouble shooting and was able to complete the merge request. This was the issue I sent to Ellie:
Noticed on the backend that the token request was now accounts/token which JWTdown looks for /token.
I changed the routing in main.py to this.
app.include_router(accounts.router)
It was working but automatically keeps getting 400 bad request error since its always looking for a token at startup. So I commented out the get_token and put the one they provided us and the 400 goes away which handles the error when there is no token yet.
Today Jean did the standup and drove. I assisted him in getting a docker issue fixed and getting the containers up and running. Next up is the logout feature.
Finished the logout feature.

8/22 In the am Leah was the driver and we all assisted in figuring out some aspects of the google api. After lunch I worked on the sign up modal and it works. The only issue I have is getting a link on the login modal. Right now it shows up white since its that way in the modal link. Tomorrow I will continue to troubleshoot this and move on to the dashboard.

8/23 I got up early to try and figure out this login/signup links with no luck so far.
