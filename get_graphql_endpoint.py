import requests
import re
import json

TWTTR_BASE_URL="https://twitter.com/"

def endpoint(TWTTR_URL=TWTTR_BASE_URL):
    top = requests.get(TWTTR_URL)
    # print(top.text)
    mainjsurl  = re.search('https:\/\/abs\.twimg\.com\/responsive-web\/client-web([^\/]+|)\/main\.[^.]+\.js', top.text).group(0)
    # mainjs = re.search("abs\.twimg\.com\/responsive-web\/client-web([^\/]+)\/main\.[^.]+\.js", top.text).text
    # print(top.text.find("abs\.twim\.com\/responsive-web\/client-web([^\/]+)\/main\.[^.]+\.js"))
    # print(a.group(0))
    mainjs = requests.get(mainjsurl).text

    params = {}

    rs = re.finditer('{queryId:"([^"]+)",operationName:"([^"]+)",operationType:"([^"]+)"', mainjs)
    for r in rs:
        # tmp = json.loads(re.sub('([\'\"])?([a-z0-9A-Z_]+)([\'\"])?:' , r.group(0), '"2": ') + "}")
        params[r.group(2)] = r.group(1)

    return params


if __name__ == "__main__":
    print(endpoint())