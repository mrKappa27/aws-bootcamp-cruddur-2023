# Week 1 — App Containerization

### TL;DR
I followed the week1 live and went through all the todolist points (TODO: WIP)
I completed the assigned homework and doing that made me more knowledgeable about Docker and app containerization in general.
I set up Docker in my local environment, my DockerHub account, pushed the images we built during the week1 to dockerhub too. Then I went deeper about multistage builds, healthchecks and the best practices about dockerfiles and their implementation.
Finally I ran the solution on and AWS EC2 instance on which I've installed docker, pulled the image from DockerHub, ran the two images and tested them.
TODO: Notifications backend+frontend, dynamodb local, postgres container  

## What we did
### Build Container

Backend 
```sh
docker build -t  backend-flask ./backend-flask
```

Frontend 
```sh
docker build -t  frontend-react-js ./frontend-react-js
```

### Run Container

Backend 
```sh
docker run --rm -p 4567:4567 -it backend-flask
```
Note: `-it` stands for interactive terminal

Frontend 
```sh
docker run --rm -p 3000:3000 -d frontend-react-js
```
Note: `-d` stands for detached mode

Env override
```sh
docker run  --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask
```

## Required Homeworks/Tasks

- Run the dockerfile CMD as external script ✅6
    - Remember: shebang and export PATH
- Push and tag the image to DockerHub ✅
    - Followed [official documentation](https://docs.docker.com/docker-hub/repos/#:~:text=To%20push%20an%20image%20to,docs%2Fbase%3Atesting%20).)
    - Created a new [public repository](https://hub.docker.com/repository/docker/mrkappa27/aws-bootcamp-cruddur-2023/general) on DockerHub
    - Tagged both images (retagged the already existing image)
    - Pushed the images to DockerHub
- Multistage build ⏸️
- Healthcheck Docker compose v3 ⏸️
- Best practices dockerfile + implement ⏸️
- Install Docker in local machine + test run containers ✅
    - ![Running Docker locally](assets/week1-docker-local.png)
- Launch EC2 with Docker installed and test container pushed to dockerhub ✅
    - Launched EC2 with Amazon Linux 2 AMI with dedicated metadata for installing docker `yum install docker`
    - Tested if Docker was correctly installed with: `docker -v` 
    - Added my user to the Docker group with55:
        ```
        sudo usermod -a -G docker ec2-user`
        id ec2-user
        # Reload a Linux user's group assignments to Docker w/o logout
        newgrp docker
        ```
    - Enabled the service for autostart: `sudo systemctl enable docker.service`
    - Started it manually for the first time: `sudo systemctl start docker.service`
    - Verified the service status: `sudo systemctl status docker.service`
    - Pulled both images from DockerHub:
        ```
         docker pull mrkappa27/aws-bootcamp-cruddur-2023:backend-flask
         docker pull mrkappa27/aws-bootcamp-cruddur-2023:frontend-react-js
        ```
    - Ran the images but on EC2:
         ```
         docker run  --rm -p 3000:3000 -e REACT_APP_BACKEND_URL='http://ec2-3-120-180-149.eu-central-1.compute.amazonaws.com:4567' -d mrkappa27/aws-bootcamp-cruddur-2023:frontend-react-js
         docker run  --rm -p 4567:4567 -d -e FRONTEND_URL='*' -e BACKEND_URL='*' mrkappa27/aws-bootcamp-cruddur-2023:backend-flask
        ```   
    - ![Running Docker EC2](assets/week1-docker-ec2.png)