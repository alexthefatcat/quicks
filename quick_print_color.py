


def print_color(*args, color_args=False,**kwargs):
    '''
    red
    green
    blue
    yellow
    pink
    cyan
    white
    underline
    italic
    '''

    sep =kwargs.get('sep',' ')
    arg = sep.join([str(e) for e in args])
    
    colors = dict(
    r = "\033[0;31m",
    g = "\033[0;32m",
    y = "\033[0;33m",
    b = "\033[0;34m",
    p = "\033[0;35m",
    c = "\033[0;36m",
    w = "\033[0;37m",
    t = "\033[1m",
    u = "\033[4m",
    i = "\033[3m",
    e="\033[0m")

    options = 'rgybpcwui'    


    if color_args:
        args = list(args)
        for i in range(min([len(args),len(options)])):
            clr = colors[options[i]]
            args[i] = clr+colors['t']+str(args[i])+ colors['w']+colors['t']
        print(*args)
        return
    
    def split_with_part(msg, sep, location='before'):
        msg_split = msg.split(sep)
        if location=='before':
            return [e if i==0 else sep+e for i,e in enumerate(msg_split)]
        if location=='after':
            lmsg = len(msg_split)-1
            return [e if i==lmsg else e+sep2 for i,e in enumerate(msg_split)]
        
    sep1 = '<'
    sep2 = '>'
    
    arg2 = arg.split(sep1)
    arg2 = split_with_part(arg, sep1)
    arg3 = [split_with_part(e, sep2,'after') for e in arg2]
    arg4 = [ee for e in arg3 for ee in e]
    arg5 = ['']
    for i,e in enumerate(arg4):
        if len(e)<3 or i==0:
            arg5[-1]+=e
        elif e.count('>')==1 and e.count('<')==1 :
            arg5.append(e)
            arg5.append('')        
        else:
            arg5[-1]+=e        
    arg5 = [e for e in arg5 if e!='']

    current_states = [None,]
    arg6 = ''
    for part in arg5:
        if not (part.count('<')==1 and part.count('>')==1):
            arg6 += part
            continue
    
        part0=part[1:-1]
        end = False
        if part0.startswith('/'):
            part0 = part0[1:]
            end = True
        if not(len(part0)>0 and all([e in options for e in part0 ])):
            arg6 += part
            continue 
        
        if end:
            if current_states[-1]==part0:
                _ = current_states.pop(-1)
                if current_states[-1]==None:
                    part00 = colors['w']+colors['t'] 
                else:
                    part0 =current_states[-1]
                    part00 = ''.join([colors[k] for k in set('t'+part0)])
            else:
                arg6 += part       
            
            
        else:
            part00 = ''.join([colors[k] for k in part0.replace('t', '')+'t'])
            current_states.append(part0)        
    
        arg6 +=part00
    print(arg6+colors['e'], **kwargs)


if __name__ == '__main__':
    for n in range(60):
        print_color(n, '<b>Everton</b> are better than <r>Liverpool</r>   <y>Warning</y>')
    print_color(*list('abcdefghijklmnop'), color_args=True)
    print(*list('abcdefghijklmnop'))
    for i in range(200):
        if i%40==0:
            print_color('Game No','Home Team','score_string','score','away team','ground_info','filepath','filename', color_args=True)
        print_color(12,'Everton','Score','2-3','Liverpool','Football at Goodison Park',r"C:\Users\Alexm\Desktop\Poster2.txt","Poster2.txt", color_args=True)



