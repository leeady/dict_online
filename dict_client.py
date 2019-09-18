"""
dict 客户端

功能: 发起请求,接收结果
"""

from socket import *
import sys
import getpass

# 服务器地址
ADDR = ('127.0.0.1',3235)
s = socket()
s.connect(ADDR)

# 注册功能
def do_register():
    while True:
        name = input("User:")
        pwd = getpass.getpass()
        pwd1 = getpass.getpass("Again:")
        if pwd != pwd1:
            print("两次密码不一致！")
            continue
        if (' ' in name) or (' ' in pwd):
            print("用户名或密码不能含有空格")
            continue

        msg = "R %s %s"%(name,pwd)
        s.send(msg.encode()) # 发送请求
        data = s.recv(128).decode() # 反馈
        if data == 'OK':
            print("注册成功")
            second_main(name)
        else:
            print("注册失败")
        return

#登录功能
def do_login():
    while True:
        name = input('User:')
        pwd = getpass.getpass()

        msg = 'L %s %s'%(name,pwd)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            print('登录成功')
            second_main(name)
        else:
            print('登录失败')
        return

#退出
def do_quit():
    s.send(b'E')
    s.close()
    sys.exit('已退出,谢谢使用')

#查单词
def do_query(name):
    while True:
        word = input('请输入查询的单词:')
        if word =='##':
            break
        msg = 'Q %s %s' % (name,word)
        s.send(msg.encode())
        data = s.recv(1024).decode()
        tmp = data.split(' ',1)
        if tmp[0] == 'OK':
            print(tmp[1])
        else:
            print('找不到该单词')

#历史记录
def do_history(name):
    msg = 'H '+name
    s.send(msg.encode())
    while True:
        data = s.recv(1024).decode()
        if data == '##':
            break
        print(data)

#二级目录
def second_main(name):
    while True:
        print("""
        ========== %s ============
          1.查单词  2.历史记录   3.注销
        ===============================
        """ % name)
        cmd = input('选项(1,2,3):')
        if cmd == '1':
            do_query(name)
        elif cmd == '2':
            do_history(name)
        elif cmd == '3':
            return
        else:
            print('输入有误,请重新输入！')


# 搭建网络
def main():
    while True:
        print("""
        ========== Welcome ============
          1.注册     2.登录     3.退出
        ===============================
        """)
        cmd = input("选项(1,2,3):")
        if cmd == '1':
            do_register()
        elif cmd == '2':
            do_login()
        elif cmd == '3':
            do_quit()
        else:
            print('输入有误,请重新输入！')


if __name__ == '__main__':
    main()








