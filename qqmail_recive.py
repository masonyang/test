#!/usr/bin/env python
#coding:utf-8
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from datetime import datetime
email = '530369682@qq.com'
passwd = 'njksqixizpdycajf'
pop_server = 'pop.qq.com'

def get_email():
    server = poplib.POP3_SSL(pop_server,'995')
    # 可以打开或关闭调试信息:
    # server.set_debuglevel(1)
    # 可选:打印POP3服务器的欢迎文字:
    print(server.getwelcome().decode('utf-8'))
    server.user(email)
    server.pass_(passwd)
    #邮件数量和占有空间
    print('Messages: %s. Size: %s' % server.stat())
    #list()返回所有邮件编号
    resp_one,mails,octets_one = server.list()
    #查看返回列表
    #print(mails)
    #获取最新的一封邮件，索引号为1开始
    index = len(mails)
    resp_two, lines, octets_two = server.retr(index)
    #lines存储邮件原始文本每行并进行解析
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_content)
    #可以根据邮件索引从服务器删除邮件
    #server.dele(index)
    #关闭邮件
    server.quit()
    print_info(msg)

#编码设置
def guess_charset(my_msg):
    charset = my_msg.get_charset()
    if charset is None:
        content_type = my_msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
        return charset
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
        return value

# indent用于缩进显示，递归打印
def print_info(my_msg, indent=0):
    if indent == 0:
        for header in ['From', 'To','Subject']:
            value = my_msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % (' ' * indent, header, value))
    if my_msg.is_multipart():
        parts = my_msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % (' ' * indent, n))
            print('%s-----------------------------------' % ' ' * indent)
            print_info(part, indent + 1)
    else:
        content_type = my_msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = my_msg.get_payload(decode=True)
            charset = guess_charset(my_msg)

            if charset:
                content = content.decode('utf-8')
                print('%sText: %s' % (' ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % (' ' * indent, content_type))
if __name__ == '__main__':
    get_email()



# user(username) 发送用户名到服务器，等待服务器返回信息
# pass_(password) 密码
# stat() 返回邮箱的状态,返回2元祖(消息的数量,消息的总字节)
# list([msgnum])  stat()的扩展，返回一个3元祖(返回信息, 消息列表, 消息的大小)，如果指定msgnum，就只返回指定消息的数据
# retr(msgnum)     获取详细msgnum，设置为已读，返回3元组(返回信息, 消息msgnum的所以内容, 消息的字节数)，如果指定msgnum，就只返回指定消息的数据
# dele(msgnum)     将指定消息标记为删除
# quit()  登出，保存修改，解锁邮箱，结束连接，退出


