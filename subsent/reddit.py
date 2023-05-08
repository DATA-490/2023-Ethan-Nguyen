import praw
import prawcore.exceptions
from threading import Thread

class Reddit:
    
    POST_TRAVERSAL_LIMIT = 20
    
    def __init__(self):
        self.reddit = praw.Reddit(site_name="subredditsentiment") # loading credential settings from praw.ini

    def grab_comments(self, inputted_subreddit, search_term):
        try:
            subreddit = self.reddit.subreddit(inputted_subreddit)        

            self.all_comments = {} # key: thread_id, value: list of dictonary where each dictonary is info for a comment
            threads = [] 
        
            # loop through posts that return from subreddit search for term
            for thread_id, submission in enumerate(subreddit.search(search_term, limit=self.POST_TRAVERSAL_LIMIT)):
                # each thread assigned to one submission/post
                threads.append(Thread(target=self._comment_traversal, args=(thread_id, submission, search_term)))
                threads[thread_id].start()

            for thread in threads:
                thread.join()
            
            return [comment for list_of_post_comments in self.all_comments.values() for comment in list_of_post_comments]
        
        except prawcore.exceptions.ResponseException as e:
            if str(e) == 'received 503 HTTP response':
                print('503')

            return []

    def _comment_traversal(self, thread_id, submission, search_term):
        submission.comments.replace_more(limit=0) # removing all instances of MoreComments

        for comment in submission.comments.list():
            if search_term.lower() in comment.body.lower():
                comment_attr = {'body': comment.body, 'score': comment.score, 'comment_id': comment.id,
                                'author': str(comment.author), 'permalink': comment.permalink}
                
                if thread_id in self.all_comments:
                    self.all_comments[thread_id].append(comment_attr)
                else:
                    self.all_comments[thread_id] = [ comment_attr ] 

    def verify_subreddit(self, subreddit):
        try:
            self.reddit.subreddits.search_by_name(subreddit, exact=True)
            try:
                self.reddit.subreddit(subreddit).subreddit_type
                return True
            except:
                return False
        except:
            return False
        
    def suggest_subreddit(self, subreddit):
        suggested = self.reddit.subreddits.search_by_name(subreddit, exact=False, include_nsfw=False)
        return [ s.display_name for s in suggested ][:3]