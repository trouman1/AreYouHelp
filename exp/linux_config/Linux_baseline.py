import os,re,platform

print(
    '''
##########################################################################
#                                                                        #
#                               主机安全检测                              #
#                                                                        #
##########################################################################
    '''
)

# 本机信息
hostname = os.popen('uname -n').read()
version = os.popen("cat /etc/redhat-release | awk '{print $4$5}'").read()
kernel = os.popen("uname -r").read()
ipaddr = os.popen("ip addr | grep inet | grep -v \"inet6\" | grep -v \"127.0.0.1\" | awk '{ print $2; }' | tr '\n' '\t' ").readline()
date = os.popen("date").read()
memory = os.popen("free -h |grep \"Mem:\" | awk '{print $2}'").read()
freememory = os.popen("free -h |grep \"Mem:\" | awk '{print $4}'").read()
freememory1 = re.findall("(.*?)M",freememory)
usedmemory = os.popen("free -h |grep \"Mem:\" | awk '{print $3}'").read()
uptime = os.popen("uptime | awk '{print $2," "$3," "$4" "}'").read()
mostpro = os.popen("ps auxf |sort -nr -k 3 |head -1").read()
mostmem = os.popen("ps auxf |sort -nr -k 4 |head -1").read()

print("     >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>系统基本信息<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
print("     主机："+hostname)
print("     操作系统："+platform.system())
print("     版本："+version)
print("     内核："+kernel)
print("     ip地址："+ipaddr)
print("     系统时间："+date)

print("     >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>资源使用情况<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
print("     总内存："+memory)
print("     已用内存："+usedmemory)
print("     可用内存："+freememory)
if int(freememory1[0]) < 200:
    print("     内存使用量过多")
print("     运行时间："+uptime)
print("     消耗CPU最多的进程：\n"+mostpro)
print("     消耗内存最多的进程：\n"+mostmem)

# 查看环境变量
print("=====================环境变量========================================")
env = os.popen("env").read()
print(      "环境变量:\n"+env)

print("======================开机自启动的服务=======================================")
enable = os.popen("systemctl list-unit-files | grep enabled").read()
print(enable)

print("=======================查看活跃用户======================================")
# 展示登录到当前系统的用户。
print(os.popen("who | awk '{print $1}'").read())

print("========================查看所有用户=====================================")
print(os.popen("cat /etc/passwd | grep -v nologin|grep -v halt|grep -v shutdown|awk -F\":\" '{ print $1\"|\"$3\"|\"$4 }'").read())

print("=========================当前用户的计划任务====================================")
print(os.popen("crontab -l").read())



print("========================特权用户=====================================")
print("系统特权用户："+os.popen("awk -F: '$3==0 {print $1}' /etc/passwd").read())

print("========================空口令账户=====================================")
nullpass = os.popen("awk -F: 'length($2)==0 {print $1}' /etc/shadow").read()
if nullpass == 0:
    print("无")
else:
    print(nullpass)

print("===================显示用户最近登录信息=========================================")
print(os.popen('last | head -n 30').read())

print("=================用户错误登录============================================")
failcount = os.popen("more /var/log/secure | grep  \"Failed\"").read()
if failcount == 0:
    print("无错误登入记录")
else:
    ip = os.popen('more /var/log/secure|awk \'/Failed/{print $(NF-3)}\'|sort|uniq -c|awk \'{print "登入失败的IP和尝试次数: "$2"="$1"次";}\'').read()
    print(ip)


print("密码过期设置：")
mima = os.popen("chage -l root").read()
print(mima)
if "从不" in mima:
    print("建议设置密码失效时间，定期修改密码")
    print("在 /etc/login.defs中修改")

print("====================syslog服务=========================================")
syslog = os.popen("service rsyslog status | grep \" active (running\"").read()
if "active (running" in syslog :
    print("syslog服务已开启")
else:
    print("syslog服务未开启")

print("====================重要文件修改时间=========================================")
print(os.popen("ls -ltr /bin/ls /bin/login /etc/passwd  /bin/ps /etc/shadow|awk '{print \">>>文件名：\"$9\"  \"\"最后修改时间：\"$6\" \"$7\" \"$8}'").read())

print("=====================检查重要日志文件是否存在========================================")
logs0 = os.popen("cat /var/log/secure").read()
log1 = os.popen("cat /var/log/messages").read()
log2 = os.popen("cat /var/log/cron").read()
log3 = os.popen("cat /var/log/boot.log").read()
log4 = os.popen("cat /var/log/dmesg").read()
if "没有那个文件或目录" in logs0:
    print("/var/log/secure日志文件不存在")
elif "没有那个文件或目录" in log1:
    print("/var/log/messages日志文件不存在")
elif "没有那个文件或目录" in log2:
    print("/var/log/cron日志文件不存在")
elif "没有那个文件或目录" in log3:
    print("/var/log/boot.log日志文件不存在")
elif "没有那个文件或目录" in log4:
    print("/var/log/dmesg日志文件不存在")
else:
    print("/var/log/secure,/var/log/messages,/var/log/cron,/var/log/boot.log,/var/log/dmes存在")


print("=================防火墙============================================")
status = os.popen("systemctl status firewalld").read()
if "active (running)" in status:
    print("防火墙已经开启")
else:
    print("防火墙未开启")

print("===================检查/usr/bin/目录下可执行文件==========================================")
print(os.popen("find /usr/bin/ -type f -perm -04000 -o -perm -02000").read())
print("把不必要的s属性去掉;")

print("====================检测文件权限=========================================")
print("/etc/passwd权限")
print(os.popen("stat -c %a /etc/passwd").read())
print("/etc/shadow权限")
print(os.popen("stat -c %a /etc/shadow").read())
print("/etc/group权限")
print(os.popen("stat -c %a /etc/group").read())
print("/etc/profile权限")
print(os.popen("stat -c %a /etc/profile").read())

print("=====================检测补丁安装情况========================================")
rqff_c = os.popen("rpm -qa|grep patch").read()
print("补丁情况："+rqff_c)

print("======================查看ssh登录地址限制=======================================")
denyid = os.popen("cat /etc/hosts.deny").read()
if "ALL:ALL" in denyid:
    print("已配置登录地址限制策略")
else:
    print("未配置登录地址限制策略")





