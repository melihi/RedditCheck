from django.db import models
from django.utils.safestring import mark_safe
from datetime import datetime
# Create your models here.
class RedditCrawl(models.Model):
    SubReddit_Name = models.CharField(max_length=200,default="")
    Title = models.CharField(max_length=300,default="")
    Posted_By = models.CharField(max_length=300,default="")
    Author_id=models.CharField(max_length=30,default="")
    Date = models.CharField(max_length=20,default="")
    Comment_Log = models.TextField(default="")
    Content = models.TextField(default="")
    Upvote = models.CharField(max_length=20,default="")
    Search_Start = models.DateTimeField("Start Time")
    Search_Finished = models.DateTimeField("Finish Time",auto_now_add=True)
    Post_Link = models.TextField(default="")
    Post_id = models.CharField(max_length=30,default="",unique=True)# block duplicate
    Post_image = models.ImageField(upload_to='screenshot/',default="")
    Comment_image = models.ImageField(upload_to='images/%y',default="")
    class Meta:
        verbose_name= "Crawls"
        verbose_name_plural = "Crawl SubReddit"
    def __str__(self):
        return self.SubReddit_Name
     
    def photo(self):
        return mark_safe('<img src="{}" width="200px" />'.format(self.Post_image.url))
    photo.short_description = 'Image'
    photo.allow_tags = True

    

class VictimList(models.Model):
    Subreddit= models.CharField(max_length=100,default="",unique=True)
    Total_Crawl = models.PositiveIntegerField(default=0)
    Last_Crawl = models.DateTimeField(auto_now_add=True)
    #Add_Date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name= "SubReddits for Crawling Service"
        verbose_name_plural = "Victim List"
    def __str__(self):
        return self.Subreddit 
    


class Live(models.Model):
    Test= models.CharField(max_length=100,default="",unique=True)
   
    class Meta:
        verbose_name= "Live Stream"
        verbose_name_plural = "Live"
    def __str__(self):
        return self.Test 


