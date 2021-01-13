#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# FileName ：test1.py
# Author   ：zheng xingtao
# Date     ：2021/1/13 14:47
class BMinx:
    def log(self):
        print("B log")

    def display(self):
        print("B display")  # A --> B --> display()
        super(B, self).display2()  # self指的是实例化的A() ==> A的self指向的display2() --> C.display2()
        self.log()  # self --> A.log()


class C:
    def display2(self):
        print("C display")


class A(BMinx, C):  # TODO：混入
    def log(self):
        print("A log")
        # self.log()
        super(A, self).log()  # super(A, self)到A类的父类中查找log() --> B.log(), 如果B里面没有再到A里面去找

    def display2(self):
        print("AA")


test = A()
test.display()

"""
MRO顺序：A B E G H L

当我们使用 self 调用的时候，是从A开始，一直到L结束
但是使用 super 的时候，是从B开始，一直到最后

Mixin ==> 利用多继承实现了一种组合模式
多继承是Python的特性，而Mixin是利用了这种特性实现了组合模式
"""
