import os
import pandas as pd
import numpy as np
import re
data_path = '/data_8t/COVIDTweets/drug_tweets'
re_path = '/data_8t/lmh_total/drug/count'
write_path1 = '/data_8t/lmh_total/drug/clean_place/'
write_path2 = '/data_8t/lmh_total/drug/count/'
name =[]
for file in os.listdir(re_path):
    name.append(file)
print(name)
for file in os.listdir(data_path):
    file_path = os.path.join(data_path, file)
    if file in name:
        continue
    print(file)
    data = pd.read_csv(file_path, low_memory=False, lineterminator="\n")
    print(len(data))
    data['is_place'] = data['geo'].str.contains(".*")
    I = range(data.index.size)
    location = []
    data['is_user'] = data['user'].str.contains("location.*description")
    for i in I:
        try:
            if data["is_place"][i] == True:
                a = data['geo'][i]
                b = eval(a)
                location.append(b.get('full_name'))
            elif data['is_user'][i] == True:
                a = data['user'][i]
                b = eval(a)
                location.append(b.get('location'))
            else:
                location.append(" ")
        except SyntaxError:
            pass
        continue
    print(len(location))
    data['location'] = location
    print("end cycle1")
    # AL--Alabama--阿拉巴马州、AK--Alaska--阿拉斯加州、AZ--Arizona--亚利桑那州、AR--Arkansas --阿肯色州、CA--California--加利福尼亚州、CO--Colorado--科罗拉多州、
    # CT--Connecticut--康涅狄格州、DE--Delaware--特拉华州、 FL--Florida--佛罗里达州、GA--Georgia--佐治亚州、HI--Hawaii--夏威夷州、ID--Idaho--爱达荷州、IL--Illinois--伊利诺伊州、
    # IN--Indiana--印第安纳州、IA--Iowa--艾奥瓦州、KS--Kansas--堪萨斯州、KY--Kentucky--肯塔基州、LA--Louisiana--路易斯安那州、ME--Maine--缅因州、MD--Maryland--马里兰州、
    # MA- Massachusetts--马萨诸塞州、MI-- Michigan--密歇根州、MN--Minnesota--明尼苏达州、MS--Mississippi--密西西比州、MO--Missouri--密苏里州、MT--Montana--蒙大拿州、
    # NE--Nebraska--内布拉斯加州、NV--Nevada--内华达州、NH--New Hampshire--新罕布什尔州、NJ--New Jersey--新泽西州、NM--New Mexico--新墨西哥州、NY--New York--纽约州、
    # NC--North Carolina--北卡罗来纳州、ND--North Dakota--北达科他州、 OH--Ohio--俄亥俄州、OK--Oklahoma--俄克拉何马州、OR--Oregon--俄勒冈州、PA--Pennsylvania--宾夕法尼亚州、
    # RL--Rhode Island--罗得岛州、SC--South Carolina--南卡罗来纳州、SD--South Dakota--南达科他州、TN--Tennessee--田纳西州、 TX--Texas--得克萨斯州、UT--Utah--犹他州、
    # VT--Vermont--佛蒙特州、 VA--Virginia--弗吉尼亚州、WA--Washington--华盛顿州、WV--West Virginia--西弗吉尼亚州、WI--Wisconsin--威斯康星州、WY--Wyoming--怀俄明州。
    state = "Alaska| AK|Alabama| AL|Arkansas| AR|Arizona| AZ|California| CA|Colorado| CO|Connecticut| CT|Delaware| DE|Florida| FL|Georgia| GA|Hawaii| HI|Iowa| IA|Idaho| ID|Illinois| IL|Indiana| IN|Kansas| KS|Kentucky| KY|Louisiana| LA| ME|Maine| MD|Maryland|Massachusetts| MA|Michigan| MI|Minnesota| MN|Missouri| MO|Mississippi| MS|Montana| MT|North Carolina| NC|North Dakota| ND|Nebraska| NE|New Hampshire| NH|New Jersey| NJ|New Mexico| NM|Nevada| NV|New York| NY|Ohio| OH|Oklahoma| OK|Oregon| OR|Pennsylvania| PA|Rhode Island| RL|South Carolina| SC|South Dakota| SD|Tennessee| TN|Texas| TX|Utah| UT|Virginia| VA|Vermont| VT|Washington| WA|Wisconsin| WI|West Virginia| WV|Wyoming| WY"
    data['state'] = "nan"
    print("begin cycle2")
    s = []
    for m in data.index:
        a = data.loc[m, 'location']
        b = re.findall(state, a)
        c = '_'.join(b)
        s.append(c.strip())
    print(len(s))
    data['state'] = s
    data['state'].replace('', np.nan, inplace=True)
    data = data[-data['state'].isna()]
    data = data.drop(['is_user'], axis=1)
#caculate the number of tweets in each state
    c = data['state'].value_counts().to_frame()
    print("begin write file")
    data.to_csv(write_path1+file, index=False)
    c.to_csv(write_path2 + file, index=True)


