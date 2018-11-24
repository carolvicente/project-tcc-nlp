'''

result_type
    mixed : Include both popular and real time results in the response.
    recent : return only the most recent results in the response
    popular : return only the most popular results in the response.

since_id 
Returns results with an ID greater than (that is, more recent than) the specified ID. 
There are limits to the number of Tweets which can be accessed through the API. 
If the limit of Tweets has occured since the since_id, the since_id will be forced to the oldest ID available.

max_id  
Returns results with an ID less than (that is, older than) or equal to the specified ID.

'''


def build_tweet_api_query(query):
    result_type = 'mixed'
    lang = 'pt'
    count = '15'
    tweet_mode = 'extended'
    base_query = '{query}&result_type={result_type}&count={count}&lang={lang}&tweet_mode={tweet_mode}' \
        .format(query=query, lang=lang, result_type=result_type, count=count, tweet_mode=tweet_mode)
    return base_query
