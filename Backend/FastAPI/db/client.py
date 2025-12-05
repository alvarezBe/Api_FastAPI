from pymongo import MongoClient

#Base de datos local
#db_client = MongoClient().local

#Base de datos en la nube (remota)
db_client = MongoClient("mongodb+srv://test:test@cluster0.8dwzjee.mongodb.net/?appName=Cluster0").test
