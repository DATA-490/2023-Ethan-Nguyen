from flask import Flask, request, render_template
from subsent import SubSent

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/sentiment")
def sentiment():
    subreddit = request.args.get('subreddit')
    searchterm = request.args.get('searchterm')
    
    subsent = SubSent()
    sentiment_results = subsent.subreddit_sentiment(subreddit, searchterm)

    if sentiment_results == None:
        error_msg = "No mention of '%s' found in subreddit r/%s" % (searchterm, subreddit)
        return render_template('result-error.html', error_msg=error_msg)
    
    elif "subreddit not found" in sentiment_results:
        error_msg = "subreddit \"r/%s\" does not exist or is privated" % (subreddit)
        return render_template('result-error.html', error_msg=error_msg, suggested=sentiment_results['suggested'])

    return render_template('result.html', sub=subreddit, term=searchterm, sentiment_adj=sentiment_results['adjective'], 
                           count=sentiment_results['comments_analyzed'], most_contrib=sentiment_results['most_contrib_comments'],
                           time=sentiment_results['execution_time'])

@app.route("/sentovertime")
def sentiment_over_time():

    subreddit = request.args.get('subreddit')
    searchterm = request.args.get('searchterm')

    subsent = SubSent()
    sentiment_results = subsent.subreddit_sentiment(subreddit, searchterm)

    if sentiment_results == None or "subreddit not found" in sentiment_results:
        return str(-1)

    sentiment_over_time = subsent.subreddit_sentiment_year(subreddit, searchterm)
    
    response = {'years': [], 'sentiment': []}
    for year in sentiment_over_time:
        response['years'].append(year)
        response['sentiment'].append(sentiment_over_time[year]['sentiment'])
    
    return response

