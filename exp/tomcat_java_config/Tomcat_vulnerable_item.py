import os

line = '—' * 100
path = '/opt/apache-tomcat-8.0.53/conf/'


# 是否禁止自动部署
def Check_auto_deploy():
    res = os.popen(f"cat {path}server.xml | grep autoDeploy | grep -v '\-\-'").read().strip().split()
    for r in res:
        if 'autoDeploy' in r:
            if 'true' in r:
                print(f'你的服务器未禁止自动部署\n'
                      f'请打开conf/server.xml配置文件\n'
                      f'将host节点的autoDeploy属性设置为“false”\n'
                      f'{line}')
                return
            print(f'自动部署通过检测\n'
                  f'{line}')


# 是否禁止显示异常调试信息
def Check_abnormal_debug():
    res = os.popen(f"cat {path}web.xml | grep error-page | grep -v '\-\-'").read().strip()
    if len(res) == 0:
        print(f'你的服务器未禁止显示异常调试信息\n'
              f'请打开conf/web.xml配置文件添加子节点：\n'
              f'<error-page><exception-type>java.lang.Throwable</exception-type><location>/error.jsp</location></error-page>\n'
              f'在webapps目录下创建error.jsp，定义自定义错误信息\n'
              f'{line}')
        return
    print(f'异常调试信息通过检测\n'
          f'{line}')


# 是否开启日志记录
def Check_Logging():
    res = os.popen(
        f"cat {path}server.xml | grep org.apache.catalina.valves.AccessLogValve | grep -v '\-\-'").read().strip()
    if len(res) == 0:
        print(f'你的服务器未开启日志记录\n'
              f'请打开conf/server.xml配置文件\n'
              f'取消Host节点下Valve节点的注释(如没有则添加)\n'
              f'<Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs" prefix="localhost_access_log" suffix=".txt" pattern="%h %l %u %t &quot;%r&quot; %s %b" /> \n'
              f'{line}')
        return
    print(f'日志记录通过检测\n'
          f'{line}')


# 是否显示目录文件列表
def Check_directory_structure():
    res = os.popen(f"cat {path}web.xml | grep -A 1 listings | grep -v '\-\-'").read().strip()
    if 'true' in res:
        print(f'你的服务器显示了目录文件列表\n'
              f'请打开conf/web.xml配置文件将listings的值设置为false\n'
              f'{line}')
        return
    print(f'目录文件列表通过检测\n'
          f'{line}')


if __name__ == '__main__':
    Check_auto_deploy()
    Check_abnormal_debug()
    Check_Logging()
    Check_directory_structure()
