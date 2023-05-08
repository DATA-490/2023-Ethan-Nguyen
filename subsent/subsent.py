import time
import multiprocessing
from threading import Thread
from statistics import mean
from .reddit import Reddit
from .pushshift import pmaw_grab_comments, pmaw_grab_comments_year
from .comment_sentiment import CommentSentiment

class SubSent:

    use_reddit_api = True

    def subreddit_sentiment(self, subreddit, search_term):
        t1 = time.perf_counter()

        reddit_api = Reddit()
        if(not reddit_api.verify_subreddit(subreddit)):
            return {
                "subreddit not found": True,
                "suggested": reddit_api.suggest_subreddit(subreddit)
            }

        comments = []

        if self.use_reddit_api:
            comments = reddit_api.grab_comments(subreddit, search_term)

        else: 
            # using multiprocessing with one process since pmaw requires main thread of main intrepretor    
            comments = multiprocessing.Manager().list()
            proc = multiprocessing.Process(target=pmaw_grab_comments, args=(subreddit, search_term, comments))
            proc.start()
            proc.join()

        if len(comments) ==  0:
            # no mention of search term found in subreddit
            return None

        sentiment_stats = CommentSentiment().comment_sentiment_vader(comments)

        t2 = time.perf_counter()

        sentiment = sentiment_stats['sentiment']
        adjective = ""
        if sentiment < -0.6:
            adjective = 'very negative'
        elif sentiment < -0.1:
            adjective = 'negative'
        elif sentiment < -0.05:
            adjective = 'slightly negative'
        elif sentiment < 0.05:
            adjective = 'neutral'
        elif sentiment < 0.1:
            adjective = 'slightly positive'
        elif sentiment < 0.6:
            adjective = 'positive'
        else:
            adjective = 'very positive'

        # truncate long comment text and check for conflicted tag
        positive_comments = []
        negative_comments = []

        most_contrib = sentiment_stats['most_contrib_comments']
        for idx, comment in enumerate(most_contrib):
            if len(comment['body']) > 400:
                most_contrib[idx]['body'] = comment['body'][:397] + ' ... '

            if comment['senti_score'] > 0:
                positive_comments.append(comment['senti_score'])
            else:
                negative_comments.append(comment['senti_score'])

        if len(positive_comments) >= 0.4 * len(most_contrib) and len(negative_comments) >= 0.4 * len(most_contrib) and mean(positive_comments) > 0.3 and mean(negative_comments) < -0.3:
            adjective = 'conflicted'

        return {
            'adjective': adjective,
            'comments_analyzed': sentiment_stats['comments_analyzed'],
            'most_contrib_comments': sentiment_stats['most_contrib_comments'],
            'execution_time': round(t2 - t1, 2)
        }
    
    def subreddit_sentiment_year(self, subreddit, search_term):
        years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
        procs = [None] * len(years)
        year_comments = multiprocessing.Manager().dict()

        for idx, year in enumerate(years):
            procs[idx] = multiprocessing.Process(target=pmaw_grab_comments_year, args=(subreddit, search_term, year, year_comments))
            procs[idx].start()
        
        for proc in procs:
            proc.join()

        sentiment_over_time = {}
        for year in years:
            if len(year_comments[year]) != 0:
                sentiment_over_time[year]  = CommentSentiment().comment_sentiment_vader(year_comments[year], most_contrib_check=False)
        
        return sentiment_over_time