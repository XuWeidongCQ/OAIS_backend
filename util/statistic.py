

def is_in(key, value):
    val = float(value)
    if '-' in key:
        min = float(key.split('-')[0])
        max = float(key.split('-')[1])
        if val >= min and val < max:
            return True
        else:
            return False
    else:
        min = float(key[2:])
        return val >= min


# 统计信息
def statistic_info(data):
    ans = {
        'patient_distribution' :{},
        'weight_distribution' :{
            '0-25' :{'男':0,'女':0},
            '25-50' :{'男':0,'女':0},
            '50-75' :{'男':0,'女':0},
            '75-100' :{'男':0,'女':0},
            '100-125' :{'男':0,'女':0},
            '125-150' :{'男':0,'女':0},
            '>=150' :{'男':0,'女':0}
        },
        'height_distribution' :{
            '100-125' :{'男':0,'女':0},
            '125-150' :{'男':0,'女':0},
            '150-175' :{'男':0,'女':0},
            '>=175' :{'男':0,'女':0}
        },
        'age_distribution' :{
            '0-20' :{'男':0,'女':0},
            '20-40' :{'男':0,'女':0},
            '40-60' :{'男':0,'女':0},
            '60-80' :{'男':0,'女':0},
            '>=80' :{'男':0,'女':0}
        },
        'sex_count':{
            '男':0,
            '女':0
        },
        'total_patient':0,
        'total_department':13
    }
    for item in data:
        department = item['病区'][0:-2]
        age = item['年龄']
        weight = item['体重']
        height = item['身高']
        sex = item['性别']
        ans['total_patient'] += 1
        # 统计男和女的患者数目
        if sex == '男':
            ans['sex_count']['男'] += 1
        else:
            ans['sex_count']['女'] += 1
        # 统计每个科室的患者分布
        if department in ans['patient_distribution']:
            if sex == '男':
                ans['patient_distribution'][department]['男'] += 1
            else:
                ans['patient_distribution'][department]['女'] += 1
        else:
            ans['patient_distribution'][department] = {
                '男':0,
                '女':0
            }
        # 统计每个患者年龄分布
        for key in ans['age_distribution'].keys():
            if is_in(key,age):
                if sex == '男':
                    ans['age_distribution'][key]['男'] += 1
                else:
                    ans['age_distribution'][key]['女'] += 1
                break
        # 统计每个科室的身高分布
        for key in ans['height_distribution'].keys():
            if is_in(key,height):
                if sex == '男':
                    ans['height_distribution'][key]['男'] += 1
                else:
                    ans['height_distribution'][key]['女'] += 1
                break
        # 统计每个科室的体重分布
        for key in ans['weight_distribution'].keys():
            if is_in(key,weight):
                if sex == '男':
                    ans['weight_distribution'][key]['男'] += 1
                else:
                    ans['weight_distribution'][key]['女'] += 1
                break
    return ans