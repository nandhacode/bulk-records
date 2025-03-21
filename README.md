This project consists of two Django Project:

Client Project Application – A frontend for uploading CSV files, validating and checking for duplicates, and sending valid data to the server application.
Server Project Application – Receives the data from the client, validates the request using decorators and data classes, and attempts to insert bulk employee records into the database.
Security is managed in the server application using JWT (JSON Web Token) authentication to secure API endpoints.


bulk-records/
│
├── env-bulk/   # Project environment file
│
├── upload_records/    # Client project folder
│   ├── employee    # Client app for uploading CSV file
│   │   ├── templates/
│   │   │   └── upload_csv.html    # Template for uploading CSV files
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── decorators.py    # Decorators file for validate the request from client call
│   │   ├── forms.py   # Form field for the upload screen
│   │   ├── models.py    # Model for create DB and access the data from DB using ORM
│   │   ├── tests.py
│   │   ├── urls.py    # URLs for To specifi the endpoint of the View function
│   │   └── views.py   # View for To create API function with business and validation logic 
│   ├── upload_records
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py   # Settings for django related configuration
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── .env    # To maintain the credentials details
│   └── manage.py
│
├── records_management/          # Server project folder
│   ├── read_records    # Server app for bulk creation with validation.
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── dataclasses.py   # Data class for to specifi the required field with the give data type format.
│   │   ├── decorators.py   # Decorators file for validate the request from client call
│   │   ├── forms.py    # Form field for the upload screen
│   │   ├── models.py    # Model for create DB and access the data from DB using ORM
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py    # URLs for To specifi the endpoint of the View function
│   │   └── views.py    # View for To create API function with business and validation logic
│   ├── records_management
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py   # Settings for django related configuration
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── manage.py
│
└── requirements.txt

-----------------------------------------------------------------------------------------------------------
Database Migration 

python manage.py makemigrations
python manage.py migrate
-----------------------------------------------------------------------------------------------------------

Client Application
--- Overview
The client application allows users to upload CSV files containing employee data. The application reads the file, checks for duplicate entries, and sends valid records to the server application.

--- Steps to Use Client Application:
1. Go to the client application page after client application (e.g., http://127.0.0.1:8000/upload/).
2. Select a CSV file for upload and submit it.
3. The CSV file will be read, and duplicate entries based on employee emp_id or email will be filtered.
4. If the file has valid records, they will be sent to the server application via an API call.

--- Key Features:
* File Upload: Supports CSV file uploads with POST method.
* Duplicate Check: Validates records and removes duplicates based on emp_id and email.
* Validation: Displays success or error messages after processing the CSV.


Installation and Setup for Client Application:
1. Install required dependencies:
    Step 1. Navigate to bulk-records folder
    Step 2. Run the command to install required dependencies file (pip install -r requirements.txt)

2. Navigate to the client project folder (e.g., /bulk-records/upload_records/) and Run the command to start the client project (py manage.py runserver 0.0.0.0:8000)

3. API list
Note: Before trigger the client project API calls, Please ensure the server application should run.
    1. http://127.0.0.1:8000/upload/ - Use this API endpoint to create an Access Token. After successfully created it will redirect to http://127.0.0.1:8000/upload/csv/ .

        Note: Befor call this endpoint http://127.0.0.1:8000/upload/. Try to create the superuser for the client application and add the username and password credentials to this path (e.g., /bulk-records/upload_records/.env)

    2. http://127.0.0.1:8000/upload/csv/ From this endpoint we can upload the employee file with csv format. It will validate the file columns format and dublicate records. Finally it will trigger the server application API with the valid data to store in the employee database.    

Note: Already added the client app name in the settings.py


-----------------------------------------------------------------------------------------------------------

Server Application
--- Overview
The server application receives requests from the client application, validates the received data using decorators and dataclasses, and attempts to insert the records into the database using Django's ORM.

Steps to Use Server Application:
1. The server waits for POST requests from the client application containing valid employee data.
2. The incoming request is validated using a custom decorator to check the structure of the data (e.g., checking if emp_id, name, email, etc. are present and correct).
3. The data is validated by a data class that ensures the correct data types and formats.
4. Once validated, the server inserts the employee records into the database using Django ORM in bulk.

--- Key Features:
* JWT Authentication: API endpoints are protected using JWT tokens to ensure only authorized clients can access them.
* Bulk Insert: The application supports bulk insertion of employee records into the database for efficiency.
* Request Validation: A decorator is used to ensure the incoming data is properly validated before proceeding with the database insertion.

--- Security (JWT):
* The server API uses JWT (JSON Web Token) authentication to protect API endpoints. Clients need to pass a valid JWT token in the headers of their requests.
* Generate a JWT Token: Authentication middleware validates the JWT token in the headers of the request.
Authorization: The server verifies that the token is valid before processing the request.


Installation and Setup for Server Application:
1. Install required dependencies:
    Step 1. Navigate to bulk-records folder
    Step 2. Run the command to install required dependencies file (pip install -r requirements.txt)

2. Navigate to the client project folder (e.g., /bulk-records/records_management/) and Run the command to start the server project (py manage.py runserver 0.0.0.0:8080)

Note: Already added the server app name, DRF, and JWT configuration in the settings.py


--- JWT Authentication
The server API uses JWT for securing API endpoints. To interact with the server's API, clients must pass a valid JWT token in the request headers.

--- Example of JWT Authentication Flow:
* Client Requests Token: Client sends a POST request to the server with valid credentials to receive a JWT token.
* Server Validates Credentials: The server generates a token and returns it to the client.
* Client Sends Token with API Requests: For all subsequent API requests, the client includes the JWT token in the Authorization header: Authorization: Bearer <JWT_Token>
