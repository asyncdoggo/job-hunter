# Create the docker file for python3 and install the required packages
# python version 3.11.x
# FROM python:3.11.0a1-alpine3.14
FROM python:3.11.9-alpine3.19 

# Set the working directory to current directory
WORKDIR /code

# Copy the current directory 
COPY . /code

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port 8000
EXPOSE 8000

# Run the application
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]




