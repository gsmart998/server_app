# todos_python

## About
This is a small todo list project without a web interface. All communication is carried out using JSON via HTTP requests. PostgreSQL database used. For convenience, the project uses environment variables. To authorize users, cookies with the session UID are used, which are stored in the DB. User password stored in the DB hashed with salt.
Docker is used to run the project in separate containers.

## Installation
Clone the repository, then in the terminal, being in the folder with the project, use the docker command to start service: 
```
docker-compose up -d
```

After launch, a message should appear in the terminal (into container):
```
Server now running on port: 8001 ...
```

*Hint: address, port and DB user data can be changed in the **docker-compose.yml** file.*

## Usage

### Registration
For register a new user, you need to send a POST request with attached JSON.

    Request type: POST
    URL: localhost:8081/register

```json
{
    "name": "John",
    "login": "admin",
    "password": "password",
    "email": "admin@mail.com"
}
```

### Login
To authorize, you must use the data specified during registration.

    Request type: POST
    URL: localhost:8081/login
```json
{
    "login": "admin",
    "password": "password"
}
```

### New todo
To create a new todo you must send the following request.

    Request type: POST
    URL: localhost:8081/new
```json
{
    "task": "Test task #1"
}
```

### Get todos
To get all created todos you need to run the following query. JSON is not needed in this request.

    Request type: GET
    URL: localhost:8081/todos


### Update todo
To change a previously created todo, you must send the following request with todo id and updated data.

    Request type: PUT
    URL: localhost:8081/todo
```json
{
    "id": 1,
    "task": "Test UPDATE # 1 postman task",
    "completed": false
}
```

### Delete todo
To delete previously created notes, you must send the following request indicating the todo id.

    Request type: DELETE
    URL: localhost:8081/delete
```json
{
    "id": 16
}
```

### Logout
To log out of your account, you must submit the following request. JSON is not needed in this request.

    Request type: POST
    URL: localhost:8081/logout