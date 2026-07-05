# -*- coding: utf-8 -*-
"""Created on Mon Nov 11 10:40:52 2024@author: AlexMilroy"""


def histogram(data, nbins=50, get_bins=False, get_info=False, plot=True, title=None, clip=None, info_extra=True, axis_limits=None):
    # in future add more than one set of data?
    # max min median mean 10% 90% total points, number of nans
    import numpy as np
    import matplotlib.pyplot as plt
    shape = data.shape
    data = data.flatten()
    if clip:
        assert 0.5 >= clip >= 0
        data = np.sort(data)
        index = int(len(data)*clip)
        data = data[index:-index]
    range0 = None
    if data.dtype == np.dtype('uint8'):    
        if nbins==256:
            range0 = (data.min(), data.max())
            nbins = range0[1] - range0[0]
        if not axis_limits is None:
            range0 = axis_limits
            nbins = axis_limits[1] -axis_limits[0]
    counts, bin_edges = np.histogram(data, bins=nbins, range=range0)
    cumulative_counts = np.cumsum(counts)
    
    if info_extra:
        mean = np.nanmean(data)  # Mean, ignoring NaNs
        std_dev = np.nanstd(data)  # Standard deviation, ignoring NaNs
        num_elements = data.size  # Total number of elements
        
        num_nans = np.isnan(data).sum()  # Number of NaNs
        
        min_value = np.nanmin(data)  # Minimum value, ignoring NaNs
        percentile_10 = np.nanpercentile(data, 10)  # 10th percentile, ignoring NaNs
        median = np.nanmedian(data)  # Median value, ignoring NaNs
        percentile_90 = np.nanpercentile(data, 90)  # 10th percentile, ignoring 
        max_value = np.nanmax(data)  # Maximum value, ignoring NaNs
        
        info0 = f'Mean(𝜇): {mean:.03f},  𝜎=± {std_dev:.03f} (𝑛={num_elements})'
        info1 = f'Count-NaNs:{num_nans}, shape:{shape}'
        info2 = f'min, perc(10), median, perc(90), max: [{min_value:.03f}, {percentile_10:.03f}, {median:.03f}, {percentile_90:.03f}, {max_value:.03f}]'
        infos = '\n'.join([info0, info1, info2])
        
    if plot:
        fig, ax1 = plt.subplots(figsize=(8, 6))
        
        if False:
            ax1.hist(data, bins=nbins                      , color='blue', edgecolor='black', alpha=0.7, label='Histogram')
        else:
            bin_width = bin_edges[1] - bin_edges[0]
            ax1.bar(bin_edges[:-1], counts, width=bin_width, color='blue', edgecolor='black', alpha=0.7, label='Histogram')
            
        ax1.set_xlabel('Value')
        ax1.set_ylabel('Frequency', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
    
        ax2 = ax1.twinx()
        ax2.hist(data, bins=nbins, color='red', edgecolor='black', alpha=0.3, cumulative=True, label='Cumulative')
        ax2.set_ylabel('Cumulative Frequency', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        
        ax1.grid(True)
        if info_extra:
            pinfos = '\n   '.join(['HistogramInfo:-']+infos.split('\n')+[''])
            print(pinfos)
            # find best location to insert text
            # ax1.text(bin_edge, count, str(int(count)), ha='center', va='bottom')
        if title is None:
            fig.suptitle('Histogram of NumPy Array with Cumulative Overlay')
        else:
            fig.suptitle(title)            
        fig.legend(loc='upper left', bbox_to_anchor=(0.15, 0.85))
        plt.show()
    if get_info:
        print("Bin counts:", counts)
        print("Bin edges:", bin_edges)
        print("Cumulative counts:", cumulative_counts)    
    if get_bins:
        return counts, bin_edges, cumulative_counts



if __name__ == '__main__':
    print('Run Examples')























