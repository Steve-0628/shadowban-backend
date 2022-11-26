from flask import Flask
from flask_cors import CORS
from requests_oauthlib import OAuth1Session, OAuth2Session
import os
import time
import json
from get_graphql_endpoint import endpoint

app = Flask(__name__)
CORS(app)

TWITTER_AUTH_KEY = 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

ENDPOINT = endpoint()

@app.route('/{screen_name}')
def shadowban(screen_name):
    # DO IT
    pass




@app.route("/<screen_name>")
def searchban(screen_name):
    returnjson = {
                "timestamp": time.time(),
                "profile": {
                    # "id": "7080152",
                    # "screenName": "TwitterJP",
                    # "protected": False,
                    # "suspended": False,
                    # "has_tweets": True,
                    "exists": False,
                    "error": None
                },
                # "check": {
                #     "search": 1484727214419628037,
                #     "suggest": True,
                #     "ghost": {"ban": True},
                #     "reply": {"ban": False, "tweet": "1480819689898987523", "in_reply_to": "1369626114381901828"}
                # }
            }

    
    # twitter = OAuth1Session(TWITTER_IPHONE_CK, TWITTER_IPHONE_CS)
    twitter_b = OAuth2Session()
    twitter_b.headers["Authorization"] = "Bearer {}".format(TWITTER_AUTH_KEY)

    # check rate limit
    # response = twitter_b.get("https://api.twitter.com/1.1/application/rate_limit_status.json")
    # print(response.json())

    # profile_url = "https://api.twitter.com/1.1/users/show.json"
    # params = {"screen_name": screen_name}
    # profile_info = twitter_b.get(profile_url, params=params)
    # profile_json = profile_info.json()
    # print(profile_json)
    # if profile_info.status_code == 200:
    #     returnjson["profile"]["exists"] = True
    #     returnjson["profile"]["id"] = profile_json["id_str"]
    #     returnjson["profile"]["screenName"] = profile_json["screen_name"]
    #     returnjson["profile"]["protected"] = profile_json["protected"]
    # elif profile_info.status_code == 403:
    #     returnjson["profile"]["suspended"] = True
    #     return returnjson
    # else:
    #     returnjson["profile"]["error"] = profile_json["errors"][0]["message"]
    #     # return returnjson

    # if profile_json["protected"] == True:
    #     returnjson["profile"]["protected"] = True
    #     return returnjson

    # if profile_json["statuses_count"] == 0:
    #     returnjson["profile"]["has_tweets"] = False
    #     return returnjson
    # else:
    #     returnjson["profile"]["has_tweets"] = True

    # check whether the user has any tweets
    usertlurl = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = {"screen_name": screen_name, "count": 200}

    usertl_b = twitter_b.get(usertlurl, params=params)
    usertl = usertl_b
    usertl_json = usertl.json()
    # # print(usertlb)
    # if "errors" in usertlb:
    #     return "An error occurred" # TODO: Better error handling
    # if len(usertlb) == 0:
    #     return "No tweets found"  # TODO: Better error handling

    if len(usertl_json) == 0:
        returnjson["profile"]["has_tweets"] = False
        return returnjson

    returnjson["profile"]["has_tweets"] = True

    if usertl.status_code == 200:
        returnjson["profile"]["exists"] = True
        returnjson["profile"]["id"] = usertl_json[0]["user"]["id_str"]
        returnjson["profile"]["screen_name"] = usertl_json[0]["user"]["screen_name"]
        # returnjson["profile"]["protected"] = usertl_json["protected"]
    elif usertl.status_code == 403:
        returnjson["profile"]["suspended"] = True
        return returnjson
    else:
        if "error" in usertl_json and usertl_json["error"] == "Not authorized.":
            returnjson["profile"]["protected"] = True
            returnjson["profile"]["suspended"] = True
            returnjson["profile"]["has_tweets"] = False
            return returnjson
        returnjson["profile"]["error"] = usertl_json
        return returnjson

    # if usertl_json["protected"] == True:
    #     returnjson["profile"]["protected"] = True  ## how do you determen protected and suspended
    #     return returnjson

    # if usertl_json["statuses_count"] == 0:
    #     returnjson["profile"]["has_tweets"] = False
    #     return returnjson
    # else:
    #     returnjson["profile"]["has_tweets"] = True

    returnjson["tests"] = {
    "search": True,    ## Search ban
    "typeahead": True, ## suggest ban
    "ghost": {"ban": None},
    "more_replies": {"ban": False, "tweet": "-1", "in_reply_to": "-1"}
}

    # searchurl = "https://api.twitter.com/1.1/users/search.json"
    # params = {"q": "from:@{}".format(screen_name), "count": 1}
    # search = twitter_b.get(searchurl, params=params).json()
    # print(search)
    # if len(search) == 0:
    #     returnjson["test"]["search"] = "ban"
    #     return returnjson
    # else:
    #     return returnjson

    searchurl_v2 = "https://api.twitter.com/2/search/adaptive.json"
    params_v2 = {"q": "from:@{}".format(screen_name), "count": 1, "spelling_corrections": 0, "tweet_search_mode": "live"}
    search_v2 = twitter_b.get(searchurl_v2, params=params_v2).json()
    search_tweets = search_v2["globalObjects"]["tweets"]
    if search_tweets == {}:
        returnjson["tests"]["search"] = False
        # returnjson["tests"]["typeahead"] = False
    else:
        returnjson["tests"]["search"] = True

    
    suggestions = twitter_b.get("https://api.twitter.com/1.1/search/typeahead.json?src=search_box&result_type=users&q=@" + screen_name).json()
    try:
        returnjson["tests"]["typeahead"] = len([1 for user in suggestions["users"] if user["screen_name"].lower() == screen_name.lower()]) > 0
    except:
        returnjson["tests"]["typeahead"] = False

    ## get replies
    ## Start GraphQL

    guest_session = twitter_b.post("https://api.twitter.com/1.1/guest/activate.json")

    twitter_b.headers["x-guest-token"] = guest_session.json()["guest_token"]

    user_id = returnjson["profile"]["id"]

    reply = None

    print(user_id)

    get_reply_vars = { "count": 700, "userId": user_id,
            "includePromotedContent": False, "withSuperFollowsUserFields": False, "withBirdwatchPivots": False,
            "withDownvotePerspective": False, "withReactionsMetadata": False,
             "withReactionsPerspective": False, "withSuperFollowsTweetFields": False, "withVoice": False, "withV2Timeline": False, "__fs_interactive_text": False, "__fs_responsive_web_uc_gql_enabled": False, "__fs_dont_mention_me_view_api_enabled": False}
    get_reply_param = param = {"variables": json.dumps(get_reply_vars)}
    replies = twitter_b.get("https://twitter.com/i/api/graphql/{}/{}".format(ENDPOINT["UserTweetsAndReplies"], "UserTweetsAndReplies"), params=get_reply_param)
    # print(replies.text)
    

    try:
        maindata = replies.json()["data"]["user"]["result"]["timeline"]["timeline"]["instructions"]
        for d in maindata:
            if d["type"] == "TimelineAddEntries":
                for ent in d["entries"]:
                    if ent["entryId"].startswith("tweet"):
                        tmp = ent["content"]["itemContent"]["tweet_results"]["result"]["legacy"]
                        if "in_reply_to_status_id_str" in tmp:
                            reply = tmp
                            # print("Found a reply!", tmp["full_text"])
                            break
        tweet_detail_vars = {
            "focalTweetId":reply["in_reply_to_status_id_str"],
            "includePromotedContent":False,
            "withBirdwatchNotes":False,
            "withSuperFollowsUserFields":False,
            "withDownvotePerspective":False,
            "withReactionsMetadata":False,
            "withReactionsPerspective":False,
            "withSuperFollowsTweetFields":False,
            "withVoice":False,
            "__fs_interactive_text":False,
            "__fs_responsive_web_uc_gql_enabled":False,
            "__fs_dont_mention_me_view_api_enabled":False
        }
        tweetdetails = twitter_b.get("https://twitter.com/i/api/graphql/{}/{}".format(ENDPOINT["TweetDetail"], "TweetDetail"), params={"variables": json.dumps(tweet_detail_vars)})

        insts = tweetdetails.json()["data"]["threaded_conversation_with_injections"]["instructions"]

        showmore = False

        for inst in insts:
            
            if inst["type"] == "TimelineAddEntries":
                for ent in inst["entries"]:
                    print(ent["entryId"])
                    if ent["entryId"].startswith("conversationthread"):
                        ghostban = True
                        for item in ent["content"]["items"]:
                           
                            if "tweet_results" in item["item"]["itemContent"] and item["item"]["itemContent"]["tweet_results"]["result"]["legacy"]["user_id_str"] == user_id:
                                
                                returnjson["tests"]["ghost"] = {"ban": False}
                                ghostban = False
                                break
                        if ghostban:
                            print("Hello")
                            returnjson["tests"]["ghost"] = {"ban": True}

                    if ent["entryId"].startswith("cursor-bottom"):
                        print("hi")
                        returnjson["tests"]["ghost"] = {}
                        returnjson["tests"]["more_replies"] = {}
                        break

                    if ent["entryId"].startswith("cursor-showmorethreadsprompt"):
                        showmore = True
                        cursor_vars = tweet_detail_vars
                        cursor_vars["cursor"] = ent["content"]["itemContent"]["value"]
                        cursor = twitter_b.get("https://twitter.com/i/api/graphql/{}/{}".format(ENDPOINT["TweetDetail"], "TweetDetail"), params={"variables": json.dumps(cursor_vars)})

                        cursor_insts = cursor.json()["data"]["threaded_conversation_with_injections"]["instructions"]
                        for c_i in cursor_insts:
                            if c_i["type"] == "TimelineAddEntries":
                                if len(c_i["entries"]) == 0:
                                    returnjson["tests"]["more_replies"] = {"ban": True}
                                    break
                                for c_ent in c_i["entries"]:
                                    if c_ent["entryId"].startswith("conversationthread"):
                                        more = True
                                        print("more")
                                        for c_item in c_ent["content"]["items"]:
                                            if c_item["item"]["itemContent"]["tweet_results"]["result"]["legacy"]["user_id_str"] == user_id:
                                                
                                                returnjson["tests"]["ghost"] = {"ban": False}
                                                returnjson["tests"]["more_replies"] = {"ban": True, "tweet":reply["id_str"], "in_reply_to": c_item["item"]["itemContent"]["tweet_results"]["result"]["legacy"]["id_str"]}
                                                more = False
                                                break
                                        if more:
                                            returnjson["tests"]["ghost"] = {"ban": True}
                                            returnjson["tests"]["more_replies"] = {"ban": True}
        if not showmore:
            returnjson["tests"]["more_replies"] = {
}
    except KeyError as e:
        # print(Exception.with_traceback(e)) 
        returnjson["tests"]["ghost"] = {}
        returnjson["tests"]["more_replies"] = {}


    print("ban" in returnjson["tests"]["more_replies"])
    print("ban" in returnjson["tests"]["ghost"])
    print(returnjson["tests"]["ghost"])
    if "ban" not in returnjson["tests"]["more_replies"] and "ban" in returnjson["tests"]["ghost"] and returnjson["tests"]["ghost"]["ban"] == False:
        returnjson["tests"]["more_replies"] == {"ban": False}

    return returnjson


if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get("PORT", 5000), host="0.0.0.0")
