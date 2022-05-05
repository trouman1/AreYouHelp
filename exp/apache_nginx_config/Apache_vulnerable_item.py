import os

line = '—' * 100
path = '/opt/lampp/etc/httpd.conf'


# 检查是否禁止Apache显示目录结构
def Check_directory_structure():
    res = os.popen(f"cat {path} | grep Options | grep -v '#' | grep -v 'None'").read().strip()
    if 'Indexes' in res:
        print(f'你的服务器目录可以被访问\n请在配置文件httpd.conf中将所有Options关键字后的Indexes去掉\n{line}')
    print(f'Apache显示目录结构通过检验\n{line}')


# 检查是否禁用PUT、DELETE等危险的HTTP方法
def Check_http_method():
    dangerous_method = ['PATCH', 'TRACE', 'OPTIONS', 'CONNECT', 'DELETE', 'PUT', 'HEAD']
    res = os.popen(f"cat {path} | grep LimitExcept | grep -v '#'").read().strip()
    if len(res) == 0:
        print(
            f'你的服务器开启了危险的HTTP方法，请在配置文件httpd.conf中添加如下内容：\n<LimitExcept GET POST> Deny from all </LimitExcept>\n{line}')
        return
    for d in dangerous_method:
        if d in res:
            print(
                f'你的服务器开启了危险的HTTP方法，请在配置文件httpd.conf中添加如下内容：\n<LimitExcept GET POST> Deny from all </LimitExcept>\n{line}')
    print(f'危险的HTTP方法通过检验\n{line}')


# 检查是否配置错误日志
def Check_error_log():
    res = os.popen(f"cat {path} | grep ErrorLog | grep -v '#'").read().strip()
    if len(res) == 0:
        print(
            f'你的服务器未设置错误日志文件\n请在配置文件httpd.conf中设置错误日志文件路径，例如：\nErrorLog logs/error_log\n其中logs/error_log为相应的文件路径\n{line}')
        return
    print(f'错误日志通过检验\n{line}')


# 是否设置错误信息详细程度为notice
def Check_error_loglevel():
    res = os.popen(f"cat {path} | grep LogLevel | grep -v '#'").read().strip()
    if 'notice' not in res:
        print(f'你的服务器未设置错误日志等级\n请在httpd.conf中设置LogLevel字段如下：\nLogLevel notice\n{line}')
        return
    print(f'日志等级通过检验\n{line}')


# 检查是否配置访问日志
def Check_visit_log():
    res = os.popen(f"cat {path} | grep CustomLog | grep -v '#'").read().strip()
    if len(res) == 0:
        print(
            f'你的服务器未设置访问日志文件\n请在配置文件httpd.conf中设置访问日志文件路径，例如：\nCustomLog log/access_log \n其中log/access_log为相应的文件路径\n{line}')
        return
    print(f'访问日志通过检验\n{line}')


# 检查是否配置日志记录格式
def Check_log_format():
    res = os.popen(f"cat {path} | grep LogFormat | grep -v '#'").read().strip()
    if len(res) == 0:
        print('你的服务器未设置访问日志文件\n请在配置文件httpd.conf中添加LogFormat命令，例如：\n'
              'LogFormat "%h %l %u % t \"%r\" %>s %b \"%{Accept}i\"\"%{Referer}i\" \"%{User-Agent}i\""')
        print(line)
        return
    print(f'日志记录格式通过检验\n{line}')


# 检查是否设置错误页面重定向
def Check_error_redirect():
    res = os.popen(f"cat {path} | grep ErrorDocument | grep -v '#'").read().strip()
    if len(res) == 0:
        print(f'在httpd.conf中，配置400错误重定向页面，例如：\nErrorDocument 400 /custom400.html \n/custom400.html为要显示的400错误页面\n{line}')
        return
    print(f'错误页面重定向通过检验\n{line}')


if __name__ == '__main__':
    Check_directory_structure()
    Check_http_method()
    Check_error_log()
    Check_error_loglevel()
    Check_visit_log()
    Check_log_format()
    Check_error_redirect()
