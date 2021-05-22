import numpy as np
import joblib
import jieba
from gensim.models import Word2Vec


def sex_one_hot(sex):
    if sex == '男':
        return [0,1]
    else:
        return [1,0]


def department_one_hot(department):
    code = {
        '口腔科':0,
        '妇产科':1,
        '心血管科':2,
        '整形外科':3,
        '普通外科':4,
        '普通胸外科':5,
        '泌尿外科':6,
        '眼科':7,
        '神经内科':8,
        '神经外科':9,
        '耳鼻咽喉科':10,
        '肝胆外科':11,
        '骨科':12,
    }
    ans = [0] * 13
    ans[code[department]] = 1
    return ans

def load_model():
    # tf_idf = np.load('../model/tf_idf.npy',allow_pickle=True)
    # mlp = joblib.load('../model/mlp.model')
    mlp = joblib.load('./model/mlp.model')
    age_bmi_scaler = joblib.load('./model/age_bmi_scaler.joblib')
    text_scaler = joblib.load('./model/text_scaler.joblib')
    wv_model = Word2Vec.load('./model/wv_model_CHI.model')
    return mlp,age_bmi_scaler,text_scaler,wv_model

def word_cut(s):
    # 这里可以加医疗文本的处理流程
    return [item for item in jieba.cut(s,use_paddle=False)]

def get_sdor(data):
    try:
        mlp, age_bmi_scaler, text_scaler, wv_model = load_model()
        ans =[]
        ans.append(data['age'])
        ans.append(float(data['weight']) / float(data['height']) * 100)
        ans = age_bmi_scaler.transform([ans]).tolist()[0]
        ans.extend(sex_one_hot(data['sex']))
        ans.extend(department_one_hot(data['departmentNow']))
        text = []
        text.extend(word_cut(data['opeBefDesc']))
        text.extend(word_cut(data['opeDesc']))
        text_vec = np.array([0.0] * 50)
        for w in text:
            if w in wv_model.wv:
                text_vec += wv_model.wv[w]
        text_vec = text_scaler.transform(text_vec.reshape(1,-1))
        # print(text_vec)
        # print(type(text_vec))

        ans.extend(text_vec.tolist()[0])
        # print(len(ans))
        # print(mlp.predict([ans]))
    except Exception as e:
        print("预测sdor出错:")
        print(e)
        return [-1]
    return mlp.predict([ans])