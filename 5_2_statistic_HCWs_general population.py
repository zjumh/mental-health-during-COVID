#compare mental health related tweets proportion between HCWs and the general population
import pandas as pd
import datetime
from scipy import stats
data = pd.read_csv("D:\\research\COVID\\text\\result\count\\count7D1.csv")
#test for anxiety
p = data['Panxiety_p'].to_list()
m = data['Manxiety_p'].to_list()
data['anxiety_pm']=data['Panxiety_p']-data['Manxiety_p']
#normal test
print(data['Panxiety_p'].describe())
print(data['Manxiety_p'].describe())
p_m = data['anxiety_pm'].to_list()
print(stats.shapiro(p))
print(stats.shapiro(m))
print(stats.shapiro(p_m))
## abnormal distribution,rank test
print(stats.wilcoxon(p, m, zero_method='wilcox', correction=False))
print(stats.ttest_rel(p,m))

## test for depression
p = data['Pdepression_p'].to_list()
m = data['Mdepression_p'].to_list()
#normal test
print(data['Pdepression_p'].describe())
print(data['Mdepression_p'].describe())
data['depression_pm']=data['Pdepression_p']-data['Mdepression_p']
p_m = data['depression_pm'].to_list()
print(stats.shapiro(p))
print(stats.shapiro(m))
print(stats.shapiro(p_m))
## abnormal distribution,rank test
print(stats.wilcoxon(p, m, zero_method='wilcox', correction=False))
print(stats.ttest_rel(p,m))

# test for insomnia
p = data['Pinsomnia_p'].to_list()
m = data['Minsomnia_p'].to_list()
#normal test
print(data['Pinsomnia_p'].describe())
print(data['Minsomnia_p'].describe())
data['insomnia_pm'] = data['Pinsomnia_p']-data['Minsomnia_p']
p_m = data['insomnia_pm'].to_list()
print(stats.shapiro(p))
print(stats.shapiro(m))
print(stats.shapiro(p_m))
## abnormal distribution,rank test
print(stats.wilcoxon(p, m, zero_method='wilcox', correction=False))
print(stats.ttest_rel(p,m))

# test for abuse
p = data['Pabuse_p'].to_list()
m = data['Mabuse_p'].to_list()
#normal test
print(data['Pabuse_p'].describe())
print(data['Mabuse_p'].describe())
data['abuse_pm'] = data['Pabuse_p']-data['Mabuse_p']
p_m = data['abuse_pm'].to_list()
print(stats.shapiro(p))
print(stats.shapiro(m))
print(stats.shapiro(p_m))
## abnormal distribution,rank test
print(stats.wilcoxon(p, m, zero_method='wilcox', correction=False))
print(stats.ttest_rel(p,m))