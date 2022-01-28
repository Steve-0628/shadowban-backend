from requests_oauthlib import OAuth2Session
import json
from get_graphql_endpoint import endpoint

TWITTER_AUTH_KEY = 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

ENDPOINT = endpoint()

twitter_b = OAuth2Session()
twitter_b.headers["authorization"] = "Bearer {}".format(TWITTER_AUTH_KEY)
# twitter_b.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
# twitter_b.headers["Accept"] = "*/*"
# twitter_b.headers["Accept-Language"] = "ja,en-US;q=0.9,en;q=0.8"
# twitter_b.headers["X-Twitter-Active-User"] = "yes"
# twitter_b.headers["content-type"] = "application/json"

# get guest session
guest_session = twitter_b.post("https://api.twitter.com/1.1/guest/activate.json")

twitter_b.headers["x-guest-token"] = guest_session.json()["guest_token"]

# user_id = "1289294626268971008"

# variables = { "count": 700, "userId": user_id,
#             "includePromotedContent": False, "withSuperFollowsUserFields": True, "withBirdwatchPivots": False,
#             "withDownvotePerspective": False, "withReactionsMetadata": False,
#              "withReactionsPerspective": False, "withSuperFollowsTweetFields": True, "withVoice": True, "withV2Timeline": False, "__fs_interactive_text": False, "__fs_responsive_web_uc_gql_enabled": False, "__fs_dont_mention_me_view_api_enabled": False}

# param = {"variables": json.dumps(variables)}

# reply = None

# a = twitter_b.get("https://twitter.com/i/api/graphql/{}/{}".format(ENDPOINT["UserTweetsAndReplies"], "UserTweetsAndReplies"), params=param)
# try:
#     maindata = a.json()["data"]["user"]["result"]["timeline"]["timeline"]["instructions"]
#     for d in maindata:
#         if d["type"] == "TimelineAddEntries":
#             for ent in d["entries"]:
#                 if ent["entryId"].startswith("tweet"):
#                     tmp = ent["content"]["itemContent"]["tweet_results"]["result"]["legacy"]
#                     if "in_reply_to_status_id_str" in tmp:
#                         reply = tmp
#                         print("Found a reply!", tmp["full_text"])
#                         break
#                     # pass
#         # elif d["type"] == "TimelinePinntries":
#         #     print("pinned tweet lol")
#     # print(json.dumps(a.json()["data"]["user"]["result"]["timeline"]["timeline"]))
# except KeyError:
#     print(a.json())

# print(reply["id_str"])
# variables2 = {
#     "focalTweetId":reply["in_reply_to_status_id_str"],
#     # "focalTweetId": "1485942551211233282"
#     # "referrer":"profile",
#     # "controller_data":"DAACDAABDAABCgABAAAAAJAAAAEKAAIAAAAAAQNACAMACAsKAAnc0aoRGUANNQ8ADAMAAAAMAQAAkAAAAAAIQAMBAAAAAA==",
#     # "with_rux_injections":False,
#     "includePromotedContent":False,
#     # "withCommunity":False,
#     # "withQuickPromoteEligibilityTweetFields":True,
#     "withBirdwatchNotes":False,
#     "withSuperFollowsUserFields":True,
#     "withDownvotePerspective":False,
#     "withReactionsMetadata":False,
#     "withReactionsPerspective":False,
#     "withSuperFollowsTweetFields":False,
#     "withVoice":False,
#     # "withV2Timeline":False,
#     "__fs_interactive_text":False,
#     "__fs_responsive_web_uc_gql_enabled":False,
#     "__fs_dont_mention_me_view_api_enabled":False}

# params2 = {"variables": json.dumps(variables2)}
# b = twitter_b.get("https://twitter.com/i/api/graphql/{}/{}".format(ENDPOINT["TweetDetail"], "TweetDetail"), params=params2)

# try:
#     insts = b.json()["data"]["threaded_conversation_with_injections"]["instructions"]
#     for inst in insts:
#         if inst["type"] == "TimeLineAddEntries":
#             for ent in inst["entries"]:
#                 if ent["entryId"].startswith("conversationthread"):
#                     for item in ent["content"]["items"]:
#                         if item["item"]["itemContent"]["tweet_results"]["result"]["legacy"]["user_id_str"] == user_id:
#                             print("No Ghost Ban or Deboosting")
#                             break
# except Exception as e:
#     print(e)
#     # print(b.json())

# # print(json.dumps(b.json()))


get_reply_vars = { "count": 700, "userId": "1289294626268971008",
            "includePromotedContent": False, "withSuperFollowsUserFields": True, "withBirdwatchPivots": False,
            "withDownvotePerspective": False, "withReactionsMetadata": False,
             "withReactionsPerspective": False, "withSuperFollowsTweetFields": True, "withVoice": True, "withV2Timeline": False, "__fs_interactive_text": False, "__fs_responsive_web_uc_gql_enabled": False, "__fs_dont_mention_me_view_api_enabled": False}
get_reply_param = param = {"variables": json.dumps(get_reply_vars)}
replies = twitter_b.get("https://twitter.com/i/api/graphql/{}/{}".format(ENDPOINT["UserTweetsAndReplies"], "UserTweetsAndReplies"), params=get_reply_param)
print(replies)

