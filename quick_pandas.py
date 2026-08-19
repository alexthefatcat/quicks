
def update_database(database_fp, df_new=None, col_id = 'File Path', file_status = "file_status", overwrite=False):
    import pandas as pd
    import os

    if overwrite:
        df_new.to_csv(database_fp)
    if os.path.exists(database_fp):
        df_database = pd.read_csv(database_fp, index_col = 0) 
        if df_new is None or len(df_new)==0:
            print('No New Data')
            return df_database
        
        df_new = df_new.copy()
        df_new[file_status] = 'Exists'   
        
        both_names = df_database[col_id].isin(df_new[col_id])
        df_database.loc[~both_names, file_status] = 'Missing'
        df_database.loc[both_names, file_status] = 'Exists'          
        
        only_in_df = df_new[~df_new[col_id].isin(df_database[col_id])].copy()
        only_in_df[file_status] = 'New'
        
        df_database_updated = pd.concat([df_database, only_in_df], ignore_index=True)
    else:
        if df_new is None:
            assert False,'The File does not exist nore does the new dataframe to append'
        df_database_updated = df_new
        
    df_database_updated = df_database_updated.reset_index(drop=True)
    df_database_updated.to_csv(database_fp)
    return df_database_updated




