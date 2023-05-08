import time
from pmaw import PushshiftAPI

def pmaw_grab_comments(inputted_subreddit, search_term, comment_list):
    COMMENT_LIMIT = 250

    pushshift = PushshiftAPI()    
    comments = pushshift.search_comments(q=search_term, subreddit=inputted_subreddit, limit=COMMENT_LIMIT)

    for comment in comments:
        comment_list.append(comment)

def pmaw_grab_comments_year(inputted_subreddit, search_term, year, year_comments):
    COMMENT_LIMIT = 20
    
    def epoch_year(cur_year):
        epoch_time = int(time.mktime(time.strptime('%s-01-01 00:00:00' % (str(cur_year),), '%Y-%m-%d %H:%M:%S')))
        return epoch_time
    
    start_year = epoch_year(str(year))
    end_year = epoch_year(str(int(year) + 1))

    pushshift = PushshiftAPI()
    year_comments[year] = list(pushshift.search_comments(q=search_term, subreddit=inputted_subreddit, limit=COMMENT_LIMIT, since=start_year, until=end_year))