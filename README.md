# Interactive-Vector-Valued-Function-App
Interactive demo web app featuring an on-the-fly supervised trained support vector machine for regression of a vector valued function. The web app is created via the Dash ML framework. 

The primary purpose is to demonstrate the advantage of leveraging Docker for data science development without installing multiple software tools and frameworks, develop in consistently reproducible environments, as well as effectively developing with a simulated "production"-like environment with natural agile and CI/CD practices. 

To run and interact with this example, use the docker-compose UP command on the docker-compose.yml file. To have the web application run, either uncomment out the bottom section of the Dockerfile or execute 'python dash_app_server.py' within the web app's running container. The default port is set to port 8080 for the web app.


Dash/Plotly: https://plotly.com/

App Screenshot:
![app-ex-img-1](https://github.com/bmurders2/Interactive-Vector-Valued-Function-App/blob/master/screenshots/app_ex_img_1.PNG)

Example Plot Screenshot:
![app-plot-ex-img-1](https://github.com/bmurders2/Interactive-Vector-Valued-Function-App/blob/master/screenshots/plot_ex_img_1.png)

Example Plot Screenshot:
![app-plot-ex-img-2](https://github.com/bmurders2/Interactive-Vector-Valued-Function-App/blob/master/screenshots/plot_ex_img_2.png)
