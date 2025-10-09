from fundus import PublisherCollection, Crawler
from firebase_admin import credentials, firestore
import firebase_admin
from fundus.scraping.filter import regex_filter, inverse

# --- Load the user information from Firestore ---

# Authenticate to firestore
cred = credentials.Certificate("../loginCredentials.json")
firebase_admin.initialize_app(cred)

# Connect to the users database
db = firestore.client()
user_ref = db.collection('users')

# A list in which we will first relevant user information to extract personalised news and also store the news URL
user_news = []

for users in user_ref.get():
    user_dict = {}
    user_dict['Company'] = users.get('company_name')
    user_dict['Industry'] = users.get('company_industry')

    # Add this user dict to the list of all users
    user_news.append(user_dict)
    #print(users.to_dict())
    # continue

# --- Crawler setup ---

# Only find news from publishers based in UK
crawler = Crawler(PublisherCollection.uk)

def industry_filter(extracted):
    topics = extracted.get('topics')
    titles = extracted.get('title')
    if(user_news[0]['Industry'].casefold() in [topic.casefold() for topic in topics]):
        return False
    return True

def sustainability_filter(extracted):
    topics = extracted.get('topics', [])
    keywords = [
        "net zero", "carbon", "emissions", "ESG", "CDP", "ISSB", "TCSB", "ESG", "decarbonization"
        "greenhouse", "net zero", "renewable", "environmental", "regulation", "reporting", "circular economy"
    ]

    # Combine all topics into a single string
    normalized_topics = " ".join(topics).casefold()

    # Match if any keyword appears as a substring
    if any(keyword.casefold() in normalized_topics for keyword in keywords):
        return False
    
    return True


# print(user_news[0]['Industry'])

# for article in crawler.crawl(only_complete=sustainability_filter, max_articles=3, url_filter=inverse(regex_filter("sustainability"))):
#     print(article)

for article in crawler.crawl(max_articles=5, only_complete=sustainability_filter):
    print(article)
    print(article.topics)

## For each user - check their industry and find 3 news articles in that industry. Then store it in new collection news with a foreign key uid 