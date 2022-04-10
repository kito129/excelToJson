import os, json
from datetime import datetime, timedelta
from re import X
import pymongo

inputPath = "VALID/01_lay the fav/04_04_2022_16_57_17"
outputPath = "uploadLog"

def log(*args, end='\n'):
    global logger
    print(*args, end=end)
    logger.write("".join(args)+end)

def checkMarketPresentByName(name):
    return db.tradeNew.find({"trade.info.marketInfo.marketName": name})

def uploadInDb(trade):
    db.tradeNew.insert_one(trade)
    log(f'\t[>] Upload: {marketName}')

def checkByHash(found, trade):
    find = False
    for x in found:
        del x['_id']
        if x == trade:
            find = True
            break

    if find:
        log(f'\t\t[x] Skip: {marketName}')
    else:
        uploadInDb(trade)
    
time = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
logger = open(os.path.join(outputPath, f'{time}_logs.txt'), 'w', encoding='utf-8')
client = pymongo.MongoClient(
    "mongodb+srv://marco:4Nr1fD8mAOSypUur@cluster1.fzsll.mongodb.net/bf_historical?retryWrites=true&w=majority")
db = client.bf_historical
    

for dirpath, dirnames, filenames in os.walk("./VALID"):
    for filename in [f for f in filenames if f.endswith(".json")]:
        try:

            name = os.path.join(dirpath, filename)
            log(f'[-] File: {name}')
            file = open(os.path.join(dirpath, filename))
            data = json.load(file)
            date = data['trade']['info']['date']
            marketName = data['trade']['info']['marketInfo']['marketName']
            find = checkMarketPresentByName(marketName)
            if find == None:
                uploadInDb(data)
            else:
                checkByHash(find, data)
        except Exception as e:
            log(f"[-] Unable to read Book: {os.path.basename(file)}, Error: {e}")
            continue


