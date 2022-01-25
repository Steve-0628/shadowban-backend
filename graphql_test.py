from requests_oauthlib import OAuth2Session
import json


TWITTER_AUTH_KEY = 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'


twitter_b = OAuth2Session()
twitter_b.headers["authorization"] = "Bearer {}".format(TWITTER_AUTH_KEY)
# twitter_b.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
# twitter_b.headers["Accept"] = "*/*"
# twitter_b.headers["Accept-Language"] = "ja,en-US;q=0.9,en;q=0.8"
# twitter_b.headers["X-Twitter-Active-User"] = "yes"
# twitter_b.headers["content-type"] = "application/json"

# get guest session
guest_session = twitter_b.post(
    "https://api.twitter.com/1.1/guest/activate.json")
# print(guest_session.json())

twitter_b.headers["x-guest-token"] = guest_session.json()["guest_token"]

variables = {"userId": "1289294626268971008", "count": 4, 
            "includePromotedContent": False, "withSuperFollowsUserFields": True, "withBirdwatchPivots": False, 
            "withDownvotePerspective": False, "withReactionsMetadata": False,
             "withReactionsPerspective": False, "withSuperFollowsTweetFields": True, "withVoice": True, "withV2Timeline": False, "__fs_interactive_text": False, "__fs_responsive_web_uc_gql_enabled": False, "__fs_dont_mention_me_view_api_enabled": False}

param = {"variables": json.dumps(variables)}

a = twitter_b.get(
    "https://twitter.com/i/api/graphql/DpEuAKkyDVJL_KgSa_xxiA/UserTweetsAndReplies", params=param)
print(json.dumps(a.json()))
