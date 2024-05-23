# installation Instructions

## 1. Clone the repository::
```
git clone https://github.com/sasheshsingh/socialnetwork
```

## 2. Navigate into the project directory:
```
cd socialnetwork
```

## 3. Create a virtual environment (optional but recommended). Ref[https://sasheshsingh.medium.com/a-beginners-guide-of-installing-virtualenvwrapper-on-ubuntu-ce6259e4d609](https://sasheshsingh.medium.com/a-beginners-guide-of-installing-virtualenvwrapper-on-ubuntu-ce6259e4d609):
```
workon myenv
```
## 4. create .env file. Add following variables
DB_NAME\
DB_USER\
DB_PASSWORD\
DB_HOST\
DB_PORT
```
nano .env
```

## 5. Install the project dependencies:
```
pip install -r requirements.txt
```
## 6. Create the migrations
```shell
python manage.py makemigrations
```
## 7. Migrate the Migrations files
```shell
python manage.py migrate
```
## 8. Start the Django Server:
```shell
python manage.py runserver 0.0.0.0:8000
```


# Docker Setup
## Building and Running Containers
### Build and start the Docker containers:
```shell
docker-compose up --build
```

# API Documentation
## API Documentation is avaiable at the below route:
```shell
/api/docs/
```