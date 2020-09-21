FROM python:3.8.5
COPY ./app/requirements.txt /data/
# WORKDIR /app


# update before moving forward
RUN apt-get update && apt-get upgrade -y
RUN apt-get install g++ unixodbc-dev -y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install msodbcsql17 -y
RUN ACCEPT_EULA=Y apt-get install mssql-tools
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r /data/requirements.txt

# *** Add a new user here with user id 1xxx with limited access and then proceed 
# RUN useradd -s /bin/bash 1001

# USER 1001

# auto-start web app
# EXPOSE 8080
# ENTRYPOINT ["python"]
# CMD ["dash_app_server.py"]