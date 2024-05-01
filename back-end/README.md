# CMP Backend
These instructions will help you set up the Comrade Marketplace Backend on your local machine for development and testing purposes.

### Prerequisites
- `Python 3.10` or higher
- `PostgreSQL` 13 or higher
- `RabbitMQ` 3.10 or higher

### Generating a Secret Key (This is Optional)
1. Run the following command to generate a new secret key:
```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
2. This will output a new secret key, which you can then copy and paste into your `.env` file.
3. In your `.env` file, add a new line with the following format: `SECRET_KEY='your_secret_key'`
4. Make sure to replace `your_secret_key` with the actual key that was generated.
5. Save the changes made in the `.env` file.
### Installing
1. Clone the repository to your local machine:
    ```
    git clone git@github.com:DSCKabarak/ComradeMarketPlace.git
    ```
2. Change into the project directory:
    ```
    cd back-end
    ```
3. Create a virtual environment and activate it:
    ```linux
    virtualenv venv
    source venv/bin/activate
    ```
4. Install the project dependencies:
    ```
    pip install -r requirements.txt
    ```
5. Create a new file named `.env`in the project root directory to store your environment variables. In your `.env` file, you can add environment variables like this:
    ```
    SECRET_KEY= <your_secret_key>
    SETTINGS=development
    ALLOWED_HOSTS=localhost 127.0.0.1
    CORS_ALLOWED_ORIGINS=http://localhost:3000
    DB_NAME= <your_db_name>
    DB_USER= <your_db_user>
    DB_PASS= <your_db_password>
    DB_HOST= <your_db_host>
    DB_PORT= <your_db_port>
    
    # Email Configuration
    EMAIL_HOST_USER=<your_email@gmail.com>
    EMAIL_HOST_PASSWORD=<your_email_password>
    EMAIL_PORT=<smtp_port>
    EMAIL_USE_TLS=True
    DEFAULT_FROM_EMAIL=<your_default_from_email@gmail.com>
    EMAIL_HOST=<smtp.gmail.com>

    # Celery Configuration
    CELERY_BROKER_URL=pyamqp://guest@localhost//
    CELERY_RESULT_BACKEND=rpc://
    CELERY_RESULT_PERSISTENT=True
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=True
    ```

    #### If using google mail, you need to create an app password for the EMAIL_HOST_PASSWORD. You can follow the instructions [here](https://support.google.com/accounts/answer/185833?hl=en).

6. Run the migrations:
    ``` 
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    ```

7. Collect the static files:
    ```
    python manage.py collectstatic
    ```

8. Generate the API schema:
    ```
    python manage.py spectacular --color --file schema.yml
    ```

9. Start the development server:
    ```
    python manage.py runserver
    ```
10. Start RabbitMQ server:
- Open a new terminal tab and enter the following commands:
    - **Linux** 
    ```
    sudo systemctl start rabbitmq-server
    ```
    - **Windows**
    ```
    rabbitmq-server start
    ```
11. Start the celery worker:
 - Open a new terminal window and enter the following command:
    ```
    celery -A cmp worker -l info
    ```

The backend will be accessible at `http://localhost:8000/`. or any other specified port and IP address.

It is recommended to use a virtual environment in the development process.


## Running with Docker
If you have Docker installed on your machine, you can run the project using Docker containers. Follow these steps:

1. Set the environment variables in the `.env.prod` file for the application, and in the `.env.prod.db` file for the database.
   
2. Ensure that the database names are the same in both files.
   
3. In the `.env.prod` file, set the `DB_HOST` environment variable to `db`. This will allow the application to connect to the database container.
   
4. In the `.env.prod.db` file, set the database credentials to the same value as the ones in the `.env.prod` file.
   
5. In `entrypoint.sh`, set  `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, and `DJANGO_SUPERUSER_PASSWORD` to the desired values for the superuser account.
   
6. While in the `back-end` directory, you can run the following script to build and run the project using Docker:

    ```bash
    ./scripts/startup.sh
    ```

7. if the script does not have the necessary permissions, you can run the following command to give it the necessary permissions:

    ```bash
    chmod +x scripts/entrypoint.sh
    chmod +x scripts/startup.sh
    ```

## API Documentation
After running the server, you can access the API documentation at the following URLs:
- Swagger Documentation: `http://localhost:8000/api/schema/swagger-ui/`
- Redoc Documentation: `http://localhost:8000/api/schema/redoc/`


## Contributing
Contributions are welcome! If you find any issues or have ideas for new features, please create a new issue or submit a pull request.