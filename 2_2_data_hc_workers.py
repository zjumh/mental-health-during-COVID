import pandas as pd
import os

DOCTOR = "(doctor|physician|surgeon|dentist|ophthalmologist|pediatrician|gynecologist|nurse|Physician|Surgeon|Dentist|Ophthalmologist|Pediatrician|Gynecologist|Nurse)"
MD = "(MD|BN|B.S.Med|BSMT|B.S.Med.Tech|BSN|BSNurs|MSMT|MSN|DDS|MBBS|MHS|MPH|RPH|RN|FACP|FACS|FICS|FRCOG|FRCP)"


# filter tweets from health care workers
def hcws_select(data):
    prefix = "( |,|;|\.|\!|^)"
    suffix = "( |,|;|\.|\!|$)"
    data['doctor'] = data['user'].str.contains(prefix + DOCTOR + suffix, na=False, case=True)
    data['medicine'] = data['user'].str.contains(
        "Doctor of Medicine|Bachelor of Nursing|Bachelor of Science in Medicine|Bachelor of Science in Medical Technology|Bachelor of Science in Nursing|Master of Nursing|Master of Science in Medical Technology|Master of Science in Nursing|Doctor of Dental Science|Doctor of Osteopathy",
        na=False)
    data['MD'] = data['user'].str.contains(prefix + MD + suffix, na=False, case=True)
    data_hcw = data[data['doctor'] | data['medicine'] | data['MD']]
    data_count = data_hcw.groupby('time').agg({'id': 'count'})
    return data_count

data_path = "/data1/data_clean"

for file in os.listdir(data_path):
    file_path = os.path.join(data_path, file)
    data = pd.read_csv(file_path, low_memory=False, lineterminator="\n", keep_default_na=False)
    job_count = hcws_select(data)
    job_count.to_csv(f"/data2/lmh/covid_review/result/clean_job_count/{file}")
