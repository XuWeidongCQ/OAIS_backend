
import pymongo

def fetch_data():
    HOST = 'localhost'
    PORT = 27017
    DATABASE = 'graduate'
    COL = 'OAIS_data'
    db_client = pymongo.MongoClient(HOST,PORT)
    db_col = db_client[DATABASE][COL]
    data = db_col.find({},{"_id":0})
    data = [item for item in data ]
    print('获取数据{}条'.format(len(data)))
    # 关闭连接
    db_client.close()
    return data