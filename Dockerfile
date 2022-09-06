FROM google/cloud-sdk:latest
WORKDIR /app

COPY ./app .
RUN pip install -r requirements.txt
CMD [ "python3", "main.py" ] 