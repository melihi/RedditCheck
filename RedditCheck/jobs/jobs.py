from django.conf import settings
from RedditCheckService.models import RedditCrawl
from RedditCheckService.models import VictimList
# Create your views here.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import asyncio
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from PIL import Image
from io import BytesIO
import threading
import queue

q = queue.Queue()


def schedule_api():
    dataList = VictimList.objects.values_list(
        'Subreddit', 'Total_Crawl', 'Last_Crawl')

    print("Calisiyorr")
    # add rows to queue
    for data in dataList:
        q.put(data[0])

    threads = []

    # added 2 for to prevent 0 thread
    # number 20 varies according to system specifications .
    num_threads = q.qsize()//20
    num_threads += 2

    # creat thread and pass the queue
    for _ in range(num_threads):
        t = threading.Thread(target=GetSubdredit, args=(q,))
        threads.append(t)
        t.start()
    # start threads
    for t in threads:
        t.start()
    # wait threads for finishing their jobs
    for t in threads:
        t.join()


def GetSubdredit(subname):

    options = Options()
    options.add_argument("--headless")

    # driver for post visit
    Postdriver = webdriver.Chrome(options=options)

    # disable loading images for performance
    options.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.images": 2})
    # dirver for collect posts
    driver = webdriver.Chrome(options=options)
    while not subname.empty():

        sname = subname.get()
        # set reddit link
        subreddit_url = "https://www.reddit.com/r/"+sname+"/"

        # open subreddit post
        driver.get(subreddit_url)
        driver.implicitly_wait(10)
        # error counter for detect now new post
        noNewPost = 0
        # start time
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        # 0-10 means 10 scroll down to bottom of loaded page. Bigger number increase the depth .
        for i in range(0, 10):
            # select post container
            elements = driver.find_elements(
                By.CSS_SELECTOR, 'div[data-testid="post-container"]')
            print(len(elements))

            driver.implicitly_wait(10)

            # if element not found scroll
            if len(elements) <= 0:
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                continue
            # exit if 10 posts already saved it means there is no new post .
            # next subdomain collection will start.
            if noNewPost > 10:
                print("No new Post exiting")
                break
            # loop over founded elements
            for index, title in enumerate(elements):

                try:

                    if len(title.get_attribute("id")) < 15 and len(title.text) > 1:
                        print(title.get_attribute("id"))
                        clas = 'div[id="UserInfoTooltip--' + \
                            title.get_attribute("id")+"\"]"
                        vote = 'div[id="vote-arrows-' + \
                            title.get_attribute("id")+"\"]"

                        user = title.find_element(By.CSS_SELECTOR, clas).text
                        head = title.find_element(
                            By.CLASS_NAME, '_eYtD2XCVieq6emjKBH3m').text
                        date = title.find_element(
                            By.CSS_SELECTOR, 'span[data-click-id="timestamp"]').text
                        upvote = title.find_element(By.CSS_SELECTOR, vote).text
                        content = title.find_element(
                            By.CLASS_NAME, 'STit0dLageRsa2yR4te_b').text
                        comment = title.find_element(
                            By.CLASS_NAME, 'FHCV02u6Cp2zYL0fhQPsO').text
                        outboundLink = ""
                        link = title.find_element(
                            By.CSS_SELECTOR, 'a[class="SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"]').get_attribute("href")
                        # print(link)
                        if 'data-testid="outbound-link"' in title.get_attribute("innerHTML"):
                            outboundLink = title.find_element(
                                By.CSS_SELECTOR, 'a[data-testid="outbound-link"]').get_attribute("href")

                        test = title.get_attribute("id")

                        Postdriver.get(link)
                        Postdriver.implicitly_wait(10)
                        postscrn = Postdriver.find_elements(
                            By.TAG_NAME, 'shreddit-post')

                        div_width = postscrn[0].size['width']
                        div_height = postscrn[0].size['height']

                        # take screnshot
                        screenshot = Postdriver.get_screenshot_as_png()

                        # crop div
                        left = postscrn[0].location['x']
                        top = postscrn[0].location['y']
                        right = left + div_width
                        bottom = top + div_height
                        image = Image.open(BytesIO(screenshot))

                        # Crop Div
                        div_screenshot = image.crop((left, top, right, bottom))
                        div_screenshot.save(
                            "media/screenshot/screenshot-"+test+".png")

                        # set author id
                        authorid = postscrn[0].get_attribute('author-id')
                        comment = ""
                        for c in postscrn:
                            comment += c.text.replace("Reply\nreply\nShare\nShare",
                                                      "[Endf of Comment]") + "\n"

                        # finish time
                        comment = comment.replace(
                            "Additional comment actions", "[End of comment tree]")
                        # add post to database
                        RedditCrawl.objects.create(SubReddit_Name=sname, Title=head, Posted_By=user, Content=content +
                                                   "\n"+outboundLink, Date=date, Comment_Log=comment, Upvote=upvote, Search_Start=formatted_time, Search_Finished="", Post_Link=link, Post_id=test, Post_image="screenshot/screenshot-"+test+".png", Comment_image="", Author_id=authorid)
                        # update total crawled post
                        row = RedditCrawl.objects.filter(
                            SubReddit_Name=sname).count()  # Güncellenecek satırı alın
                        t = VictimList.objects.get(Subreddit=sname)
                        t.Total_Crawl = row  # change field
                        t.save()  # th
                except Exception as e:
                    # print("hata")
                    # print(e)
                    if "UNIQUE constraint failed" in str(e):
                        noNewPost += 1

                    continue
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(10)
        # Selenium sürücüsünü kapatın
    driver.quit()
    Postdriver.quit()
