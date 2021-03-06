import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

def get_plot(data, ylabel, mode = 'MLS'): 
    if mode == 'ILS':
        plt.plot(data[0], label = 'Mutation 0.01')
        plt.plot(data[1], label = 'Mutation 0.03')
        plt.plot(data[2], label = 'Mutation 0.05')
        plt.legend()
        plt.xlabel('Run')
        plt.ylabel(ylabel)
        plt.show()
        
        plt.boxplot(data)
        plt.xticks([1,2,3], ['ILS 0.01','ILS 0.03','ILS 0.05'])
        plt.ylabel(ylabel)
        plt.show()

    if mode == 'MLS':
        plt.plot(data)
        plt.ylabel(ylabel)
        plt.xlabel('Run')
        plt.show()

        plt.boxplot(data)
        plt.xticks([1], [mode])
        plt.ylabel(ylabel)
        plt.show()    

    if mode == 'GLS':
        plt.plot(data)
        plt.ylabel(ylabel)
        plt.xlabel('Run')
        plt.show()

        plt.boxplot(data)
        plt.xticks([1], [mode])
        plt.ylabel(ylabel)
        plt.show()

    if mode == 'ALL':
        plt.boxplot(data)
        plt.ylabel(ylabel)
        plt.xticks([1,2,3,4,5,6], ['MLS','ILS 0.01','ILS 0.03','ILS 0.05','GLS','ILS x GLS'])
        plt.show()

    if mode == 'Real':
        plt.plot(data[0])
        plt.ylabel(ylabel)
        plt.xlabel('Run')
        plt.show()

        plt.plot(data[1])
        plt.ylabel(ylabel)
        plt.xlabel('Run')
        plt.show()

        plt.boxplot(data)
        plt.ylabel(ylabel)
        plt.xticks([1,2], ['MLS','ILS 0.01'])
        plt.show()

def get_gls_data(data):
    gls_data_cutstate = []
    # Convert the list of strings to numeric values
    for cut_value in data:
        cut_value = cut_value.replace(']', '[').split('[')
        if len(cut_value) > 0:
            gls_data_cutstate.append(int(cut_value[1]))
    return gls_data_cutstate

def get_timeout_data(data):
    timeout_data = []
    value = []
    for i in data:
        cut_value = i.replace('[',',').replace(']',',').split(',')
        for j in cut_value:
            if len(j) > 0:
                value.append(int(j))
        timeout_data.append(np.mean(value))
    return timeout_data


if __name__ == '__main__':
    # Read data
    mls_data = pd.read_csv('data/mls/mls_with_fm.csv')
    mls_performance = pd.read_csv('data/mls/mls_with_fm_performance.csv')
    ils_data_005 = pd.read_csv('data/ils/ils_with_fm_0.05.csv')
    ils_performance_005 = pd.read_csv('data/ils/ils_with_fm_0.05_performance.csv')
    gls_data = pd.read_csv('data/gls/gls_with_fm.csv')
    gls_performance = pd.read_csv('data/gls/gls_with_fm_performance.csv')
    ### TIMEOUT DATA###
    mls_timeout_1 = pd.read_csv('data/mls/mls_with_fm_time_limit_60.csv')
    ils_timeout_1 = pd.read_csv('data/ils/ils_with_fm_0.05_limit_60.csv')
    gls_timeout_1 = pd.read_csv('data/gls/gls_with_fm_limit_60.csv')
    mls_timeout_20 = pd.read_csv('data/mls/mls_with_fm_time_limit_1200.csv')
    ils_timeout_20 = pd.read_csv('data/ils/ils_with_fm_0.05_limit_1200.csv')
    gls_timeout_20 = pd.read_csv('data/gls/gls_with_fm_limit_1200.csv')
    ### ILS X GLS ###
    gls_mutation = pd.read_csv('data/gls/gls_with_fm_mutation.csv')
    gls_mutation_performance = pd.read_csv('data/gls/gls_with_fm_mutation_performance.csv')
    gls_mutation_cutstate = get_gls_data(gls_mutation['Cutstate'])
    average_gls_mutation = np.mean(gls_mutation_cutstate)
    average_gls_mutation_performance = np.mean(gls_mutation_performance['Execution Time'] / 60)
    #print(average_gls_mutation)
    #print(average_gls_mutation_performance)

    ### REAL DATA ###
    real_mls = pd.read_csv('data/mls/mls_limit_1500.csv')
    average_real_mls = np.mean(real_mls['cutstate'])
    #print(average_real_mls)
    real_ils = pd.read_csv('data/ils/ils_0.01_limit_1500.csv')
    average_real_ils = np.mean(real_ils['cutstate'])
    #print(average_real_ils)
    get_plot([real_mls['cutstate'], real_ils['cutstate']], ylabel = 'Cutstate', mode='Real')
    mannwhitneyu_real_mls_ils = mannwhitneyu(real_mls['cutstate'], real_ils['cutstate'])
    print(mannwhitneyu_real_mls_ils)


    #### CUTSTATE ####
    data_001 = list(ils_data_005['cutstate'][:25])
    data_003 = list(ils_data_005['cutstate'][25:50])
    data_005 = list(ils_data_005['cutstate'][50:])
    gls_data_cutstate = get_gls_data(gls_data['Cutstate'])
    
    #get_plot([mls_data['cutstate'], data_001, data_003, data_005, gls_data_cutstate, gls_mutation_cutstate], ylabel= 'Cutstate', mode = 'ALL')

    average_mls_data = np.mean(mls_data['cutstate'])
    average_ils_001 = np.mean(data_001)
    average_ils_003 = np.mean(data_003)
    average_ils_005 = np.mean(data_005)
    average_gls_data = np.mean(gls_data_cutstate)
    """
    print(average_mls_data)
    print(average_ils_001)
    print(average_ils_003)
    print(average_ils_005)
    print(average_gls_data)

    get_plot(mls_data['cutstate'], ylabel= 'Cutstate', mode = 'MLS')
    get_plot([data_001, data_003, data_005], ylabel= 'Cutstate', mode = 'ILS')
    get_plot(gls_data_cutstate, ylabel= 'Cutstate', mode = 'GLS')
    get_plot([mls_data['cutstate'], data_001, data_003, data_005, gls_data_cutstate], ylabel= 'Cutstate', mode = 'ALL')
    """
    # Wilcoxon test
    mannwhitneyu_mls_gls = mannwhitneyu(mls_data['cutstate'], gls_data_cutstate)
    mannwhitneyu_mls_ils001 = mannwhitneyu(mls_data['cutstate'], data_001)
    mannwhitneyu_mls_ils003 = mannwhitneyu(mls_data['cutstate'], data_003)
    mannwhitneyu_mls_ils005 = mannwhitneyu(mls_data['cutstate'], data_005)
    mannwhitneyu_gls_ils001 = mannwhitneyu(gls_data_cutstate, data_001)
    mannwhitneyu_gls_ils003 = mannwhitneyu(gls_data_cutstate, data_003)
    mannwhitneyu_gls_ils005 = mannwhitneyu(gls_data_cutstate, data_005)
    mannwhitneyu_ils001_ils003 = mannwhitneyu(data_001, data_003)
    mannwhitneyu_ils001_ils005 = mannwhitneyu(data_001, data_005)
    mannwhitneyu_ils003_ils005 = mannwhitneyu(data_003, data_005)
    mannwhitneyu_ils001_ilsxgls = mannwhitneyu(data_001, gls_mutation_cutstate)
    mannwhitneyu_gls_ilsxgls = mannwhitneyu(gls_data_cutstate, gls_mutation_cutstate)

    print(f'MLS and GLS: {mannwhitneyu_mls_gls}')
    print(f'MLS and ILS001: {mannwhitneyu_mls_ils001}')
    print(f'MLS and ILS003: {mannwhitneyu_mls_ils003}')
    print(f'MLS and ILS005: {mannwhitneyu_mls_ils005}')
    print(f'GLS and ILS001: {mannwhitneyu_gls_ils001}')
    print(f'GLS and ILS003: {mannwhitneyu_gls_ils003}')
    print(f'GLS and ILS005: {mannwhitneyu_gls_ils005}')
    print(f'ILS001 and ILS003: {mannwhitneyu_ils001_ils003}')
    print(f'ILS001 and ILS003: {mannwhitneyu_ils001_ils005}')
    print(f'ILS001 and ILS003: {mannwhitneyu_ils003_ils005}')
    print(mannwhitneyu_ils001_ilsxgls)
    print(mannwhitneyu_gls_ilsxgls)

    #### CPU PERFORMANCE ####
    mls_performance_minutes = mls_performance['Execution Time'] / 60
    performance_001 = list(ils_performance_005['Execution Time'][:25] / 60)
    performance_003 = list(ils_performance_005['Execution Time'][25:50] / 60)
    performance_005 = list(ils_performance_005['Execution Time'][50:75] / 60)
    gls_performance_minutes = gls_performance['Execution Time'] / 60

    average_mls_performance = np.mean(mls_performance_minutes)
    average_ils_performance001 = np.mean(performance_001)
    average_ils_performance003 = np.mean(performance_003)
    average_ils_performance005 = np.mean(performance_005)
    average_gls_performance = np.mean(gls_performance_minutes)
    """
    print(average_mls_performance)  
    print(average_ils_performance001)  
    print(average_ils_performance003)  
    print(average_ils_performance005)  
    print(average_gls_performance)

    get_plot(mls_performance_minutes, ylabel= 'Time (min)', mode = 'MLS')
    get_plot([performance_001, performance_003, performance_005], ylabel= 'Time (min)', mode = 'ILS')
    get_plot(gls_performance_minutes, ylabel= 'Time (min)', mode = 'GLS')
    get_plot([mls_performance_minutes, performance_001, performance_003, performance_005, gls_performance_minutes], ylabel= 'Time (min)', mode = 'ALL')
    """

    # Wilcoxon test
    mannwhitneyu_performance_mls_gls = mannwhitneyu(mls_performance_minutes, gls_performance_minutes)
    mannwhitneyu_performance_mls_ils001 = mannwhitneyu(mls_performance_minutes, performance_001)
    mannwhitneyu_performance_mls_ils003 = mannwhitneyu(mls_performance_minutes, performance_003)
    mannwhitneyu_performance_mls_ils005 = mannwhitneyu(mls_performance_minutes, performance_005)
    mannwhitneyu_performance_gls_ils001 = mannwhitneyu(gls_performance_minutes, performance_001)
    mannwhitneyu_performance_gls_ils003 = mannwhitneyu(gls_performance_minutes, performance_003)
    mannwhitneyu_performance_gls_ils005 = mannwhitneyu(gls_performance_minutes, performance_005)
    mannwhitneyu_performance_ils001_ils003 = mannwhitneyu(performance_001, performance_003)
    mannwhitneyu_performance_ils001_ils005 = mannwhitneyu(performance_001, performance_005)
    mannwhitneyu_performance_ils003_ils005 = mannwhitneyu(performance_003, performance_005)
    
    print(f'MLS and GLS: {mannwhitneyu_performance_mls_gls}')
    print(f'MLS and ILS001: {mannwhitneyu_performance_mls_ils001}')
    print(f'MLS and ILS003: {mannwhitneyu_performance_mls_ils003}')
    print(f'MLS and ILS005: {mannwhitneyu_performance_mls_ils005}')
    print(f'GLS and ILS001: {mannwhitneyu_performance_gls_ils001}')
    print(f'GLS and ILS003: {mannwhitneyu_performance_gls_ils003}')
    print(f'GLS and ILS005: {mannwhitneyu_performance_gls_ils005}')
    print(f'ILS001 and ILS003: {mannwhitneyu_performance_ils001_ils003}')
    print(f'ILS001 and ILS003: {mannwhitneyu_performance_ils001_ils005}')
    print(f'ILS001 and ILS003: {mannwhitneyu_performance_ils003_ils005}')
    

    #### TIMEOUT ###
    # 1 minute
    timeout_1_001 = list(ils_timeout_1['cutstate'][:25])
    timeout_1_003 = list(ils_timeout_1['cutstate'][25:50])
    timeout_1_005 = list(ils_timeout_1['cutstate'][50:])

    gls_timeout_cutstate = get_timeout_data(gls_timeout_1['Cutstate'])

    average_mls_timeout = np.mean(mls_timeout_1['cutstate'])
    average_ils_timeout_001 = np.mean(timeout_1_001)
    average_ils_timeout_003 = np.mean(timeout_1_003)
    average_ils_timeout_005 = np.mean(timeout_1_005)
    average_gls_timeout = np.mean(gls_timeout_cutstate)
    """
    print(average_mls_timeout)
    print(average_ils_timeout_001)
    print(average_ils_timeout_003)
    print(average_ils_timeout_005)
    print(average_gls_timeout)

    get_plot(mls_timeout_1['cutstate'], ylabel= 'Cutstate', mode = 'MLS')
    get_plot([timeout_1_001, timeout_1_003, timeout_1_005], ylabel= 'Cutstate', mode = 'ILS')
    get_plot(gls_timeout_cutstate, ylabel= 'Cutstate', mode = 'GLS')
    get_plot([mls_timeout_1['cutstate'], timeout_1_001, timeout_1_003, timeout_1_005, gls_timeout_cutstate], ylabel= 'Cutstate', mode = 'ALL')
    """

    # 20 minutes
    timeout_20_001 = list(ils_timeout_20['cutstate'][:25])
    timeout_20_003 = list(ils_timeout_20['cutstate'][25:50])
    timeout_20_005 = list(ils_timeout_20['cutstate'][50:])

    gls_timeout_cutstate_20 = get_gls_data(gls_timeout_20['Cutstate'])

    average_mls_timeout_20 = np.mean(mls_timeout_20['cutstate'])
    average_ils_timeout_001_20 = np.mean(timeout_20_001)
    average_ils_timeout_003_20 = np.mean(timeout_20_003)
    average_ils_timeout_005_20 = np.mean(timeout_20_005)
    average_gls_timeout_20 = np.mean(gls_timeout_cutstate_20)
    """
    print(average_mls_timeout_20)
    print(average_ils_timeout_001_20)
    print(average_ils_timeout_003_20)
    print(average_ils_timeout_005_20)
    print(average_gls_timeout_20)

    get_plot(mls_timeout_20['cutstate'], ylabel= 'Cutstate', mode = 'MLS')
    get_plot([timeout_20_001, timeout_20_003, timeout_20_005], ylabel= 'Cutstate', mode = 'ILS')
    get_plot(gls_timeout_cutstate_20, ylabel= 'Cutstate', mode = 'GLS')
    get_plot([mls_timeout_20['cutstate'], timeout_20_001, timeout_20_003, timeout_20_005, gls_timeout_cutstate_20], ylabel= 'Cutstate', mode = 'ALL')
    """
