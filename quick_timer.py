# -*- coding: utf-8 -*-
"""Created on Sat Sep 27 05:16:23 2025@author: Alexm"""






from time import time

class Timer:
    def __init__(self, msg=''):
        self.msg =msg      
    def __enter__(self):
        self.start = time()
        return self

    def __exit__(self, *args):
        print(self.msg+f'(timetaken: {time() - self.start:.2f}s)')






if __name__ == '__main__':
    with Timer('Squaring 1000000 numbers'):
        [x ** 2 for x in range(1000000)]
