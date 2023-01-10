### BACKEND DEVELOPMENT 

- `Python 3.6` and above
- `django  4.1.1`
- Postgresql => Version 13

Install all requirements in the `requirements.txt`

It is recommended to use a virtual environment in the development process.

## API endpoints
| HTTP Verbs | Endpoints | Action |
| --- | --- | --- |
| POST | /comrade-market-place/api/auth/login | To login to an existing account |
| POST | /comrade-market-place/api/auth/register | To create a new user account |
| POST | /comrade-market-place/api/auth/logout | To logout of a logged in account |
| GET | /comrade-market-place/api/auth/profile | To get a logged in user's profile details |
| GET | /comrade-market-place/products | To get a list of all products |
