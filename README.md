# Django CSV Upload and Validation System

This project consists of two Django applications:

## 1. Client Project Application
The client application provides a frontend for uploading CSV files. It validates the uploaded files, checks for duplicates, and sends the valid data to the server application.

### Key Features:
- **CSV File Upload**: Allows users to upload employee data in CSV format.
- **Duplicate Check**: Filters out records with duplicate `emp_id` or `email`.
- **Validation**: Validates the CSV data before sending it to the server application.

---

## 2. Server Project Application
The server application receives the data from the client, validates the request using custom decorators and data classes, and attempts to insert the bulk employee records into the database.

### Key Features:
- **Request Validation**: Validates the structure of the incoming request using decorators and data classes.
- **Bulk Insert**: Supports the bulk insertion of employee records into the database using Django ORM.
- **Security**: The server application uses **JWT (JSON Web Token)** authentication to secure API endpoints.

---

## Security
- **JWT Authentication**: The server application is protected by JWT authentication. Only clients with valid JWT tokens are authorized to make requests to the server.

---

![Project Folder Structure](docs/folder_structure.png)

# Database Migration  

To apply database migrations, run the following commands:  

```bash
python manage.py makemigrations
python manage.py migrate


# Client Application

## Overview  
The client application allows users to upload CSV files containing employee data. The application reads the file, checks for duplicate entries, and sends valid records to the server application.

## Steps to Use Client Application:
1. Go to the client application page (e.g., [http://127.0.0.1:8000/upload/](http://127.0.0.1:8000/upload/)).
2. Select a CSV file for upload and submit it.
3. The CSV file will be read, and duplicate entries based on employee `emp_id` or `email` will be filtered.
4. If the file has valid records, they will be sent to the server application via an API call.

## Key Features:
- **File Upload**: Supports CSV file uploads with POST method.
- **Duplicate Check**: Validates records and removes duplicates based on `emp_id` and `email`.
- **Validation**: Displays success or error messages after processing the CSV.


# Installation and Setup for Client Application

## 1. Install Required Dependencies:
- Navigate to the `bulk-records` folder.
- Run the command to install the required dependencies:  
  ```bash
  pip install -r requirements.txt

## 2. Start the Client Project:
- Navigate to the client project folder (e.g., `/bulk-records/upload_records/`):
  ```bash
  cd bulk-records/upload_records

- Run the command to start the client project:
  ```bash
  py manage.py runserver 0.0.0.0:8000

## 3. API List
**Note:** Before triggering the client project API calls, ensure that the server application is running.

### 1. Authentication & File Upload
- **Endpoint:**  http://127.0.0.1:8000/upload/
- This API endpoint is used to create an Access Token.
- After successfully creating the token, it will redirect to:

  http://127.0.0.1:8000/upload/csv/

  - **Important:** Before calling this endpoint (`http://127.0.0.1:8000/upload/`), create a superuser for the client application.  
  - Add the username and password credentials in the `.env` file located at:

    /bulk-records/upload_records/.env

### 2. Employee CSV Upload
- **Endpoint:**  http://127.0.0.1:8000/upload/csv/

- This API allows uploading an employee CSV file.
- It validates:
  - CSV file column format.
  - Duplicate records.
- After validation, it triggers the server application API to store valid data in the employee database.

**Note:** The client app name is already added in the `settings.py` file.

# Server Application

## Overview
The server application receives requests from the client application, validates the received data using decorators and dataclasses, and attempts to insert the records into the database using Django\'s ORM.

## Steps to Use Server Application:
1. The server waits for `POST` requests from the client application containing valid employee data.
2. The incoming request is validated using a custom decorator to check the structure of the data  
   (e.g., verifying if `emp_id`, `name`, `email`, etc., are present and correctly formatted).
3. The data is further validated by a data class to ensure correct data types and formats.
4. Once validated, the server inserts the employee records into the database using Django ORM in bulk.

## Key Features:
- **JWT Authentication**: API endpoints are protected using JWT tokens to ensure only authorized clients can access them.
- **Bulk Insert**: The application supports bulk insertion of employee records into the database for efficiency.
- **Request Validation**: A decorator is used to ensure the incoming data is properly validated before proceeding with the database insertion.

## Security (JWT):
- The server API uses **JWT (JSON Web Token) authentication** to protect API endpoints. Clients need to pass a valid JWT token in the headers of their requests.
- **Generate a JWT Token**: Authentication middleware validates the JWT token in the headers of the request.
- **Authorization**: The server verifies that the token is valid before processing the request.

# Installation and Setup for Server Application

## 1. Install Required Dependencies:
- Navigate to the `bulk-records` folder:
  ```bash
  cd bulk-records

- Run the command to install the required dependencies:
  ```bash
  pip install -r requirements.txt

## 2. Start the Server Project:
- Navigate to the server project folder (e.g., `/bulk-records/records_management/`):
  ```bash
  cd bulk-records/records_management

- Run the command to start the server project:
  ```bash
  py manage.py runserver 0.0.0.0:8080

**Note:** Already added the server app name, DRF, and JWT configuration in the `settings.py` file.


# JWT Authentication

The server API uses **JWT (JSON Web Token)** for securing API endpoints.  
To interact with the server\'s API, clients must pass a valid JWT token in the request headers.

## JWT Authentication Flow:

1. **Client Requests Token**  
   - The client sends a `POST` request to the server with valid credentials to receive a JWT token.

2. **Server Validates Credentials**  
   - The server verifies the credentials, generates a token, and returns it to the client.

3. **Client Sends Token with API Requests**  
   - For all subsequent API requests, the client includes the JWT token in the request headers:
     ```
     Authorization: Bearer <JWT_Token>
     ```

This ensures secure access to the API and prevents unauthorized usage.
