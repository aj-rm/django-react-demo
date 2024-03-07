# Base image
FROM node:20

# create and set working directory
RUN mkdir /app
WORKDIR /app

# Add current directory code to working directory
COPY . /app/

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Remove package-lock.json and node_modules
RUN rm -rf /app/package-lock.json
RUN rm -rf /app/node_modules

# Install environment dependencies
RUN npm install

# Build the app
RUN npm run build

EXPOSE 5173

# CMD python manage.py runserver 0.0.0.0:$PORT
# CMD gunicorn djdocker.wsgi:application --bind 0.0.0.0:$PORT