FROM python:3.8.5
COPY . /app
WORKDIR /app

# update before moving forward
RUN apt-get update
RUN apt-get upgrade -y
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# *** Add a new user here with user id 1xxx with limited access and then proceed 
# 	-- use case for PRD containers --
# ***

# auto-start web app
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["dash_app_server.py"]