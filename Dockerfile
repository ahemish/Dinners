FROM tiangolo/uwsgi-nginx-flask:python3.7
RUN apt update
RUN pip install flask_sqlalchemy
RUN pip install flask_login

RUN pip3 install flask_sqlalchemy
RUN pip3 install flask_login
RUN pip install pymysql
RUN pip3 install pymysql

COPY ./App/app /app
