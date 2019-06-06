FROM python:3.7-alpine
WORKDIR /app
ENV FLASK_ENV development
ENV FLASK_APP example
COPY . .
#RUN python -m pip install flask
RUN ["pip", "install", "flask"]
RUN chmod 777 main.py
EXPOSE 5000
#CMD [ "python", "main.py" ]
CMD ["flask", "run", "-h", "0.0.0.0"]