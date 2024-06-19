FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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




