#!/usr/bin/env python
# coding=utf-8
import os
# from fabric.colors import *
from os.path import join, isfile


def find_file(filepath, filename, find_depth=1, ignore_path=['.git', 'node_modules']):
    """查找文件"""
    # print blue("当前查找目录：{}，递归层级：{}".format(filepath, find_depth))
    # 递归深度控制
    find_depth -= 1
    for file_ in os.listdir(filepath):
        # print cyan("file: {}".format(file_))
        if isfile(join(filepath, file_)):
            # print "当前文件：{}".format(file_)
            if file_ == filename:
                return True, filepath
        elif find_depth <= 0:  # 递归深度控制, 为0时退出
            # print yellow("超出递归深度，忽略!")
            continue
        elif file_ in ignore_path:  # 忽略指定目录
            # print yellow("此目录在忽略列表中，跳过！")
            continue
        else:
            result, abs_path = find_file(filepath=join(filepath, file_),
                                              filename=filename,
                                              find_depth=find_depth)
            if result:
                print("找到{}文件，所在路径{}".format(filename, abs_path))
                return result, abs_path
    return False, filepath

result, filepath = find_file(filepath="/root/tools/AreYouHelp/exp", filename="gulpfile.js", find_depth=3)
