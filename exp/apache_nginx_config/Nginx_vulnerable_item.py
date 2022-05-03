import os

line = '—' * 100
path = '/usr/local/nginx/conf/nginx.conf'


# 检测Nginx后端服务指定的Header隐藏状态服务配置
def Check_header_hidden_state():
    res = os.popen(f"cat {path} | grep proxy_hide_header | grep -v '#'").read().strip()
    if len(res) == 0:
        print(f'你的服务器未隐藏Nginx后端服务指定Header的状态\n'
              f'请打开conf/nginx.conf配置文件,在http下增加或修改为\n'
              f'proxy_hide_header X-Powered-By;\n'
              f'proxy_hide_header Server;\n'
              f'{line}')
        return
    print(f'Header隐藏状态通过检测\n'
          f'{line}')


# 针对Nginx SSL协议进行安全加固服务配置
def Check_SSL_protocol():
    res = os.popen(f"cat {path} | grep ssl_protocols | grep -v '#'").read().strip()
    if len(res) == 0:
        print(f'你的服务器未对SSL协议的加密策略进行加固\n'
              f'请打开conf/nginx.conf配置文件,在http下增加或修改为\n'
              f'ssl_protocols TLSv1.2;\n'
              f'{line}')
        return
    print(f'SSL协议的加密策略通过检测\n'
          f'{line}')


# Nginx的WEB访问日志记录状态
def Check_access_log():
    res = os.popen(f"cat {path} | grep access_log | grep -v '#'").read().strip()
    if len(res) == 0:
        print(f'你的服务器未对每个核心站点启用access_log指令\n'
              f'请打开conf/nginx.conf配置文件,在http下增加或修改为\n'
              f'access_log logs/host.access.log main;\n'
              f'{line}')
        return
    print(f'WEB访问日志记录状态通过检测\n'
          f'{line}')


# 隐藏Nginx服务的Banner服务配置
def Check_banner_state():
    res = os.popen(f"cat {path} | grep server_tokens | grep -v '#'").read().strip()
    if len(res) == 0:
        print(f'你的服务器未隐藏Nginx服务Banner的状态\n'
              f'请打开conf/nginx.conf配置文件,在server下增加或修改为\n'
              f'server_tokens off;\n'
              f'{line}')
        return
    print(f'Banner服务配置通过检测\n'
          f'{line}')


if __name__ == '__main__':
    Check_header_hidden_state()
    Check_SSL_protocol()
    Check_access_log()
    Check_banner_state()
