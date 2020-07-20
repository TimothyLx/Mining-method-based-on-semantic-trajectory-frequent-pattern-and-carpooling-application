# -*- coding:utf-8 -*-
# @FileName:RGA.py
# @Time    :2020/6/176:17
# @Author  :LX
from numpy import *
import time
import pickle
import sys


def apriori(data_set, min_sup=0.5):
    c_1 = create_c1(data_set)
    d = list(map(set, data_set))
    l_1, support_data = scan_d(d, c_1, min_sup)
    l = [l_1]
    k = 2
    while (len(l[k - 2]) > 0):
        c_k = gen_apriori(l[k - 2], k)
        # print("候选项集是：", c_k)
        l_k, sup_k = scan_d(d, c_k, min_sup)
        # print("筛频繁项集是", l_k)
        support_data.update(sup_k)
        l.append(l_k)
        k += 1
    return l, support_data

def create_c1(data_set):
    c1 = []
    for trans in data_set:
        for i in trans:
            if not [i] in c1:
                c1.append([i])
    c1.sort()
    return list(map(frozenset, c1))

def scan_d(d, c_i, min_sup):
    count = {}
    for id in d:
        for j in c_i:
            if j.issubset(id):
                if not j in count:
                    count[j] = 1
                else:
                    count[j] += 1
    num_items = float(len(d))
    ret_list = []
    support_data = {}
    for key in count:
        support = count[key] / num_items
        if support >= min_sup:
            ret_list.append(key)
        support_data[key] = support
    return ret_list, support_data

def gen_apriori(l_i, k):
    len_l_i = len(l_i)
    temp_dict = {}
    for i in range(len_l_i):
        for j in range(i + 1, len_l_i):
            L1 = l_i[i] | l_i[j]
            if len(L1) == k:
                if not L1 in temp_dict:
                    temp_dict[L1] = 1
    return list(temp_dict)

def load_data():
    with open('data.pk', 'rb') as f:
        my_dataset = pickle.load(f)
    return my_dataset

def conf_calc(freq, h, support_data, br1, min_conf=0.6):
    prunedH = []
    for con_seq in h:
        conf = support_data[freq] / support_data[freq - con_seq]
        if conf >= min_conf:
            # print(freq - con_seq, "-->", con_seq, "\tconf:", conf)
            br1.append((freq - con_seq, con_seq, conf))
        else:
            prunedH.append(con_seq)
    return prunedH

def gen_rules(l, support_data, min_conf=0.6):
    rule_list = []
    for i in range(1, len(l)):
        for freqSet in l[i]:
            h_1 = [frozenset([item]) for item in freqSet]
            if i > 1:
                rules_conseq(freqSet, h_1, support_data, rule_list, min_conf)
            else:
                conf_calc(freqSet, h_1, support_data, rule_list, min_conf)
    return rule_list

def rules_conseq(freq_set, h, support_data, b_1, min_conf=0.7):
    is_find = True
    m = 1
    mp_1 = h
    while is_find:
        if len(freq_set) > m:
            if m > 1:
                mp_1 = gen_apriori(h, m)
            h_0 = conf_calc(freq_set, mp_1, support_data, b_1, min_conf)
            if len(h_0) != 0:
                h_0 = list(set(frozenset([item]) for row in mp_1 for item in row))
                h = list(set(h) - set(h_0))
            m = m + 1
            if len(h) < m:
                is_find = False
        else:
            is_find = False

if __name__ == "__main__":
    data_set = load_data()
    st = time.time()
    l, supp_data = apriori(data_set, min_sup=0.16)
    rules = gen_rules(l, supp_data, min_conf=0.5)
    et = time.time()
    print("程序花费时间{}秒".format(et - st))


