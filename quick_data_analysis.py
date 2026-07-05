# -*- coding: utf-8 -*-
"""Created on Fri Jun  6 19:27:34 2025@author: Alexm"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



def create_dataframe():
    # Sample data
    np.random.seed(41)
    ages_male = np.random.normal(30, 10, 500)
    ages_female = np.random.normal(32, 12, 500)
    
    # Create DataFrame
    df = pd.DataFrame({"Age": np.concatenate([ages_male, ages_female]), 
                       "Sex": ["Male"] * len(ages_male) + ["Female"] * len(ages_female)})
    
    df.loc[(df['Age']>19) & (df['Age']<31),'Age'] = df.loc[(df['Age']>19) & (df['Age']<31),'Age']+10
    df['Male'] = df['Sex'] == 'Male'
    df['Color'] = np.random.choice(['Blue', 'Green', 'Yellow', 'Red', 'Orange'], size=len(df))
    df['GamingAbility'] = np.random.normal(30, 10, len(df))
    df.loc[np.random.choice([True, False], size=len(df), p=[0.3, 0.7]), 'GamingAbility'] = np.nan
    df.loc[df['GamingAbility'].isna(), 'GamingAbility'] = np.random.normal(80, 10, sum(df['GamingAbility'].isna()) )
    df['GamingAbility2'] = df['GamingAbility']-df['GamingAbility'].min()
    df['GamingAbility2'] = df['GamingAbility2']/df['GamingAbility2'].max()
    df['col_no'] = np.random.choice(['Col__01', 'Col__09', 'Col__03', 'Col__07', 'Col__08'], size=len(df))        
    return df


df = create_dataframe()



'''
True/Postive # Male
MultiClass   # Color
Regression   # GamingAbility2



Add percentage of the middle to show of the data
sort bins

add line number to graph
'''





 
#%%----------------------------------------------------------------------------




def safe_divide(numerator, denominator):
    return np.where(denominator == 0, np.nan, numerator / denominator)

def plot_missing(ax, x, y, limits=None, se=None, mean_ratio=None, color='black'):
    nan_mask = np.isnan(y)
    y_interp = np.copy(y)
    y_interp[nan_mask] = np.interp(x[nan_mask], x[~nan_mask], y[~nan_mask])
    
    ax.plot(x, y, marker='o', linestyle='-', color=color, alpha=0.3, label="Original Data")
    ax.plot(x, y_interp, linestyle='--', color='grey', alpha=0.7, label="Interpolated")
    ax.scatter(x[nan_mask], y_interp[nan_mask], marker='x', color='red', label="Missing Data")   
    
    if se is not None:
        ax.errorbar(x, y, yerr=se, fmt="o", capsize=5, label="Standard Error", color=color, alpha=0.3)
    if mean_ratio is not None:
        ax.axhline(y=mean_ratio, color=color, alpha=0.5, linestyle=':', label=f"Mean Ratio ({mean_ratio:.2f})")
    if limits is not None:
        ax.set_ylim(*limits)

def plot_stacked_histogram(ax, df, col_stacking, col_xaxis, bins=None, values=None, columns_sorter=None, colors=None):
    
    df_dict = {key: value[col_xaxis] for key, value in df.groupby(col_stacking)}
    if columns_sorter is None:
        columns_sorter = sorted    
    if values is None:
        values = list(columns_sorter(df_dict.keys()))
        
    df_dict = {k:df_dict[k] for k in values}

    if len(df_dict)==2 and colors is None:
        colors=['royalblue', 'salmon']
        
    ax.hist(df_dict.values(), bins=bins, stacked=True, label=list(df_dict.keys()), color=colors, edgecolor = ("black"), alpha=0.7)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.set_xticks(bins)
    ax.legend(loc="upper left") 
    ax.set_ylabel("Count")
    ax.set_xlabel(col_xaxis)

def suggest_good_bins(s):
    values = np.sort(s.values)
    
    def percentile(n, values):
        if isinstance(n, (list,tuple)):
            return type(n)([percentile(e, values) for e in n])
        return values[int(n*(len(values)-1))]
  
    perc_min = 0.03    
    perc_inner = 0.1
    
    basics2 = percentile((0, perc_min, perc_inner, 0.5, 1-perc_inner, 1-perc_min, 1), values)
    lower  = max(basics2[0],  basics2[1] -(0.3*(basics2[2]-basics2[1])) )
    higher = min(basics2[6],  basics2[5] -(0.3*(basics2[4]-basics2[5])) )
    width = higher- lower
    correction = 10**int(np.log10(width)-1)
    l,h = lower/correction, higher/correction
    
    scores = []
    for wbin in [1,10,2,5,3,4,6,7,8,9]:
        l2 = int(wbin*(l//wbin))
        h2 = int(wbin*(h//wbin))
        w2 = h2 -l2
        if l2//wbin <3:
            l2 = 0
            w2 = h2 -l2
        n2 = w2//wbin
        nd = 12-n2
        if 4>nd>0:
            a1 = nd//2
            if l2 ==0:
                a1 = 0
            b1 = nd -a1
            l2 = l2 - (a1*wbin)
            h2 = h2 + (b1*wbin)   
        n2 = w2//wbin
        scores.append([l2,h2,wbin, w2//wbin])
    score = [e for e in scores if 20>e[-1]>9][0]
    l3,h3,bw3,*_ = correction*score[0],correction*score[1],correction*score[2],correction*score[3]
    bins = np.arange(l3, h3, bw3)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    return bins, bin_centers
  



'''
stacked histogrma
nice bins
predication rate


binary claffidication
classfication
prediction

QuickDataAnalysis
  Info
  corr
  Histograms of INput data
  models
  plot__column_afisnt_y




looks at some kaggles


'''








#Classification
if True:
    AGE = 'Age'
    SEX = 'Sex'
    df_dict = {key: value[AGE] for key, value in df.groupby(SEX)}
    if False:
        hists = {k:np.histogram(v, bins=bins)[0] for k,v in df_dict.items()} 
        total = sum(list(hists.values()))    

    bins, bin_centers = suggest_good_bins(df[AGE])
    bins2 = np.arange(bins.min(), bins.max(), 1)
    cum,_ = np.histogram(df[AGE], bins=bins2)
    cumulative_values = np.cumsum(cum)

    # Compute histogram data
    hist_male, _ = np.histogram(df_dict["Male"], bins=bins)
    hist_female, _ = np.histogram(df_dict["Female"], bins=bins)
    hist_total = hist_male+hist_female
    
    # Compute ratio (avoid division by zero)
    ratio = safe_divide(hist_male, hist_total)
    ratio2 = safe_divide(hist_male+1, hist_total+2) 
    ratio_se = safe_divide(ratio2*(1-ratio2), hist_total)**0.5 # SE = sqrt((p * (1 - p)) / n)
    ratio_mean =  sum(hist_male)/(sum(hist_total))
    

    # Create figure and axis
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    if True:
        plot_stacked_histogram(ax1, df, SEX, AGE, bins)    
    
    if True:
        ax2.plot(bins2[:-1], cumulative_values, alpha=0.1, color='purple',label='Cumaltive')
        ax2.fill_between(bins2[:-1], cumulative_values, alpha=0.1, color='purple')
        ax2.set_ylim([0, None])
        ax2.set_yticks([])
        if True:
            handles_ax1, labels_ax1 = ax1.get_legend_handles_labels()
            handles_ax2, labels_ax2 = ax2.get_legend_handles_labels()
            handles = handles_ax1 + handles_ax2
            labels = labels_ax1 + labels_ax2
            ax1.legend(handles, labels, loc="upper left")
        
    if True:
        plot_missing(ax3, bin_centers, ratio, limits=(0,1), se=ratio_se, mean_ratio=ratio_mean)
        ax2.set_ylabel("Male_Ratio")
        # ax2.set_yticks(None)  
        # ax2.set_yticklabels(None)        
        
        
    ax1.set_title("Stacked Histogram with Male/Female Ratio Overlay")
    plt.show()    
      
    

   





  
if False:  
    s = df['Age']
    
    fig, ax = plt.subplots(figsize=(10, 6))  
    plot_missing(ax, bin_centers, ratio, limits=(0,1), se=ratio_se, mean_ratio=ratio_mean)
    plt.show()     
    
    fig, ax = plt.subplots(figsize=(10, 6))
    values = list(df['Color'].unique())
    plot_stacked_histogram(ax, df, 'Color', 'Age', bins, df['Color'], colors=values)
    plt.show()   
        
      
        

    bins5 = np.arange(10, 100, 2)  
    fig, ax = plt.subplots(figsize=(10, 6))       
    plot_stacked_histogram(ax, df, 'Sex', 'GamingAbility', bins5)
    plt.show()       
  

if True:
    #MultiCLASS
    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(10, 10), sharex=True)
    
    values = list(df['Color'].unique())
    
    # First plot – stacked histogram
    plot_stacked_histogram(ax1, df, 'Color', 'Age', bins, df['Color'], colors=values)
    ax1.set_title('Relative Age Distribution by Color')
    ax1.legend(loc='upper right')

    ax1b = ax1.twinx()
    ax1b.plot(bins2[:-1], cumulative_values, alpha=0.1, color='purple',label='Cumaltive')
    ax1b.fill_between(bins2[:-1], cumulative_values, alpha=0.1, color='purple')
    ax1b.set_ylim([0, None])
    ax1b.set_yticks([])
    
    
    df_dict = {key: value['Age'] for key, value in df.groupby('Color')}
    bottom = np.zeros(len(bins) - 1)  # Initial base (bottom) for stacking
    counts = [np.histogram(d, bins=bins)[0] for d in df_dict.values()]
    total_counts =  np.stack(counts).sum(0)
    total_counts_error = [(e+1)**-0.5 for e in total_counts]
    relative_counts = [list(r/total_counts) for r in counts]
        
    colors =values
    for count, label, color in zip(relative_counts, df_dict.keys(), colors):
        ax2.bar(bins[:-1], count, width=np.diff(bins), bottom=bottom,
               label=label, color=color, edgecolor='black', alpha=0.7, align='edge')
        bottom += count  # Update bottom for next layer
        
        ax2.plot(bins[:-1]+2.5, total_counts_error)
        ax2.scatter(bins[:-1]+2.5, total_counts_error,color="black")
    print('2.5 needs fixing')    
    plt.tight_layout()
    plt.show()
    
    
    





  
    
  
    