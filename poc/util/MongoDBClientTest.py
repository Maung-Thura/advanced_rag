import pymongo

client = pymongo.MongoClient("mongodb://advancedragteam1:86k4DoxBAOsx@pvj8334-msai490-documentdb-group-shared.cluster-cfrmjneqc9ua.us-east-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=true")
db = client.advancedrag_db
collection = db.advancedrag_db_embeddings

print(collection)