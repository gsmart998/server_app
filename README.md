# Todos

## About
This is a small task list project without a web interface. All communication is carried out using http requests.

## Installation
Copy the repository, then in the terminal, being in the folder with the project, use the command to install dependencies: 
```
pip install -r requirements.txt
```

After that, start the server with the command:
```
python3.12 main.py
```

After launch, a message should appear in the terminal:
```
Server now running on port: 8000 ...
```

*Hint: address, port, and path with the database name can be changed in the **.env** file.*

## Usage

### Registration
For register a new user, you need to send a POST request with attached JSON.

    Request type: POST
    URL: localhost:8000/register

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
    URL: localhost:8000/login
```json
{
    "login": "admin",
    "password": "password"
}
```

### New todo
To create a new todo you must send the following request.

    Request type: POST
    URL: localhost:8000/new
```json
{
    "task": "Test task #1"
}
```

### Get todos
To get all created todos you need to run the following query. JSON is not needed in this request.

    Request type: GET
    URL: localhost:8000/todos


### Update todo
To change a previously created todo, you must send the following request with todo id and updated data. The *"completed"* section in the JSON indicates the status of the todo. 0 - not completed, 1 - completed.

    Request type: PUT
    URL: localhost:8000/todo
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
    URL: localhost:8000/delete
```json
{
    "id": 16
}
```

### Logout
To log out of your account, you must submit the following request. JSON is not needed in this request.

    Request type: POST
    URL: localhost:8000/logout