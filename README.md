# Subreddit Sentiment
* **Author**: Ethan Nguyen, github: [ethanhn11](https://github.com/ethanhn11/)
* **Major**: B.S. Computer Science
* **Year**: 2023

# Type of project

Flask web application for sentiment analysis of subreddits (isolated communities on social media website reddit.com).

# Purpose (including intended audience)

Allows users of reddit.com to gain insight into how a particular subreddit feels about a given topic.

# Explanation of files

* `static/` - static assets for use in Flask's templates
    - `htmx.min.js`, `particles.min.js`: JavaScript libraries for AJAX and particle background respectively
    - `particles.json`: configuration file for particle background
    - `script.js`: main JavaScript file, handles loading state, return from graph over time, among other things
    - `styles.css`: styling for certain elements
* `subsent/` - collection of Python files that handle main functionality of sentiment analysis
    - `comment_sentiment.py`: returns a sentiment score given a list of comments
    - `pushshift.py`: all functions relating to PushShift service
    - `reddit.py`: all functions relating to Reddit API
    - `subsent.py`: main driver and connection from comment scraping to sentiment analysis
* `templates/` - all Jinja templates returned by Flask
    - `index.html`: home page
    - `result.html`: return from an query
    - `result-error.html`: return from an erroneous query
* `app.py` - main file for Flask (routes and their associated views)

# Completion status 

## Enhancements: 

Potential enhancements include:

- [ ] a dashboard to control specific parameters in the backend (e.g. when to switch between PushShift and Reddit API, the max post to traverse, etc.)
- [ ] add specialized models that are trained on particular popular subreddits

# Can someone else work on this project? 
No

# Public Display/dissemination
* Spring 2023 College of Engineering, Computer Science, and Construction Management Design Expo

# License
