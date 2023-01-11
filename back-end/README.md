# CMP Backend
The CMP backend is built using the Django web framework. It handles all of the data storage and business logic for the Comrade Market Place.
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
### Prerequisites
- `Python 3.6` and above
- `django  4.1.1`
- Postgresql => Version 13
### Installing
1. Clone the repository to your local machine:
```
git clone git@github.com:DSCKabarak/ComradeMarketPlace.git
```
2. Change into the project directory:
```
cd cmp-backend
```
3. Create a virtual environment and activate it:
```
virtualenv venv
source venv/bin/activate
```
4. Install the project dependencies:
```
pip install -r requirements.txt
```
5. Create a new file named `.env`in the project root directory to store your environment variables.
6. Run the migrations:
```
python manage.py makemigrations
python manage.py migrate
```
7. Run the development server:
```
python manage.py runserver
```
8. The backend will be accessible at `http://localhost:8000/`.

It is recommended to use a virtual environment in the development process.

## API endpoints
The following API endpoints are available for interacting with the CMP backend:
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| POST | /comrade-market-place/api/auth/login | To login to an existing account |
| POST | /comrade-market-place/api/auth/register | To create a new user account |
| POST | /comrade-market-place/api/auth/logout | To logout of a logged in account |
| GET | /comrade-market-place/api/auth/profile | To get a logged in user's profile details |
| GET | /comrade-market-place/products | To get a list of all products |

- You can add additional endpoints as required.
- You can also include the sample request and response of each endpoint with proper format and data type
- It will be helpful to include some extra information like request parameter, body parameters and response codes etc.
