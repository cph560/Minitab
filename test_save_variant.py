import pandas as pd
import numpy as np
import pickle
import base64

# 定义要导出的数据
def pack():
    data1 = pd.DataFrame(np.random.rand(3, 5))
    type1 = "t"
    config1 = {'name': 't', 'size': 'j', 'stack': 'yes'}

    data2 = pd.DataFrame(np.random.rand(3, 5))
    type2 = "t"
    config2 = {'name': 't', 'size': 'j', 'stack': 'yes'}
    existing_data_list = []

    # 将数据打包成一个字典
    data_dict1 = {
        'data1': data1,
        'type1': type1,
        'config1': config1
    }
    data_dict2 = {
        'data2': data2,
        'type2': type2,
        'config2': config2
    }
    data_dict={'data_dict1':data_dict1,'data_dict2':data_dict2}
    # 使用pickle序列化数据字典
    serialized_data = pickle.dumps(data_dict)

    # 将字节流编码为base64字符串，以便于存储和传输
    data_string = base64.b64encode(serialized_data).decode('utf-8')

    print(data_string)
    return data_string
def import_data(string):
    byte_data = base64.b64decode(string)
    data_dict=pickle.loads(byte_data)
    return data_dict

def save():
    packed_string = pack()
    # 将生成的字符串保存到txt文件
    with open('data.txt', 'w') as file:
        file.write(packed_string)

def load():
    with open('data.txt', 'r') as file:
        packed_string = file.read()
    data_dict=import_data(packed_string)
    return data_dict

save()
data=load()
pass