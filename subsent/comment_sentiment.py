from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class CommentSentiment:

    DOWNVOTE_SCALEBACK_FACTOR = 3
    HEAV_NEG_SENT_CUTOFF = -0.6
    HEAV_NEG_FACTOR = 3
    # HEAV_POS_SENT_CUTOFF = 0.6
    # HEAV_POS_FACTOR = 2

    def comment_sentiment_vader(self, comments, most_contrib_check=True):
        vader_analyzer = SentimentIntensityAnalyzer()

        sentiment = 0
        vote_count = 0

        raw_sentiment = 0 # no changes in scaling, 1 upvote == 1 scale
        raw_vote_count = 0 

        most_contrib = []

        for comment in comments:
            vader_score = vader_analyzer.polarity_scores(comment['body'])['compound']
            scaling_factor = comment['score'] # downvotes will reverse trend

            # changing scaling factor depending on comment attributes

            # downvoted comment
            if scaling_factor < 0: 
                scaling_factor /= self.DOWNVOTE_SCALEBACK_FACTOR
                vote_count += abs(comment['score']) / self.DOWNVOTE_SCALEBACK_FACTOR

            # heavily negative comment
            elif vader_score < self.HEAV_NEG_SENT_CUTOFF: 
                scaling_factor *= self.HEAV_NEG_FACTOR
                vote_count += comment['score'] * self.HEAV_NEG_FACTOR

            # elif vader_score < self.HEAV_POS_SENT_CUTOFF: 
            #     scaling_factor *= self.HEAV_POS_FACTOR
            #     vote_count += comment['score'] * self.HEAV_POS_FACTOR

            else:
                vote_count += comment['score']

            # score with negative scaling
            comment_senti_score = vader_score * scaling_factor
            sentiment += comment_senti_score

            # raw score calcuations
            raw_sentiment += vader_score * comment['score']
            raw_vote_count += abs(comment['score'])

            if most_contrib_check:
                most_contrib.append({'abs_score': comment_senti_score,
                                    'senti_score': vader_score, 
                                    'body': comment['body'], 
                                    'author': comment['author'], 
                                    'permalink': comment['permalink']})

        sentiment /= vote_count
        raw_sentiment /= raw_vote_count

        if most_contrib_check:
            most_contrib.sort(key=lambda comm: abs(comm['abs_score']), reverse=True)

            return {
                'sentiment' : sentiment,
                'comments_analyzed': len(comments),
                'raw_sentiment': raw_sentiment, 
                'most_contrib_comments': most_contrib[:min(max(int(0.1 * len(most_contrib)), len(most_contrib)), 25)] # show 10% (or all if less than 10 total comments) capped at 25 
            }

        else:
            return {
                'sentiment': sentiment,
                'comments_analyzed': len(comments)
            }