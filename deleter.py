
import pymongo

# bfl id 62534c6e56114c0a8ba2002b

client = pymongo.MongoClient(
    "mongodb+srv://marco:4Nr1fD8mAOSypUur@cluster1.fzsll.mongodb.net/bf_historical?retryWrites=true&w=majority")
db = client.bf_historical


d = db.tradeNew.delete_many({ "trade.info.strategyId": "62534c6e56114c0a8ba2002b"})

print(d.deleted_count, " documents deleted !!")


#{ "trade.info.strategyId": "62534c6e56114c0a8ba2002b"}
#{ "updated" : { "$gte" : 1660656712000 } }