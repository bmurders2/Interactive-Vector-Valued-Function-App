FROM python:3.8.5
COPY ./app/requirements.txt /tmp
# WORKDIR /app


# update before moving forward
RUN apt-get update && apt-get upgrade -y
RUN apt-get install g++ unixodbc-dev -y
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

# *** Add a new user here with user id 1xxx with limited access and then proceed 
# RUN useradd -s /bin/bash 1001

# USER 1001

# auto-start web app
# EXPOSE 8080
# ENTRYPOINT ["python"]
# CMD ["dash_app_server.py"]