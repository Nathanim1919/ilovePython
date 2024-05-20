# Flask API Implementation
## Overview
Flask Advanced API is a RESTful API built with Flask that implements various advanced features such as authentication, input validation, logging, and Dockerization. The API allows users to perform CRUD operations on a database of users and their associated tasks. The API is secured with JWT authentication and input validation. The API is also Dockerized for easy deployment and scalability.

## Installation
1. Clone the repository
```bash
git clone https://github.com/Nathanim1919/ilovePython.git
```

2. Change directory to the project folder
```bash
cd ilovePython/flask_advanced_api
```

3. Create a virtual environment
```bash
python3 -m venv venv
```

4. Activate the virtual environment
```bash
source venv/bin/activate
```

5. Install the required packages
```bash
pip install -r requirements.txt
```

6. Set the environment variables
```bash
export FLASK_APP=app
export FLASK_ENV=development
export FLASK_SECRET_KEY=mysecretkey
export DATABASE_URL=sqlite:///database.db
```

7. Initialize the database
```bash
flask init-db
```

8. Run the application
```bash
flask run
```

## Usage
The API has the following endpoints:
- `/register` - Register a new user
- `/login` - Login an existing user
- `/logout` - Logout the current user
- `/users` - Get all users
- `/refresh` - Refresh the JWT token
- `/users/<int:user_id>` - Get a user by ID
- `/users/<int:user_id>/tasks` - Get all tasks for a user
- `/users/<int:user_id>/tasks/<int:task_id>` - Get a task by ID for a user
- `/users/<int:user_id>/tasks` - Create a new task for a user
- `/users/<int:user_id>/tasks/<int:task_id>` - Update a task by ID for a user
- `/users/<int:user_id>/tasks/<int:task_id>` - Delete a task by ID for a user


## Deployment
The API can be deployed using Docker. To build the Docker image, run the following command:
```bash
docker build -t flask-advanced-api .
```

To run the Docker container, run the following command:
```bash
docker run -p 5000:5000 flask-advanced-api
```

The API will be accessible at `http://localhost:5000`.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors
- Nathanim Tadele
