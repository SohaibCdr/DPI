# Hospital Management System API Documentation

## Authentication
All protected endpoints require a JWT token in the Authorization header.

### Login
- **URL**: `/api/login/`
- **Method**: POST
- **Body**:
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Success Response**: Returns JWT tokens and actor information

### Token Refresh
- **URL**: `/api/token/refresh/`
- **Method**: POST
- **Body**: `{"refresh": "string"}`

## Hospital Management

### Create Hospital
- **URL**: `/api/hospital/create/`
- **Method**: POST
- **Body**:
  ```json
  {
    "name": "string",
    "address": "string"
  }
  ```

### Get Hospital Details
- **URL**: `/api/hospital/`
- **Method**: GET
- **Query Parameters**: `name=string`
- **Response**: Hospital details including staff counts

### List All Hospitals
- **URL**: `/api/hospitals/`
- **Method**: GET
- **Response**: List of all hospitals with details

## Patient Management

### Register Patient
- **URL**: `/api/register/patient/`
- **Method**: POST
- **Body**:
  ```json
  {
    "email": "string",
    "address": "string",
    "name": "string",
    "phoneNumber": "string",
    "SSN": "string",
    "dateOfBirth": "string",
    "Gender": "string",
    "emergencyContactName": "string",
    "emergencyContactPhone": "string",
    "hospital": "string"
  }
  ```

### List Patients
- **URL**: `/api/patients/`
- **Method**: GET
- **Query Parameters**: 
  - `hospital=string`
  - `page=number`
- **Response**: Paginated list of patients

### Get Patient Details
- **URL**: `/api/patients/{id}/`
- **Method**: GET

### Search Patient by SSN
- **URL**: `/api/search-patient/{SSN}/`
- **Method**: GET

### Edit Patient
- **URL**: `/api/patient/edit/{id}/`
- **Method**: PUT
- **Body**: Patient fields to update

## Staff Management

### Register Worker
- **URL**: `/api/register/worker/`
- **Method**: POST
- **Body**:
  ```json
  {
    "role": "string", // doctor, nurse, administrative, radiologist, or laborantin
    "email": "string",
    "name": "string",
    "phoneNumber": "string",
    "SSN": "string",
    "hospital": "string",
    "specialty": "string" // required for doctors only
  }
  ```

### List Workers
- **URL**: `/api/workers/`
- **Method**: GET
- **Query Parameters**: 
  - `hospital=string`
  - `page=number`
- **Response**: Paginated list of all staff by role

### Update Worker
- **URL**: `/api/worker/edit/`
- **Method**: PUT
- **Body**:
  ```json
  {
    "role": "string",
    "id": "number",
    "fields_to_update": "values"
  }
  ```

### Delete Worker
- **URL**: `/api/worker/delete`
- **Method**: DELETE
- **Body**:
  ```json
  {
    "role": "string",
    "id": "number"
  }
  ```

### Search Workers
- **URL**: `/api/search-worker/`
- **Method**: GET
- **Query Parameters**: `name=string`

## Analytics

### Patient Graph Data
- **URL**: `/api/patient-graph-data/`
- **Method**: GET
- **Query Parameters**: `hospital=string`
- **Response**: Weekly patient registration data for graphs
