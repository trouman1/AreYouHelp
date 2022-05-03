# -*- coding: UTF-8 -*-
import os
print("当前系统可能存在的漏洞有：")
version = os.popen("uname -r|awk -F . '{print $1\".\"$2}'").read().strip()

with open("/root/tools/AreYouHelp/exp/vuln_check/ali_cve1.txt",'r',encoding='GBK') as f:
    contents = f.readlines()

for content in contents:
    if f"Linux Kernel {version}" in content:
        print(content)

print("注：此结果仅供参考，更多内容请自行搜索")