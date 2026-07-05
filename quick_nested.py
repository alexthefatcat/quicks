# -*- coding: utf-8 -*-
"""Created on Wed Nov  8 03:05:16 2023@author: alexm"""


def unnest(nes_con, with_loc=False):
    def unnest_generator(obj):
        if isinstance(obj, (tuple, list)):
            for e in obj:
                yield from unnest_generator(e)
        else:
            yield obj
    return list(unnest_generator(nes_con))

def find_nest(nes_con, func):
    # find objectects nest inside which mathc funtion
    pass
    
def get_from_nested(nes_con, loc):
    if len(loc)==1:
        return nes_con[loc[0]]
    return get_from_nested(nes_con[loc[0]], loc[1:])

if __name__ == "__main__":
    v = [1, [2 ,[2,4],3,[[5,6,7,(8,9)]]]]        
    print(unnest(v))
    vvv_9 = v[1][3][0][3][1]
    loc = [1, 3, 0, 3, 1]
    vv_9 = get_from_nested(v, loc)
    