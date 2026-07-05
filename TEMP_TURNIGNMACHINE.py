



default = (None,)

class turing_machine:
    def __init__(self):
        self.create_tape()
        # at the moment negative values are appended at the end rather than the start of a list
        
    def create_tape(self):
        self.tape = [[], [None], []]
        
    def __tape_index(self, index):
        index0 = max(0,abs(index)-1)
        if index<0:
            return (0, index0)
        if index==0:
            return (1, index0)
        if index>0:
            return (2, index0)
        
    def __prepare_tape(self, lis, index):
        extra_len = 1 + index - len(lis)
        if extra_len>0:
            lis.extend([None for _ in range(extra_len)])
        
    def __call__(self, index, value=default):
        tape_index, index0 = self.__tape_index(index)
        tape0 = self.tape[tape_index]        
        self.__prepare_tape(tape0, index0)
        if value is default:
            return tape0[index0]
        tape0[index0] = value
        
    def __str__(self):
        return str(self.tape)
    
    def __iter__(self):
        for kk, t in enumerate(self.tape):
            for k,v in enumerate(t):
                yield (k-len(t) if kk==0 else k+kk-1, v)
          

tm = turing_machine()
loc = 0
for n in range(10):
    print('\nIteration ', n)
    value = tm(loc)
    # if value is None:
    if True:
        loc = loc+1
    tm(loc,1)
    print(f'   {value=}, {loc=}')
    print('  ', tm)

if False:
    a = ([1,1,1,1], [2], [3,3,3])
    tm.tape = a
    dict(tm)



 
       
 
assert False  
        
# index=3
# t = [(0,index<0),(1,index==0),(2,index>1)]



# def get_first(t):
#     for k,v in t.items():
#         if v:
#             return k

# t = {0:index<0, 1:index==0, 2:index>1}

# get_first( {0:index<0, 1:index==0, 2:index>1} )

p = [1,1]

index = 10


    


p[10] = 0







default = [None,]

tapes = [[],[],[]]

def tape(index, value=default, tapes=tapes):
    tape_index = 0 if index<0 else 1 if index==0 else 2
    tape = tapes[tape_index]
    index0 = abs(index)
    if values is default:
       return tape[index]
    else:
       tape[index] = value




    




