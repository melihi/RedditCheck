from django.conf import settings
from RedditCheckService.models import RedditCrawl
from RedditCheckService.models import VictimList
# Create your views here.
 
from datetime import datetime
from playwright.sync_api import sync_playwright
import threading
import queue

from random import randint


q = queue.Queue()
noNewPost=0
 
 
def schedule_api():
    

    dataList = VictimList.objects.values_list(
        'Subreddit', 'Total_Crawl', 'Last_Crawl')

    print("Scheduler calisiyor")
    # add rows to queue
    for data in dataList:
        q.put(data[0])


    threads = []

    # added 2 for to prevent 0 thread
    # number 20 varies according to system specifications .
    num_threads = q.qsize()//20
    num_threads += 2
    if q.qsize()==1:
        num_threads=1;
    # creat thread and pass the queue
    for _ in range(num_threads):
        t = threading.Thread(target=GetSubdredit, args=())
        threads.append(t)
       # t.start()
    # start threads
    for t in threads:
        if not t.is_alive():
            #sleep(randint(1,3))
            t.start()
            
    # wait threads for finishing their jobs
    for t in threads:
        t.join()
    
    print("finished")

    


def GetSubdredit():
    while not q.empty():
        
        sname=q.get() 
        with sync_playwright() as pw:
                print("getsubdreddit calisiyor")
                # create browser instance
                browser = pw.chromium.launch(headless=True)
                context = browser.new_context(viewport={"width": 1920, "height": 1080})
                page = context.new_page()

                  
                
                #postbrowser = pw.chromium.launch(headless=False)
                #postcontext = browser.new_context(viewport={"width": 1920, "height": 1080})
                postpage = context.new_page()

                # go to url
                page.goto("https://www.reddit.com/r/"+sname+"/")
                # scroll to the bottom:
                _prev_height = -1
                _max_scrolls = 3
                _scroll_count = 0
                while _scroll_count < _max_scrolls:
                    # Execute JavaScript to scroll to the bottom of the page
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    # Wait for new content to load (change this value as needed)
                    page.wait_for_timeout(3000)
                    # Check whether the scroll height changed - means more pages are there
                    new_height = page.evaluate("document.body.scrollHeight")
                    if new_height == _prev_height:
                        break
                    _prev_height = new_height
                    _scroll_count += 1

                #page.wait_for_selector("div[class=rpBJOHq2PR60pnwJlUyP0]")  # wait for content to load
                
                parsed = []
                stream_boxes = page.locator("div[data-testid=\"post-container\"]")
                # crawl start time
                current_datetime = datetime.now()
                formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                for box in stream_boxes.element_handles():
                    if noNewPost > 5:
                            print("No new Post exiting")
                            browser.close()
                            break
                    try:
                        upvote=""
                        time=""
                        subdredditid=""
                        commentcount=""
                        comments=""
                        authorid=""
                    
                        # promoted post has very long id . ignore pormoted posts
                        if len(box.get_attribute('id'))>15:
                            continue
                        postpage.goto("https://www.reddit.com"+box.query_selector( "a[class=\"SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE\"]").get_attribute("href"))
                        postpage.wait_for_timeout(3000)
                        post=postpage.locator("shreddit-post")
                        comment=postpage.locator("shreddit-comment-tree")
                        # take screenshot of post
                        post.screenshot(path="media/screenshot/screenshot-"+box.get_attribute('id')+".png")
                        for x in post.element_handles():
                            #print(x.get_attribute("created-timestamp"))
                            upvote=x.get_attribute("score")
                            time=x.get_attribute("created-timestamp")
                            subdredditid=x.get_attribute("subreddit-id")
                            commentcount=x.get_attribute("comment-count")
                            authorid=x.get_attribute("author-id")
                            #print(x.inner_text())
                        for y in comment.element_handles():
                            #print(y.inner_text())     
                            comments=y.inner_text()         
                        #parsed.append({
                        title= box.query_selector("h3").inner_text()
                        # "url": box.query_selector(".tw-link").get_attribute("href"),
                        username= box.query_selector("a[data-testid=\"post_author_link\"]").inner_text()
                        content= box.query_selector("div[class=\"STit0dLageRsa2yR4te_b\"]").inner_text()
                        postid=box.get_attribute('id')
                        
                            
                        postlink="https://www.reddit.com"+box.query_selector( "a[class=\"SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE\"]").get_attribute("href"),
                    # subdredditid=subdredditid,
                        #commentcount=commentcount,
                        
                        # <time datetime="2020-04-25T17:22:41.245Z" title="Saturday, April 25, 2020 at 8:22:41 PM GMT+3"><!--?lit$6987230037$-->3 yr. ago</time>
                            # tags are not always present:
                            #"tags": box.query_selector(".tw-tag").inner_text() if box.query_selector(".tw-tag") else None,
                        
                        #})
                        a = {"SubReddit_Name":sname,
                            "Title":title,
                            "Posted_By":username,
                            "Content":content,
                            "Date":time,
                            "Comment_Log":comments,
                            "Upvote":upvote,
                            "Search_Start": formatted_datetime,
                            "Search_Finished":"",
                            "Post_Link":postlink[0],
                            "Post_id":postid,
                            "Post_image":"screenshot/screenshot-"+postid+".png",
                            "Comment_image":"",
                            "Author_id":authorid}
                        
                        
                        print(a["Post_id"])
                        #sync_to_async(save_data_to_database(a))
                        x = threading.Thread(target=save_data_to_database, args=(a,))
                        x.start()
                     

                    except Exception as e :
                        print(e)
                    
                browser.close()           
                        
                
                # get HTML
                #print(page.content())
             
def save_data_to_database(data):
    print("save data calisiyor")
    try:
        # Veri tabanına kaydetme işlemleri burada gerçekleştirilir
        RedditCrawl.objects.create(SubReddit_Name=data["SubReddit_Name"], Title=data["Title"], Posted_By=data["Posted_By"], Content=data["Content"], Date=data["Date"], Comment_Log=data["Comment_Log"], Upvote=data["Upvote"], Search_Start=data["Search_Start"], Search_Finished="", Post_Link=data["Post_Link"], Post_id=data["Post_id"], Post_image=data["Post_image"], Comment_image="", Author_id=data["Author_id"])
                    
                                # update total crawled post
        row = RedditCrawl.objects.filter(
                    SubReddit_Name=data["SubReddit_Name"]).count()  # Güncellenecek satırı alın
        t = VictimList.objects.get(Subreddit=data["SubReddit_Name"])
        t.Total_Crawl = row  # change field
        t.save()  # t
    except Exception as e:
         if "UNIQUE constraint failed" in str(e):
            global noNewPost
            noNewPost +=  1