import locale
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def set_spanish_locale():
    locale.setlocale(locale.LC_ALL, 'es_AR.UTF-8')

def assert_spanish_locale():
    assert 'es' in locale.getlocale()[0]
    
def format_mil_spanish(number):
    assert_spanish_locale()
    return locale.format_string("%d", number, grouping=True)

def matplot_formatter_mil_spanish():
    return matplotlib.ticker.FuncFormatter(lambda x, p: format_mil_spanish(x))


def plot_histogram_mrs_support_count(df_freq_data, min_val, max_val, n_bins, logy=True, vline=0.025, ylabel=None):
    df_freq_data_hist = df_freq_data.rename(columns={
        'freq_percentage': 'Soporte', 
        'family': 'Familia'})

    # https://stackoverflow.com/questions/65351989/how-to-center-the-histogram-bars-around-tick-marks-using-seaborn-displot-stacki
    val_width = max_val - min_val
    bin_width = val_width / n_bins

    ax = sns.histplot(df_freq_data_hist, 
                              x='Soporte', 
                              hue='Familia',
                              multiple='dodge',
                              shrink=0.8,
                              bins=n_bins,
                              binrange=(min_val, max_val),
                              log_scale=(False, logy));

    
    if vline:
        plt.axvline(x=vline, color='red')

    plt.ylim(1, None)    
    plt.xticks(np.arange(min_val, max_val+bin_width, bin_width))

    if ylabel:
        ax.set_ylabel(ylabel)

    fig = ax.get_figure()

    return fig

