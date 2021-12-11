![GitHub repo size](https://img.shields.io/github/repo-size/PudgyElderGod/amphibia_forum_mongo)
![Lines of code](https://img.shields.io/tokei/lines/github/pudgyeldergod/amphibia_forum_mongo) 
![Website](https://img.shields.io/website?down_color=red&down_message=Offline&up_color=green&up_message=Online&url=http%3A%2F%2Famphibia-forum.dev.thomis.gay%2F)
![Gay](https://img.shields.io/badge/Me-Gay-blueviolet)

# Amphibia Forum
The Amphibia Forum is a place for fans of the ongoing Disney cartoon Amphibia to talk about the show. It features a main message board, comments for each forum post, and user accounts/auth. 

Beyond that, it is a demonstration of competency in the following fields: Flask & MongoDB, Docker, Docker Compose, CapRover, and DigitalOcean Droplets.

## Getting Started
No installation necessary to visit and use the live forum at http://amphibia-forum.dev.thomis.gay/. Browse without an account or sign up for full access.

If you'd rather download and run the application locally, check the prerequisites and follow the installation instructions below. 

### Prerequisites

pip3 or similar (optional but reccomended)

#### That's all you need to get started, but downloads will be involved in setup later. Preview requirements.txt to see what will be downloaded later. 

### Installing
Clone this repo:
```
$ git clone https://github.com/angelinaolmedo7/digDigDogs
```

Navigate to the parent folder and install requirements with pip3
```
$ pip3 install -r requirements.txt
```
Alternately check requirements.txt and download each manually. But like. Why would you.

Export app.py to flask 
```
$ export FLASK_APP=app.py
```

Run with flask
```
$ flask run
```
Visit the local address displayed in the terminal in the web browser of your choice.


## Contributing
If you run into any issues or feel like contributing, go ahead and submit a pull request!

# Building the Container
### Prerequisites
Docker

### Build the image
```
docker build -t amphibia-image .
```

### Build the container
```
docker run -p 5000:5000 --rm --name amphibia-container amphibia-image
```

### When you're done, double-check that relevant images and containers have been removed 
Remove all images with names that contain amphibia
```
docker images -a | grep "amphibia" | awk '{print $3}' | xargs docker rmi
```

Remove all containers with names that contain flask
```
docker ps -a | grep "amphibia" | awk '{print $3}' | xargs docker rmi
```
___
