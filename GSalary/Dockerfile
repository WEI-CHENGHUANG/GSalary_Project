FROM python:3.9.6
# COPY is actually executed on the host
COPY . /app 
WORKDIR /app
# RUN gets executed inside of the container.
RUN ["pip3", "install", "-r", "requirements.txt"]
EXPOSE 3000

ENTRYPOINT ["python3", "/app/backend/app.py"]