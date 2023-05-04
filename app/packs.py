import time
import base64
import json
from urllib.parse import urlparse, parse_qs, unquote, urlencode, urlunparse, quote


def formattime(timestamp):
    time_struct = time.localtime(timestamp)
    year = time_struct.tm_year
    month = time_struct.tm_mon
    day = time_struct.tm_mday
    hour = time_struct.tm_hour
    minute = time_struct.tm_min
    second = time_struct.tm_sec
    return f'{year}年{month}月{day}日 {hour}时{minute}分{second}秒'

def modifyps(node):
    temp = node.split('://')
    res=''
    if temp[0]=='trojan':
        try:
            res=handle_normal(node)
        except:
            res=handle_trojan(node)
    elif temp[0] == 'ss':
        try:
            res=handle_normal(node)
        except:
            res=handle_ss(node)
    else:
        try:
            res=handle_normal(node)
        except BaseException as e:
            print(f'Error: {e}')
    return res

def text_processor(text):
    raw = text.strip('\n')
    a = raw.split('\n')
    nodes = ''
    counts = len(a)
    for i in range(counts):
        # print(f'doing {i}:')
        nodes += modifyps(a[i])+'\n'

    nodes = nodes.strip('\n')

    # 字符串转字节串
    text_bytes = nodes.encode('utf-8')

    # 对字节串进行base64编码
    encoded_bytes = base64.b64encode(text_bytes)

    # 将编码后的字节串转换为字符串
    encoded_text = encoded_bytes.decode('utf-8')
    return encoded_text, counts


def handle_normal(node):
    temp = node.split('://')
    
    de = base64.b64decode(temp[-1].encode('utf-8'))
    res = json.loads(de.decode('utf-8'))
    
    
    # res['ps'] = res['ps'].replace('(Youtube:不良林)', '')
    res['ps'] = res['ps'].split('(')[0]
    
    text_bytes = str(res).encode('utf-8')
    encoded_bytes = base64.b64encode(text_bytes)
    encoded_text = encoded_bytes.decode('utf-8')

    out=temp[0]+'://'+encoded_text
    return out
        
def handle_trojan(node):
    # URL地址
    #url = 'trojan://sfgdg225v5ddfs@cc.tross...'

    # 使用urlparse解析URL
    parsed_url = urlparse(node)

    # 提取URL中的各个组成部分
    scheme = parsed_url.scheme  # 协议
    username = parsed_url.username  # 用户名
    hostname = parsed_url.hostname  # 主机名
    port = parsed_url.port  # 端口号
    query = parsed_url.query  # 查询参数
    fragment = parsed_url.fragment  # 锚点

    # 使用parse_qs解析查询参数
    parsed_query = parse_qs(query)

    # 使用unquote解码锚点
    decoded_fragment = unquote(fragment)
    
    # 修改解码后的锚点，去掉"(Youtube:不良林)"
    new_decoded_fragment = decoded_fragment.split('(')[0]

    # 使用quote重新编码锚点
    new_encoded_fragment = quote(new_decoded_fragment)
    
    # 使用urlunparse重新构造URL
    new_url = urlunparse((scheme, f'{username}@{hostname}:{port}', '', '', query, new_encoded_fragment))
    return new_url

def handle_ss(node):
    # 使用urlparse解析URL
    parsed_url = urlparse(node)

    # 提取URL中的各个组成部分
    scheme = parsed_url.scheme  # 协议
    username = parsed_url.username  # 用户名（Base64编码的加密方法和密码）
    hostname = parsed_url.hostname  # 服务器地址
    port = parsed_url.port  # 服务器端口
    query = parsed_url.query  # 查询参数（插件信息）
    fragment = parsed_url.fragment  # 锚点（备注信息）

    # 使用base64解码加密方法和密码
    decoded_username = base64.urlsafe_b64decode(username + '==').decode('utf-8')
    method_password = decoded_username.split(':')

    # 提取加密方法和密码
    method = method_password[0]
    password = method_password[1]

    # 使用parse_qs解析插件信息
    parsed_query = parse_qs(query)

    # 使用unquote解码备注信息
    decoded_fragment = unquote(fragment)
    
    # 修改解码后的锚点，去掉"(Youtube:不良林)"
    new_decoded_fragment = decoded_fragment.split('(')[0]

    # 使用quote重新编码锚点
    new_encoded_fragment = quote(new_decoded_fragment)
    
    # 使用urlunparse重新构造URL
    new_url = urlunparse((scheme, f'{username}@{hostname}:{port}', '', '', query, new_encoded_fragment))
    return new_url
    
def write_to_file(text):
    with open('nodes.txt', 'w') as f:
        f.write(text)