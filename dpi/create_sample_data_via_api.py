import requests
from faker import Faker
from random import choice, randint

fake = Faker()

# API endpoint for creating workers and patients
WORKER_API_URL = "http://localhost:8000/api/register/worker/"  # Update with your actual API URL
PATIENT_API_URL = "http://localhost:8000/api/register/patient/"  # Update with your actual API URL

# Create hospitals first (ensure these are in the database)
hospitals = [
    {'id': 1, 'name': "City Hospital"},
    {'id': 4, 'name': "Greenwood Medical Center"},
    {'id': 5, 'name': "Sunnydale Clinic"}
]

roles = ['doctor', 'nurse', 'radiologist', 'administrative', 'laborantin']

def create_worker():
    hospital = choice(hospitals)
    role = choice(roles)
    data = {
        'name': fake.name(),
        'email': f'{fake.user_name()}@example.com',  # Valid email format
        'phoneNumber': fake.phone_number()[:10],
        'SSN': fake.ssn(),
        'role': role,
        'hospital': hospital['name'],  # Send the hospital name
    }

    # If the role is 'doctor', add the specialty field
    if role == 'doctor':
        data['specialty'] = fake.job()

    response = requests.post(WORKER_API_URL, data=data)

    if response.status_code == 201:
        print(f"Worker {response.json()}\n (Role: {role}) added successfully to {hospital['name']}")
    else:
        print(f"Failed to add worker: {response.json()['message']}")

def create_patient():
    hospital = choice(hospitals)
    data = {
        'email': f'{fake.user_name()}@example.com',  # Valid email format
        'name': fake.name(),
        'SSN': fake.ssn(),
        'gender': choice(['male', 'female']),
        'address': fake.address(),
        'age': randint(20, 80),
        'logged_at': fake.date_this_decade(),
        'hospital': hospital['name'] , # Send the hospital name
        'phoneNumber': fake.phone_number()[:10],
        'Gender':'male'
    }

    response = requests.post(PATIENT_API_URL, data=data)

    if response.status_code == 201:
        print(f"Patient {data['name']} added successfully to {hospital['name']}")
    else:
        print(f"Failed to add patient: {response.json()['message']}")

 
def create_admin():
    role = "admin"
    data = {
        'name': fake.name(),
        'email': f'{fake.user_name()}@example.com',  # Valid email format
        'phoneNumber': fake.phone_number()[:10],
        'role': role,
        'SSN': fake.ssn(),
    }


    response = requests.post(WORKER_API_URL, data=data)

    if response.status_code == 201:
        print(f"Worker data: \n{response.json()}")
    else:
        print(f"Failed to add worker: {response.json()['message']}")


# Create workers and patients
# for _ in range(5):  # Create 5 workers and 5 patients for each hospital
#     create_worker()
#     create_patient()

create_admin()
# 
#create_worker()
