FROM google/cloud-sdk:latest
RUN apt update && apt install -y time && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY ./app .
# Install venv if not already installed
RUN apt-get update && apt-get install -y python3-venv

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Activate the virtual environment and install dependencies
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD [ "python3", "main.py" ] 