 
'''




print_debug() ?






title
section differnt colors
progress bars
line number


###############################################################################
#                         This_is_The_Title                                   #
###############################################################################





'''
     
#%%----------------------------------------------------------------------------

def progress_bar(progress, total, color=None):
    from colorama import init, Fore
    init()
    color = Fore.GREEN if color is None else color
    bar_length = 40
    filled_length = int(bar_length * progress / total)
    bar = color + '█' * filled_length + '-' * (bar_length - filled_length) + Fore.RESET
    print(f'\rProgress: |{bar}| {progress}/{total}', end='\r')


import time
for i in range(0, 101):
    if i in(50,51,52,53,54):
        i = 23
    progress_bar(i, 100)
    time.sleep(0.1)
print('\n')
#%%----------------------------------------------------------------------------

aa = 433
def print2(variable):
    #add multiple args
    import inspect
    import sys    
    # Get the current frame
    frame = inspect.currentframe().f_back
    # Get the line number
    line_number = frame.f_lineno
    # Find the variable name
    local_vars = frame.f_locals.items()
    variable_name = [name for name, val in local_vars if val is variable][0]
    # Print the variable name, value, and line number
    print(f'# {variable_name} -> {variable} (line {line_number})')

print2(aa)    
        
 #%%----------------------------------------------------------------------------
    




from colorama import init as colorama_init, Fore, Style
colorama_init()

print(f"This is {Fore.GREEN}color{Style.RESET_ALL}!")



from colorama import init, Fore, Back, Style

# Initialize colorama
init()

from colorama import init, Fore, Back, Style

# Initialize colorama
init()

print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "Bright light blue text" + Style.RESET_ALL)
print(Fore.RED + Back.WHITE + "Red text with white background" + Style.RESET_ALL)

from colorama import init, Fore

# Initialize colorama
init()

def print_colored(text, color):
    print(color + text + Fore.RESET)

print_colored("Hello in red", Fore.RED)
print_colored("Hello in green", Fore.GREEN)
print_colored("Hello in blue", Fore.BLUE)
print_colored("Hello in light blue", Fore.LIGHTBLUE_EX)





from colorama import init, Fore

# Initialize colorama
init()

print(Fore.LIGHTBLUE_EX + "This is light blue text" + Fore.RESET)
print(Fore.LIGHTGREEN_EX + "This is light green text" + Fore.RESET)
print(Fore.LIGHTCYAN_EX + "This is light cyan text" + Fore.RESET)


from colorama import init, Fore, Style

# Initialize colorama
init()

print(Style.BRIGHT + Fore.LIGHTBLUE_EX + "Bright light blue text" + Style.RESET_ALL)
print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "Bright light green text" + Style.RESET_ALL)
print(Style.BRIGHT + Fore.LIGHTCYAN_EX + "Bright light cyan text" + Style.RESET_ALL)




