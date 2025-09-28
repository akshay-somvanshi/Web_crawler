from fundus import PublisherCollection, Crawler
from firebase_admin import credentials, firestore
import firebase_admin
import os

# --- Firestore setup ---

# Locate the JSON certificate file
certificate_path = os.environ.get("certificate_path")

# Authenticate to firestore
cred = credentials.Certificate(certificate_path)
firebase_admin.initialize_app(cred)

db = firestore.client()
user_ref = db.collection('users').document('CORZZX0MxTQtGyAD7PSCI1HLp3y2')

users = user_ref.get()
print(users._data['uid'])

# --- Crawler setup ---

crawler = Crawler(PublisherCollection.uk)

# for article in crawler.crawl(max_articles=4):
#     print(article)