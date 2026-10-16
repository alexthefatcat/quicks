# -*- coding: utf-8 -*-
"""Created on Sat Sep  5 03:04:59 2026@author: alexm





"""




from MultiStageTaskRunner import MultiStageTaskRunner


import sys
from PyQt5.QtWidgets import QApplication

def stage_1(msg):
    out = []
    for n in range(2,1000):
        for e in out:
            if out%e ==0:
                break
        else:
            out.append(e)
            yield e

def stage_2():
    pass

def stage_3():
    pass

def stage_4():
    pass

stages = [stage_1, stage_2, stage_3, stage_4]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MultiStageTaskRunner(stages)
    window.show()
    sys.exit(app.exec_())
    