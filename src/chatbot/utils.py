def get_all_tweets(client, username: str, user_id: str, tool_name: str = "X.SearchRecentTweetsByUsername") -> list:
    """
    Fetch all available tweets for a given username using pagination.
    
    Args:
        client: Arcade client instance
        username: Twitter username to fetch tweets for
        user_id: Arcade user ID
        tool_name: Name of the Arcade tool to use
        
    Returns:
        list: All collected tweets
    """
    all_tweets = []
    next_token = None
    
    while True:
        # Prepare inputs (include next_token if we have one)
        inputs = {"username": username, "max_results": 100}
        if next_token:
            inputs["next_token"] = next_token
            
        # Execute the request
        response = client.tools.execute(
            tool_name=tool_name,
            inputs=inputs,
            user_id=user_id,
        )
        
        # Get tweets from the response
        new_tweets = response.output.value['data']
        all_tweets.extend(new_tweets)
        
        # Get next token if available
        next_token = response.output.value["meta"].get("next_token", None)
        
        # If no next token, we've reached the end
        if not next_token:
            break
            
    return all_tweets