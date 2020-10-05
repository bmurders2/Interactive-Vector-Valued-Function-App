FROM python:3.8.6-slim
COPY ./app /project_code/app/

WORKDIR /project_code/app


# update and install app deps before moving forward
RUN apt-get update && apt-get upgrade -y
RUN apt-get install nano g++ unixodbc-dev curl gnupg1 gnupg2 -y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install msodbcsql17 -y
RUN ACCEPT_EULA=Y apt-get install mssql-tools
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r /project_code/app/requirements.txt

# # for PRD
# # *** Add a new user here with user id 1xxx with limited access and then proceed 
# RUN useradd -m -u 1001 -s /usr/bin/bash appuser_docker
# USER appuser_docker

# # auto-start web app
# EXPOSE 8080
# ENTRYPOINT ["python"]
# CMD ["dash_app_server.py"]