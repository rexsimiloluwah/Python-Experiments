# Use the Base python image 
FROM python:3.7-slim 
FROM tiangolo/uwsgi-nginx:python3.6

# Change the working directory 
WORKDIR /usr/src/app

# Copy the app the the working dir
COPY . .

# Install dependencies 
RUN pip install -r requirements.txt

# RUN THE APP USING UWSGI
CMD ["uwsgi","app.ini"]