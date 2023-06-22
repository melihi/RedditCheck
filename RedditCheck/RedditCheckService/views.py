from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from RedditCheckService.models import *
# Create your views here.
import os
import json


@api_view(['GET'])
def getSubRedditData(request):
    isim = request.GET.get('name')

    """  RedditCrawl.objects.create(
     SubReddit_Name=isim, Title="title", Content=data, Search_Start="", Search_Finished="") """

    return Response({'message': 'Processing request ...'})


@ api_view(['GET'])
def getTotalCrawl(request):
    row = RedditCrawl.objects.count()

    return Response({'total_url': row})


@ api_view(['GET'])
def getTotalCrawlSubreddit(request):

    names = VictimList.objects.values_list('Subreddit', flat=True)
    count = {}
    for i in names:
        tmp = RedditCrawl.objects.filter(SubReddit_Name=i).count()
        count[i] = tmp

    return Response({'Total_Crawls_Subreddit':  count})


@ api_view(['GET'])
def getLatestCrawl(request):

    names = RedditCrawl.objects.latest('Search_Finished')

    data = {'author':  names.Author_id, 'postid': names.Post_id, 'content': names.Content, 'upvote': names.Upvote,
            'title': names.Title, 'username': names.Posted_By, 'subreddit': names.SubReddit_Name}

    return Response(data)


@ api_view(['GET'])
def getVictimList(request):
    names = VictimList.objects.values_list('Subreddit', flat=True)

    return Response({'Subreddits': names})


@ api_view(['GET'])
def getScreenshotCount(request):
    count = 0
    for _, _, files in os.walk("media/screenshot/"):
        count += len(files)
    return Response({'Total_Screenshot': count})


@ api_view(['GET'])
def getTotalCrawlSize(request):

    # assign folder path
    folder_path = 'media/screenshot/'

    total_size = 0

    for path, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(path, file)
            total_size += os.path.getsize(file_path)
    database_size = os.path.getsize("db.sqlite3")
    database_size = database_size / (1024**3)
    database_size = round(database_size, 3)

    # Convert bytes to gigabytes
    total_size = total_size / (1024**3)
    total_size = round(total_size, 3)
    size = total_size+database_size
    return Response({'Total_Screenshot': total_size, 'Database': database_size, 'Total_Size': size})


def Live(request):
    print("livee")


@ api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Merhaba, Dünya!'})
