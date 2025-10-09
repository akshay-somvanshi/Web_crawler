import urllib.request

url = "https://sustainability-news.net/tag/news/"

request = urllib.request.Request(url, headers={'User-Agent': 'FundusBot'})

with urllib.request.urlopen(request) as response:
    content = response.read()

print("Crawlable!")