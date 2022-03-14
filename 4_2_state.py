import pandas as pd
import os
data_path = "/data_8t/lmh_total/mental_place/clean_place"
re_path = "/data_8t/lmh_total/mental_place/state/WY"
state = {
'AK': 'Alaska|AK', 'AL':'Alabama|AL',
'AR': 'Arkansas|AR', 'AZ': 'Arizona|AZ','CA': 'California|CA','CO': 'Colorado|CO','CT': 'Connecticut|CT','DE': 'Delaware|DE',
'FL': 'Florida|FL', 'GA': 'Georgia|GA','HI': 'Hawaii|HI','IA': 'Iowa|IA','ID': 'Idaho|ID','IL': 'Illinois|IL','IN': 'Indiana|IN',
'KS': 'Kansas|KS','KY': 'Kentucky|KY','LA': 'Louisiana|LA','ME': 'ME|Maine','MD': 'MD|Maryland','MA': 'Massachusetts|MA',
'MI': 'Michigan|MI','MN': 'Minnesota|MN','MO': 'Missouri|MO','MS': 'Mississippi|MS','MT': 'Montana|MT','NC': 'North Carolina|NC',
'ND': 'North Dakota|ND','NE': 'Nebraska|NE','NH': 'New Hampshire|NH','NJ': 'New Jersey|NJ','NM': 'New Mexico|NM','NV': 'Nevada|NV',
'NY': 'New York|NY','OH': 'Ohio|OH','OK': 'Oklahoma|OK','OR': 'Oregon|OR','PA': 'Pennsylvania|PA','RL': 'Rhode Island|RL',
'SC': 'South Carolina|SC','SD': 'South Dakota|SD','TN': 'Tennessee|TN','TX': 'Texas|TX','UT': 'Utah|UT','VA': 'Virginia|VA',
'VT': 'Vermont|VT','WA': 'Washington|WA','WI': 'Wisconsin|WI','WV': 'West Virginia|WV','WY': 'Wyoming|WY'
}
state_name = ['AK','AL','AR','AZ','CA','CO','CT','DE','FL','GA','HI','IA','ID','IL','IN','KS','KY','LA','ME','MD','MA','MI','MN',
            'MO','MS','MT','NC',"ND","NE",'NH','NJ','NM','NV','NY','OH','OK','OR','PA','RL','SC','SD','TN','TX','UT',
            'VA','VT','WA','WI','WV','WY']
for i in state_name:
    os.makedirs(f"/data_8t/lmh_total/mental_place/state/{i}/", exist_ok=True)
name =[]
#creat a csv to storage the number of tweets number in each csv
data_count = pd.read_csv("/data_8t/lmh_total/mental_place/count.csv")
for file in os.listdir(re_path):
    name.append(file)
print(name)
for file in os.listdir(data_path):
    file_path = os.path.join(data_path, file)
    if file in name:
        continue
    print(file)
    data = pd.read_csv(file_path, low_memory=False, lineterminator="\n")
    s = []
    #add the information of state and remove the tweets containing reduplicative states
    for i in state_name:
        a = state[i]
        data[i] = data['state'].str.contains(a, na=False, case=True)
    #calculate the number of "True"
    print(len(data))
    data['state_n'] = data[state_name].sum(axis=1)
    data1 = data[(data['state_n'] == 1)]
    print(len(data1))
    for i in state_name:
        data2 = data1[data1[i]]
        data2 = data2.drop(labels=state_name, axis=1)
        #data2 = data2.drop(labels='state_n', axis=1)
        write_path = f"/data_8t/lmh_total/mental_place/state1/{i}/{file}"
        data2.to_csv(write_path)
        s.append(len(data2))
    data_count[file] = s
data_count.to_csv("/data_8t/lmh_total/mental_place/count.csv", index=False)


