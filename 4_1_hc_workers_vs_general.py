# compare mental health related tweets proportion between HCWs and the general population
import pandas as pd
import datetime
from scipy import stats

data = pd.read_csv("D:/research/COVID/text/result/count/count7D.csv")

def symptom_statistic(symptom):
    print(symptom)
    p = data[f'P{symptom}_p'].to_list()
    m = data[f'M{symptom}_p'].to_list()
    data[f'{symptom}_pm'] = data[f'P{symptom}_p'] - data[f'M{symptom}_p']
    # normal test
    print(data[f'P{symptom}_p'].describe())
    print(data[f'M{symptom}_p'].describe())
    p_m = data[f'{symptom}_pm'].to_list()
    print(stats.shapiro(p))
    print(stats.shapiro(m))
    print(stats.shapiro(p_m))
    # abnormal distribution,rank test
    print(stats.wilcoxon(p, m, zero_method='wilcox', correction=False))
    print(stats.ttest_rel(p, m))

symptom_list = ['anxiety', 'depression', 'insomnia', 'abuse']
for i in symptom_list:
    symptom_statistic(i)
