import feedparser
import codecs
import random
import datetime

# Function to fetch the rss feed and return the parsed RSS
def parseRSS( rss_url ):
    return feedparser.parse( rss_url ) 
    
# Function grabs the rss feed headlines (titles) and returns them as a list
def getHeadlines( rss_url ):
    headlines = []
    #links = []
    
    feed = parseRSS( rss_url )
    for newsitem in feed['items']:
        headlines.append((newsitem['title'], newsitem['link']))
        #headlines.append(newsitem['title'])
        #links.append(newsitem['link'])
    
    return headlines

def main():
# A list to hold all headlines
    allheadlines = []
#alllinks = []
 
# List of RSS feeds that we will fetch and combine
    newsurls = {
    #'yahoonews':        'https://sg.news.yahoo.com/rss/',
    #'malaysiakini':     'https://www.malaysiakini.com/en/news.rss',
    #'thestar':          'http://www.thestar.com.my/rss/editors-choice/news/',
        'googlenews':       'https://www.google.com/alerts/feeds/01553869885481404916/18114317402207573217',
    #  'apnews':           'http://hosted2.ap.org/atom/APDEFAULT/3d281c11a96b4ad082fe88aa0db04305',
    #  'googlenews':       'https://news.google.com/news/rss/?hl=en&amp;ned=us&amp;gl=US',
    #  'themalaysianinsight':   'https://www.themalaysianinsight.com/rss/all'
    #  'yahoonews':        'http://news.yahoo.com/rss/'
}
 
# Iterate over the feed urls
    for key,url in newsurls.items():
    # Call getHeadlines() and combine the returned headlines with allheadlines

        allheadlines = getHeadlines( url )
    
    #allheadlines.extend( getHeadlines( url ) )
 
    file = codecs.open("headlines.yml", "w", "utf-8")
    file.write("categories:"
               "\n- headlines"
               "\nconversations:\n")
# Iterate over the allheadlines list and print each headline

    # headlineQuestion = ["- - What is the news headline today?\n",
    #                     "- - News headline today?\n",
    #                     "- - Tell me a current news\n"]

    headlineAnswer = ["  - Here is what I found, <br />",
                      "  - There you go,<br />",
                      "  - Breaking news is<br />"]

    today_date = datetime.datetime.today().strftime('%A %d %B %Y')
    secure_random = random.SystemRandom()
    for hl, l in allheadlines:
        hl = hl.replace(':', ',')

        file.write("- - " + today_date + "\n")
        file.write(secure_random.choice(headlineAnswer) + "\"<a href=\"" + l + "\">"
                   + hl + "</a>\"\n")

        #file.write("- - News headline today?\n")
        #file.write("  - Here is what I found, \"<a href=\"" + l + "\">" + hl + "</a>\"\n")
        #print(hl + '\t', l)
#for l in alllinks:
#    print(l)
 
# end of code

    file.close()


if __name__ == '__main__':
    main()
