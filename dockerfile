# Use a base image with the desired OS and dependencies
FROM debian:latest

# Update package lists and install necessary dependencies
RUN apt-get update && apt-get install -y \
    clang \
    python3 \
    python3-dev \
    swig \
    make 
    


# Copy the contents of your project into the container
COPY . /app

# Set the working directory inside the container
WORKDIR /app/server

# Get most recent version of physics lib
RUN make clean && make 

# Set the library path to the current directory
ENV LD_LIBRARY_PATH=/app/server

EXPOSE 50124
    
# Copy and run the entrypoint script
#CMD ["python3", "server.py"]