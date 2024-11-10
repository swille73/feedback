# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
#ENV STREAMLIT_APP_TITLE="Mein erster Streamlit-App"
#ENV STREAMLIT_APP_TEXT="Hello World!"

# Set the working directory in the container
WORKDIR /streamlit_app

# Copy the current directory contents into the container at /streamlit_app
COPY . /streamlit_app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]