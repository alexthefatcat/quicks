


if False:
    def get_var_name(arg_name_find):
        import inspect
        frame = inspect.currentframe().f_back
        caller_code = frame.f_code
        caller_vars = frame.f_globals | frame.f_locals
        for var_name, var_value in caller_vars.items():
            if var_value is arg_name_find:
                return var_name
    
    
    import inspect
    
    def get_var_name(arg_name_find):
        # Traverse the stack to find the top-most frame
        frame = inspect.currentframe()
        while frame.f_back:
            frame = frame.f_back
        
        caller_vars = frame.f_globals | frame.f_locals
        for var_name, var_value in caller_vars.items():
            if var_value is arg_name_find:
                return var_name
    
    # Example usage
    caller_var = get_var_name
    var_name = caller_var(caller_var)
    print(f"The name of the variable is: {var_name}")


# this works as wanted in spyder but not in cmd
def get_var_name(arg_name_find):
    import inspect
    top_var_name = None
    top_var_name = []
    frame = inspect.currentframe()
    while frame.f_back:
        frame = frame.f_back
        caller_vars = frame.f_globals | frame.f_locals
        for var_name, var_value in caller_vars.items():
            if var_value is arg_name_find:
                #top_var_name = var_name
                top_var_name.append(var_name)
                break
        else:
            return str(top_var_name)
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
