## Project Documentation

Please put any and all documentation for your project in this folder. Other than the documents that are required at the end of week 13, feel free to organize this however your group sees fit.



## API Endpoints

## Full List

- Login *** free!
- Logout
[x] Create account
- Request reset password
- Change password
- Delete account
- Edit account information


[x] Create party plan
- Get all list of plans for user
- Update party plan
    - Status: Pending, Draft-for-review, Finalize
- View specific party plan
    - Party planner: see invitee list read/responded status
    - Invitee: see own response, see yes list?
- Share party plan with invitees
- Delete party plan


[x] Send invitations to invitees (post)
- Get all user invitations
- Invitee update invitation
    - Status: accepted, declined, maybe


- View specific location
- View all locations
    - Create ordered itinerary of favorite locations?
    - View as a map?
- Update location
[x] Favorite location (post)
    - Favorite status: bool
- View location reviews
- Delete location



STRETCH
- View all suggestions.
    - View as a map?
- View suggestion.
- View plan for collaboration (add as plan attribute?)
- Add suggestion to plan

- Get all user notifications
- Update notification
    - Status: Unread, read.



### Log in

* Endpoint path: /token
* Endpoint method: POST

* Request shape (form):
  * username: string
  * password: string

* Response: Account information and a token
* Response shape (JSON):
    ```json
    {
      "account": {
        «key»: type»,
      },
      "token": string
    }
    ```


### Log out

* Endpoint path: /token
* Endpoint method: DELETE

* Headers:
  * Authorization: Bearer token

* Response: Always true
* Response shape (JSON):
    ```json
    true
    ```


### «Human-readable of the endpoint»

* Endpoint path: «path to use»
* Endpoint method: «HTTP method»
* Query parameters:
  * «name»: «purpose»

* Headers:
  * Authorization: Bearer token

* Request shape (JSON):
    ```json
    «JSON-looking thing that has the
    keys and types in it»
    ```

* Response: «Human-readable description
            of response»
* Response shape (JSON):
    ```json
    «JSON-looking thing that has the
    keys and types in it»
    ```


### Create account

* Endpoint path: /users/create
* Endpoint method: POST

* Query parameters:
  * N/A

* Headers:
  * Content-Type: application/json???

* Request shape (JSON):
    ```json
        {
            "username": "string"
            "firstname": "string"
            "email": "string"
            "password": "string"
            "DOB": "formatted string YYYY-MM-DD"
            "avatar": "URL string"
        }
    ```

* Response: Account information
* Response shape (JSON):
    ```json
        "status": "success or error string"
        "userId": "<unique identifier">
    ```


### Create party plan

* Endpoint path: /parties/create
* Endpoint method: POST

* Query parameters:
  * N/A

* Headers:
  * Authorization: Bearer token

* Request shape (JSON):
    ```json
        {
            "username": "string"
            "notes": "string"
            "date": "formatted string YYYY-MM-DD"
            "invitees": "dict/string"
            "startTime": "formatted string HH:MM"
            "endTime": "formatted string HH:MM"
            "partyStatus": "string"
            "keywords": "string"
            "generalLocation": "string"
            "favoriteLocations": "dict/string"
                "description": "string"
                "picture": "url"
                "startTime": "formatted string HH:MM"
        }
    ```

* Response: Party information
* Response shape (JSON):
    ```json
        "status": "success or error string"
        "partyId": "<unique identifier>"
    ```


### Create location

* Endpoint path: /locations/create
* Endpoint method: POST

* Query parameters:
  * N/A

* Headers:
  * Authorization: Bearer token

* Request shape (JSON):
    ```json
        {
            "notes": "string"
            "name": "string"
            "hoursOfOperation": "dict/string"
            "address": "string"
            "reviews": "dict/string"
            "favoriteStatus": "bool string"
            "website": "URL string"
            "parties": "dict/string"
        }
    ```

* Response: Party information
* Response shape (JSON):
    ```json
        "status": "success or error string"
        "locationId": "<unique identifier>"
    ```


### Create invitation

* Endpoint path: /invitations/create
* Endpoint method: POST

* Query parameters:
  * N/A

* Headers:
  * Authorization: Bearer token

* Request shape (JSON):
    ```json
        {
            "firstname": "string"
            "lastname": "string"
            "email": "formatted string YYYY-MM-DD"
            "rsvpStatus": "string"
        }
    ```

* Response: Party information
* Response shape (JSON):
    ```json
        "status": "success or error string"
        "invitationId": "<unique identifier>"
    ```
