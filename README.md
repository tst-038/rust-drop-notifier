# Rust Drop Notifier

A Python-based project to monitor new Rust drops and send notifications to Discord channels via webhooks.

## Features
- Monitors a Rust drops website for new updates.
- Sends rich, embedded notifications to a Discord channel.
- Scalable using Docker.
- Simple setup for sharing with others.

## Version
Current Version: **0.1.0**

## Prerequisites
- Python 3.10+
- Docker and Docker Compose

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/rust-drop-notifier.git
cd rust-drop-notifier
```

### 2. Set Up Configuration
#### 1. Create an `.env` file
In the project directory, create a file called .env and define the following variables:
- DROP_URL: The URL of the Rust drops website you want to monitor. (default=`https://twitch.facepunch.com`)
- WEBHOOK_URL: The Discord webhook URL where notifications will be sent. (**required**)
- ROLE_ID: The Discord role ID that should be tagged when a notification is sent. This is only used if the event status is “Event Live”.
- CHECK_INTERVAL: The interval (in seconds) at which the program will check for updates on the Rust drops website. The default is 3600 seconds (1 hour). You can change it to suit your needs.

Example `.env` file:
```env
DROP_URL=https://rustdrops.facepunch.com/
WEBHOOK_URL=https://discord.com/api/webhooks/your-webhook-id
ROLE_ID=your-role-id
CHECK_INTERVAL=3600  # Default is 1 hour
```

### 2. Optional: Customize Docker Configuration
If you’re using Docker, you can set the values of the environment variables in the docker-compose.yml file. Docker Compose will automatically read from the `.env` file or from your system’s environment.
The `docker-compose.yml` file should look like this (make sure WEBHOOK_URL is set correctly):
```yaml
services:
  rust-drop-notifier:
    build: .
    environment:
      - WEBHOOK_URL=${WEBHOOK_URL}
      - DROP_URL=${DROP_URL}
      - ROLE_ID=${ROLE_ID}
      - CHECK_INTERVAL=${CHECK_INTERVAL}
    restart: unless-stopped
```
This ensures that Docker Compose will use the .env variables when running the service.

## 3. Install Dependencies
If you plan to run the project locally without Docker, you can install the necessary Python dependencies using pip. First, create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
Then, install the required dependencies:
```bash
pip install -r requirements.txt
```

## 4. Run the Project
### With Docker
To build and run the project in a Docker container, use:
```bash
docker-compose up --build 
```

The project will now monitor the Rust drops website for new updates and send notifications to your Discord channel when a new drop occurs.

### Without Docker
If you’re running the project directly, you can start the script with:
```bash
python main.py
```

The project will now monitor the Rust drops website for new updates and send notifications to your Discord channel when a new drop occurs.