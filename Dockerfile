# Use the official Python image as the base image
FROM python:3.10-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    curl \
    && apt-get clean

# Install TA-Lib from source
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY backend/requirements.txt /app/

# Install Python dependencies
RUN python3 -m ensurepip --upgrade && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt || cat requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port your application will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
