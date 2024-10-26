# Example: Docker Compose
The demo shows how to set up FastAPI with MongoDB.


# Before start -> Install tools
```
Docker, Postman, nosqlbooster4mongo(Mongodb GUI)
```
### install Docker
for docker windows users, if u encounter cant start docker enginer issue, do as the followings steps
- open admin cmd and run 
    `net start com.docker.service`
- update wsl `wsl --update`
- go to docker installation pasth then run `.\DockerCli.exe -SwitchDaemon`
- start docker desktop with admin then it should be ok

### set up Python Environment
Use Pipenv to manage local python running env
`
pip install --user pipenv
`
-------------
# Project structure
```
fastapi_demo

── app
    ├── db/  (code to set up the database)
    ├── models/  (define database models)
    ├── routers/  (REST routers)
    ├── settings.py  (Project settings variables)
── main.py  (sevice main entrypoint)
── .env  (pipenv local env file)
── docker-compose.yml
── docker.env (docker env file)
── Dockerfile
── requirements.txt
```

-------------
# Running project
Select below one of this two way base on ur needs
### * for local developemt prepare local enviroment first, temp command out [web](docker-compose.yml) part in [docker-compose.yml](docker-compose.yml) file as running in directly in local
- `pipenv shell` active vitrul env 
- `pipenv install` or `pipenv run pip install -r requirements.txt` to install required libs thenrestart shell to load them
- `docker-compose up -d` to start mongodb in container
- `uvicorn main:app --reload` to start server

    **[.env](.env) for local env variables would be loaded**
### * for testing prupose directly run it in docker
- `docker-compose up -d` , api entry port is http://127.0.0.1:8888
    
    **[docker.env](docker.env) would be loaded**

# Api Details
### Authendication
Backend is using oauth2 JWT token for auth, valid time is 300m
1. Register
   > Request
    ``` 
    POST http://127.0.0.1:8888/auth/register 
    Json data: 
    {
        "username": "ttth",
        "password": "eee" (encode this in real project)
    }
    ```
    > Response
    ```
    {
        "message": "New User registered successfully."
    }
    ```
2. Login
   > Requst
   ```
   POST http://127.0.0.1:8000/auth/login
   Json data 
   {
    "username": "ttth",
    "password": "eee"
   }
   ```
   > Response
    ```
    {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InR0dGgiLCJleHAiOjE3Mjk5MzI1MDJ9.6XKDf8kzOhnpkXpubn0kxHDABYA6JP-BOkVApVqkyUM",
    "token_type": "bearer"
    }
    ```
    ***by using postman, copy and paste this access token in postman to Authorization -> Auth Type -> Bear Token for the following request***
3. User info
    > Request
    ```
    GET http://127.0.0.1:8000/auth/user_info (dont forget access token)
    ```
    > Response
    ```
    success
    {
        "username": "ttth",
        "password": "reee" (fake encoded here)
    }
    failed
    {
        "detail": "Invalid token."
    }
    ```
### Story
1. Add new story
   > Request
    ```
    POST http://127.0.0.1:8000/story
    {
       "title": "abc123",
       "content": "efghj",
       "author": "gggggggggggggggggg",
       "country": "cn"
    }
    ```
    > Reponse
    ```
    {
       "data": [
           {
               "title": "abc123",
               "content": "efghj",
               "author": "gggggggggggggggggg",
               "country": "cn"
           }
       ],
       "code": 200,
       "message": "done"
   }
    ```
2. Get all story
    > Request
    ```
    GET http://127.0.0.1:8000/story
    ```
    > Reponse
    ```
    {
       "data": [
           [
               {
                   "title": "abc123",
                   "content": "efghj",
                   "author": "gggggggggggggggggg",
                   "country": "cn"
               },
               {
                   "title": "abc123345",
                   "content": "efghj",
                   "author": "gggggggggggggggggg",
                   "country": "cn"
               }
           ]
       ],
       "code": 200,
       "message": "done"
   }
    ```
3. Uate a story
   > Request
   ```
   PUT http://127.0.0.1:8000/story/{title}
   {
       "title": "abc123345",
       "content": "efghj",
       "author": "hhhhhh",
       "country": "cn"
   }
   ```
   > Response
   ```
   {
    "data": [
        "story with title: abc123 updated"
    ],
    "code": 200,
    "message": "done"
   }
   ```
4. Delete story
    > Request
    ```
    DELETE http://127.0.0.1:8000/story/{title}
    ```
    > Response
    ```
    {
    "data": [
        "story with title: abc123 removed"
    ],
    "code": 200,
    "message": "done"
   }
    ```
# Backend Ground task
1. Batch update in backend, this will update all story country to 'cn' which country field is none
   > Request
   ```
   POST http://127.0.0.1:8000/story/bactch update
   ```

## References
* [Get started with Docker Compose](https://docs.docker.com/compose/gettingstarted/)
* [MongoDB](https://www.mongodb.com/de)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Pipenv](https://pipenv.pypa.io/en/latest/)