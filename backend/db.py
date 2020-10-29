from private import mongo_details  # dict with user/psw/cluster/connection url
import motor.motor_asyncio

url = mongo_details['url'].format(*[mongo_details[i] for i in ['user', 'password', 'cluster']])
db_client = motor.motor_asyncio.AsyncIOMotorClient(url)

# should make sure the connection is closed by following:
# with pymongo.MongoClient(db_config['HOST']) as client:
#     db = client[ db_config['NAME']]
#     item = db["document"].find_one({'id':1})
#     print(item)