
# Django -Channels Real Time Chat Demo

This project  project is a real-time chat application developed using Django Channels, an extension for Django that enables handling of WebSockets and asynchronous tasks. Users can create chat rooms, join existing rooms, and exchange messages in real-time. The application includes user authentication for security and RESTful API endpoints for managing user accounts and chat functionalities.


## Features

- Real-Time Messaging: Users can exchange messages instantly within chat rooms.
- RESTful API: API endpoints for user management, chat room creation, and messaging.
- Interactive API Documentation: Utilized Swagger for interactive API documentation, allowing users to explore and interact with the API endpoints easily.
- Containerized Deployment: Utilized Docker to containerize the project.


## Tech Stack

**Backend:** Python, Django, Rest Framework

**Database:** PostgreSQL

**Other Tools:** Docker, Django-Channels , WebSockets

## Installation

Prerequisites

    Python latest version
    Docker 

Clone the repository:
```bash 
git@github.com:asefdevs/Python-Chat-App.git
```
    
## Usage

Run Docker Compose:

```bash

sudo docker-compose up --build

```
For Running Manually:

```bash

python manage.py runserver (for django app)
docker run --rm -p 6379:6379 redis:7 (for websocket connection )

```
Main Urls:

```bash

http://127.0.0.1:8000/api/schema/swagger-ui/#/
ws://127.0.0.1:8000/ws/chat/chat_uuid/token/

```



## 🔗 Endpoints and Features


### Chat App Endpoints

| Endpoint                                | HTTP Method | Description                                       |
|-----------------------------------------|-------------|---------------------------------------------------|
| /api/add-contact/                       | POST        | Add a new contact                                 |
| /api/delete-contact/<int:contact_id>/   | DELETE      | Delete a contact by ID                            |
| /api/my-contacts/                       | GET         | Retrieve the list of user's contacts              |
| /api/start-chat-room/                   | POST        | Start or get chat room                             |
| /api/chat-room/<str:room_id>/           | GET         | Retrieve details of a specific chat room          |
| /api/token/                             | POST        | Obtain a JWT authentication token                 |
| /api/token/refresh/                    | POST        | Refresh a JWT authentication token                |
| /register/                              | POST        | Register a new user                               |
| /generate-otp/                          | POST        | Generate an OTP for user verification             |
| /verify-otp/                            | POST        | Verify an OTP for user verification               |
| /profile/                               | GET         | Retrieve user's profile details                   |
| /profile/update/                        | PUT         | Update user's profile                             |
| /all-users/                             | GET         | Retrieve list of all users                        |


## License

[MIT](https://choosealicense.com/licenses/mit/)

