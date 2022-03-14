import pandas as pd
data = pd.read_csv("/data_8t/lmh_total/model3/topic17_5.csv", low_memory=False, lineterminator="\n")
print("search")
#find the tweets whose user is a healthcare worker
data['doctor'] = data['user'].str.contains("doctor|physician|surgeon|dentist|ophthalmologist|pediatrician|gynecologist|nurse|Physician|Surgeon|Dentist|Ophthalmologist|Pediatrician|Gynecologist|Nurse", na=False, case=True)
data['medicine'] = data['user'].str.contains("Doctor of Medicine|Bachelor of Nursing|Bachelor of Science in Medicine|Bachelor of Science in Medical Technology|Bachelor of Science in Nursing|Master of Nursing|Master of Science in Medical Technology|Master of Science in Nursing|Doctor of Dental Science|Doctor of Osteopathy", na=False)
data['MD'] = data['user'].str.contains("MD |BN |B.S.Med |BSMT |B.S.Med.Tech |BSN |BSNurs |MSMT | MSN | DDS | MBBS | MHS | MPH | RPh | RN | FACP | FACS | FICS | FRCOG | FRCP ", na=False, case=True)
print("summary")
#the tweets from HCWs
data1 = data[data['doctor'] | data['medicine'] | data['MD']]
data1.to_csv('/data_8t/lmh_total/mental_job1/mental_M17.csv')
#the tweets from the general population
data2 = data[-(data['doctor'] | data['medicine'] | data['MD'])]
data2.to_csv('/data_8t/lmh_total/mental_job1/mental_P17.csv')
print("count")
#count the daily number
a = data1['time'].value_counts().to_frame()
a.to_csv("/data_8t/lmh_total/mental_job1/M_count17.csv", index=True)
b = data2['time'].value_counts().to_frame()
b.to_csv("/data_8t/lmh_total/mental_job1/P_count17.csv", index=True)
#count the number in each topic
c = data1['topic'].value_counts().to_frame()
c.to_csv("/data_8t/lmh_total/mental_job1/M_topic17.csv", index=True)
d = data2['topic'].value_counts().to_frame()
d.to_csv("/data_8t/lmh_total/mental_job1/P_topic17.csv", index=True)