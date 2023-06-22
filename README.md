
![Alt text](https://raw.githubusercontent.com/melihi/RedditCheck/main/diagram.png)

# RedditCheck
RedditCheck Crawling Service



python manage.py makemigrations
python manage.py migrate 
python3 manage.py createsuperuser


# Docker 
sudo docker build -t reddit-check .
sudo docker run -p 8000:8000 reddit-check