## Flask, Nginx, and Docker-compose to run a containerized Web app

To run the web app using docker-compose :- 

1. Install Docker and Docker-compose

2. Clone the repository and cd into 'flask-nginx-dockercompose' where the docker-compose.yml is. The docker-compose.yml file contains the configuration for each containerized service, there are 3 containerized services in this webapp :-

- flask (For the main flask app),
- nginx (Reverse proxy to uWSGI for running the app),
- mysql (Database)

```
$ git clone https://github.com/rexsimiloluwah/Tinkering
$ cd flask-nginx-dockercompose
```

3. Build the app using docker-compose
```
$ docker-compose build
```

4. Run the app
```
$ docker-compose up
```

5. View running services 
```
$ docker-compose ps
```

6. Stop services
```
$ docker-compose stop
```

7. Stop the entire containers and bring down mysql volumes
```
$ docker-compose down --volumes
```

