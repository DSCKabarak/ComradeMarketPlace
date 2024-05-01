# Use the official Python image as the base image
FROM python:3.10.4-alpine

# Set the PATH environment variable
ENV PATH="/scripts:${PATH}"

# Update and install required packages
RUN apk update && \
    apk add --no-cache build-base

# Copy the requirements file
COPY ./requirements.txt /requirements.txt

# Install build dependencies for installing Python packages
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers

# Install Python dependencies
RUN pip install --no-cache-dir -r /requirements.txt

# Remove build dependencies
RUN apk del .tmp

# Create the /app directory
RUN mkdir /app

# Copy the project code into the container
COPY . /app

# Set the working directory
WORKDIR /app

# Copy the scripts directory
COPY ./scripts /scripts

# Make the scripts executable
RUN chmod +x /scripts/*


# Create a non-root user
RUN adduser -D user

# Change ownership of the /app directories

RUN mkdir -p /app/marketplace/migrations/
RUN touch /app/marketplace/migrations/__init__.py

RUN mkdir -p /app/notifications/migrations/
RUN touch /app/notifications/migrations/__init__.py

RUN mkdir -p /app/accounts/migrations/
RUN touch /app/accounts/migrations/__init__.py

# Set permissions for migration files
RUN chmod -R 755 /app/*/migrations/

RUN chown -R user:user /app 
# Switch to the non-root user
USER root

# Set the entrypoint script
CMD ["./scripts/entrypoint.sh"]

USER user