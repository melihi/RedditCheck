
![Alt text](https://raw.githubusercontent.com/melihi/RedditCheck/main/diagram.png)

# RedditCheck
RedditCheck Crawl Reddit every 1 minute . 


https://github.com/melihi/RedditCheck/assets/17669771/6a3abba8-e7cf-4bae-a7e4-062ac104c9b0


## Key features
- Take screenshots of Reddit post
- Crawl
  - Comment
  - User id
  - Username
  - post url
  - upvote
- Live Dashboard  
  - Every 3 seconds all data updating in dashboard screen
  - Total Data size , Screenshot count , Following subreddits , Last crawled posts 
- Multithread
  - Automatically scale thread count
- Detetcs no new post and interrupt 
- Several optimizations for slenium browser due to huge resource usage 


# Run Without Docker
```
python manage.py runserver
```
After the runserver command login admin panel and then add your subreddits . 1 minute later crawling will be start .
**Default user credential admin:admin . The database and default user were left intentionally. 

# Docker 
```
sudo docker build -t reddit-check .
```
```
sudo docker run -p 8000:8000 reddit-check
```
