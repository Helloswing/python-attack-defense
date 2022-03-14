import base64, os,time

# 解密
from collections import Counter


def decrypt(filepath):
    with open(filepath, mode='r') as file:
        content = file.read()
    dest = ''
    for c in content:
        dest += chr(ord(c)-5)
    newfile = filepath.replace('.enc', '')
    with open(newfile, mode='wb') as file:
        file.write(base64.b64decode(dest))
    # 删除加密文件
    os.remove(filepath)
#启动防火墙防止ddos
# 第一步：先采集跟DOS攻击关联度较高的数据
# 1、采集CPU的平均负载
def get_cpu_load():
    # 利用Python处理字符串的方式
    uptime = os.popen('uptime').read()
    uptime = uptime.replace(": ", ",")
    cpu_load = float(uptime.split(",")[-3])
    # 利用awk命令来提取CPU负载
    cpu_load = os.popen("uptime | awk -F ': ' '{print $2}' | awk -F ',' '{print $1}'").read()
    cpu_load = float(cpu_load)
    return cpu_load
# 2、采集netstat -ant的连接数量
def get_conn_count():
    netstat = os.popen('netstat -ant | wc -l').read()
    return int(netstat)
# 3、采集队列长度
def get_queue_size():
    # ss -lnt | grep :80 | awk '{print $3}'
    sslnt = os.popen("ss -lnt | grep :80").read()
    recvq = int(sslnt.split()[1])
    sendq = int(sslnt.split()[2])
    return recvq, sendq
def get_most_ip():
    result = os.popen('netstat -ant | grep :80').read()
    line_list = result.split('\n')
    ip_list = []
    for line in line_list:
        try:
            temp_list = line.split()
            ip = temp_list[4].split(':')[0]
            ip_list.append(ip)
        except:
            pass
    dict = Counter(ip_list)
    most_ip = dict.most_common(1)
    return most_ip[0][0]
def firewall_ip(ip):
    result = os.popen(f"firewall-cmd --add-rich-rule='rule family=ipv4 source address={ip} port port=80 protocol=tcp reject'").read()
    if 'success' in result:
        print(f"已经成功将可疑攻击源 {ip} 进行封锁，流量将不再进入.")
    else:
        print(f"对可疑攻击源 {ip} 进行封锁时失败，转为人工处理.")

#界面
def title():
    print("+*****************")
    print("+作者:suweidong")
    print("+当前日期:2022-3-13")
    print("使用方法：按照提示输入")
    print("+*****************")

def defence():
    choose = int(input("选择服务：\n1、解密文件\n2、防dos攻击\n3.返回界面\n4.退出\n请输入："))
    if choose==1:
        file_pa = input("please input the file path")
        decrypt(file_pa)
        # 启动防火墙防dos攻击
    elif choose==2:
        while True:
            cpu = get_cpu_load()
            conn = get_conn_count()
            recvq, sendq = get_queue_size()
            most_ip = get_most_ip()
            print(f"CPU-Load: {cpu}, TCP Conn: {conn}, TCP Queue: {recvq, sendq}")
            # 对采集到的数据进行判断，并进行预警提醒
            if cpu > 50 and conn > 500 and recvq > sendq - 10:
                print(f"当前系统TCP连接负载和CPU使用率过高，存在DOS攻击的可能性，可疑IP地址为：{most_ip}.")
                firewall_ip(most_ip)
            time.sleep(5)
    elif choose == 3:
        defence()
    else:
        exit()


if __name__ == '__main__':
    title()
    defence()
