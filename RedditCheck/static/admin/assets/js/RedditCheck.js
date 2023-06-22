
//Global variables
var FollowedSubreddits = [];
var addedSubreddits = [];
var RedditStatistics = new Map();
var TotalCrawl = 0;

setInterval(function () {
    $.ajax({
        url: "/api/getVictimList/",
        method: "GET",
        success: function (data) {
            // İstek başarılı olduğunda burada işlemler yapabilirsiniz

            // set labels
            for (var i = 0; i < data.Subreddits.length; i++) {
                FollowedSubreddits.push = data.Subreddits[i];
            }
            FollowedSubreddits = data.Subreddits;
            $("#VictimRedditCount").text(data.Subreddits.length);
        },

        error: function (xhr, status, error) {
            // İstek hata verdiğinde burada işlemler yapabilirsiniz
            console.log("Hata: " + error);
        }/* ,
        async: false */
    });

    $.ajax({
        url: "/api/getTotalCrawl/",
        method: "GET",
        success: function (data) {
            // İstek başarılı olduğunda burada işlemler yapabilirsiniz

            $("#TotalCrawl").text(data.total_url);
            TotalCrawl = data.total_url;
        },
        error: function (xhr, status, error) {
            // İstek hata verdiğinde burada işlemler yapabilirsiniz
            console.log("Hata: " + error);
        }
    });
    $.ajax({
        url: "/api/getScreenshotCount/",
        method: "GET",
        success: function (data) {
            // İstek başarılı olduğunda burada işlemler yapabilirsiniz


            $("#TotalScreenshot").text(data.Total_Screenshot);
        },
        error: function (xhr, status, error) {
            // İstek hata verdiğinde burada işlemler yapabilirsiniz
            console.log("Hata: " + error);
        }
    });

    $.ajax({
        url: "/api/getTotalCrawlSize/",
        method: "GET",
        success: function (data) {
            // İstek başarılı olduğunda burada işlemler yapabilirsiniz


            $("#TotalDataSize").text(data.Total_Size + " GB");
        },
        error: function (xhr, status, error) {
            // İstek hata verdiğinde burada işlemler yapabilirsiniz
            console.log("Hata: " + error);
        }
    });

    $.ajax({
        url: "/api/getTotalCrawlSubreddit/",
        method: "GET",
        success: function (data) {
            // İstek başarılı olduğunda burada işlemler yapabilirsiniz


            // Get keys and values using Object.keys() and forEach()
            Object.keys(data.Total_Crawls_Subreddit).forEach(function (key) {
                var value = data.Total_Crawls_Subreddit[key];

                setBar(key, value);

            });
        },
        error: function (xhr, status, error) {
            // İstek hata verdiğinde burada işlemler yapabilirsiniz
            console.log("Hata: " + error);
        }
    });

    $.ajax({
        url: "/api/getLatestCrawl/",
        method: "GET",
        success: function (data) {
            // İstek başarılı olduğunda burada işlemler yapabilirsiniz

            $('#title').text(data.title);
            $('#username').text(data.username + " (" + data.author + ")   👍🏻" + data.upvote);
            $('#subreddit').text("r/" + data.subreddit);
            $('#postcontent').text(data.content);

            $("#screenshot").attr('src', "/media/screenshot/screenshot-" + data.postid + ".png");
        },
        error: function (xhr, status, error) {
            // İstek hata verdiğinde burada işlemler yapabilirsiniz
            console.log("Hata: " + error);
        }
    });
}, 3000);




function setBar(key, value) {

    var element = $('#prgoresbars');

    let percent = (value / TotalCrawl) * 100;
    percent = percent.toFixed(2);
    // Add the inner HTML content
    if ($("#" + key).length == 0) {
        //it doesn't exist
        data = `  <h4 class="small fw-bold">` + key + `<span class="float-end">` + percent + `</span></h4>
        <div class="progress mb-4">
            <div id="`+ key + `"class="progress-bar bg-success" aria-valuenow="50" aria-valuemin="0"
                aria-valuemax="100" style="width: `+ percent + `%;"><span
                    class="visually-hidden">100%</span></div>
        </div>`
        element = element.append(data);
    } else {
        $("#" + key).css({ 'width': percent + "px;" });
    }




}

