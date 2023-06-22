from django.contrib import admin
from RedditCheckService.models import *
# Register your models here.


class RedditCrawlAdmin(admin.ModelAdmin):
    list_display = ("SubReddit_Name", "Posted_By", "Post_id",
                    "Title", "Search_Start", "Search_Finished", "photo")
    list_filter = ("SubReddit_Name", "Search_Start")
    readonly_fields = ("SubReddit_Name", "Posted_By", "Post_id", "Title", "Search_Start", "Search_Finished",
                       "Post_image", "Author_id", "Date", "Comment_Log", "Content", "Upvote", "Post_Link", "Comment_image")
    search_fields = ("SubReddit_Name", "Posted_By", "Post_id", "Title", "Search_Start", "Search_Finished",
                     "Post_image", "Author_id", "Comment_Log", "Content", "Post_Link")
    

class VictimListAdmin(admin.ModelAdmin):
    list_display = ("Subreddit", "Total_Crawl", "Last_Crawl")
    # list_filter = ("SubReddit_Name","Search_Start")
    readonly_fields = ("Total_Crawl", "Last_Crawl")

    actions = ['Add_Subreddit_Name_For_Crawling_Service']

    


class LiveAdmin(admin.ModelAdmin):
     list_display = ("Test",)
    


 

 
admin.site.register(RedditCrawl, RedditCrawlAdmin)
admin.site.register(VictimList, VictimListAdmin)
admin.site.register(Live, LiveAdmin)
# set header titile
admin.site.site_header = "RedditCheck"
admin.site.site_title = "ReddiThreadCheck"
admin.site.index_title = "Reddit Threads"
