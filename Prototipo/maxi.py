# coding: utf-8

from bron_kerbosch1 import bronker_bosch1
from bb import bronker_bosch2
#from bronker_bosch3 import bronker_bosch3
from data import *
from reporter import Reporter

def get_SS():
    funcs = [bronker_bosch1,
        bronker_bosch2]
    # bronker_bosch3]

    for func in funcs:
        report = Reporter('## pivot')
        func([], set(NODES), set(), report)

    return report.cliques

if __name__ == '__main__':
    funcs = [bronker_bosch1,
             bronker_bosch2]
             #bronker_bosch3]

    for func in funcs:
        report = Reporter('## pivot')
        func([], set(NODES), set(), report)
        report.print_report()