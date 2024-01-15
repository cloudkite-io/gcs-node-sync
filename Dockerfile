FROM google/cloud-sdk:latest
RUN apt update && apt install -y time && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY ./app .
RUN pip install -r requirements.txt
CMD [ "python3", "main.py" ] 