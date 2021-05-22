from flask import Flask, request,redirect
from flask_cors import CORS
from util import database,account,statistic
from ml.rgs import get_sdor
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



app = Flask(__name__)

# 解决跨域
CORS(app,supports_credential=True)

# 从数据库中加载数据
DATA = database.fetch_data()
# 全局变量
TOKEN = ''
SECRET_KEY = 'token'

# 响应格式
res = {
    'msg':'',
    'code':200,
}

# 生成token
def create_token(expires=3600):
    s = Serializer(SECRET_KEY,expires_in=expires)
    token = s.dumps({'username':account.USERNAME,'password':account.PASSWORD}).decode('ascii')
    return token

# 验证token
def verify_token(token):
    s = Serializer(SECRET_KEY)
    info = s.loads(token)
    print(info)
    if info['username'] == account.USERNAME and info['password'] == account.PASSWORD:
        return True
    else:
        return False


@app.before_request
def auth_request():
    if request.path == '/login' or request.method == 'OPTIONS' or request.path == '/not_login':
        print('该接口不需要进行验证')
        return None
    else:
        token = request.headers.get('token')
        if not token:
            print('验证不通过')
            return redirect("/not_login")
        if verify_token(token):
            print('验证通过')
            return None
        else:
            print('验证不通过')
            return redirect("/not_login")

@app.route('/not_login')
def not_login():
    res['msg'] = '未登录'
    res['code'] = 401
    return res

@app.route('/login',methods=['POST'])
def login():
    print('请求登录接口----')
    # 获取post请求中的json数据，同时转换为字典
    req_json = dict(request.get_json())
    print(req_json)
    usr = req_json['username']
    pwd = req_json['password']
    if account.USERNAME == usr and account.PASSWORD == pwd:
        TOKEN = create_token()
        res['msg'] = TOKEN
        res['code'] = 200
    else:
        res['msg'] = False
        res['code'] = 403
    return res

@app.route('/statistic')
def hello_world():
    print('请求探索性分析接口----')
    res['msg'] = statistic.statistic_info(DATA)
    res['code'] = 200
    return res

@app.route('/predict_SDOR',methods=['POST'])
def predict_SDOR():
    print('请求预测SDOR接口----')
    x = dict(request.get_json())
    # 处理接收到的数据，把它变成67维向量
    # mlp = joblib.load('./model/mlp.model')
    sdor = get_sdor(x)
    print(sdor)
    # print(mlp)
    res['msg'] = {
        'ope':x,
        'sdor':sdor[0]
    }
    res['code'] = 200
    return res

@app.route('/search',methods=['POST'])
def search():
    print('请求检索接口----')
    req_json = dict(request.get_json())
    print(req_json)
    filter_data = [item for item in DATA if
                   req_json['name'] in item['姓名'] and
                   req_json['departmentNow'][0:-1] in item['病区'] and
                   req_json['opeBefDesc'] in item['术前诊断'] and
                   req_json['opeDesc'] in item['实施手术']
                   ]
    res['msg'] = filter_data
    res['code'] = 200
    return res

@app.route('/word_cloud/<text_type>')
def word_cloud(text_type):
    ans = []
    data = []
    if text_type == 'opeDesc':
        data = [item['实施手术_分词'] for item in DATA ]
    if text_type == 'opeBefDesc':
        data = [item['术前诊断_分词'] for item in DATA]
    word_freq = {}
    for item in data:
        for word in item.split('|'):
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
    for word,count in word_freq.items():
        if count >= 2:
            ans.append({
                'name':word,
                'value':count
            })

    res['msg'] = ans
    res['code']= 200
    return res




if __name__ == '__main__':
    # 让同一个局域网的电脑都能访问Flask接口
    app.run(host='0.0.0.0', port=5000)


