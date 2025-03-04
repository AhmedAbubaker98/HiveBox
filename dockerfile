# Use an official lightweight Python image as a base
FROM python:3.10

# Set the working directory inside the container
WORKDIR /src

# Copy the application files into the container
COPY ./src /src
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on (5000 by default)
EXPOSE 5000

# Run the Flask app
CMD ["python", "/src/app.py"]
