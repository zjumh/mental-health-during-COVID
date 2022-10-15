import pandas as pd
import re
import os

# Full name of 50 states
full_name = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida',
             'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
             'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska',
             'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
             'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee',
             'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
# Abbreviation of 50 states
abbr_name = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA',
           'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
           'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

nf_name1 = [' '+str(i) for i in nf_name]
nf_name2 = [str(i)+',' for i in nf_name]
state_f = full_name + abbr_name2 + nf_name1
state_keywords = "|".join(state_f)
dict1 = dict(zip(full_name,full_name))
dict2 = dict(zip(nf_name1,full_name))
dict3 = dict(zip(nf_name2,full_name))
dict1.update(dict2)
dict1.update(dict3)

# Filter tweets with a user address in Washington, D.C.
def state_dup(x,keywords):
    DC_list = ["Washington, DC","Washington, D.C.","Washington,DC","Washington,D.C.","D.C.","Washington DC"]
    if any(e in x for e in DC_list): return "Washinton, DC"
    else:
        state_list = re.findall(keywords,x)
        state_list_new = [dict1[i] for i in state_list]
        result = list(set(state_list_new))
        if len(result)==1: return(result[0])
        else: return ''

# Get the geo information
def state(data):
    data['place_info'] = data['place'].apply(lambda x: eval(str(x)).get('full_name') if str(x) != 'nan' else '')
    data['location_info'] = data['user'].apply(lambda x: eval(str(x)).get('location'))
    data['place_location'] = data.apply(lambda x: x['location_info'] if x['place_info'] == '' else x['place_info'],
                                        axis=1)
    data['state'] = data['place_location'].apply(lambda x: state_dup(x, state_keywords))
    data1 = data.drop(['place_info', 'location_info'],axis=1)
    return data1



mental_pattern = {
        'anxiety': "(anxiety|anxious|antsy|restlessness|concern about the future|concerned about the future|concerning about the future|"
                   "dread fear|nervousness|panic|panic attacks|paranoia|worry|worried|worrying)",
        'depression': "(collapse|anger|compassion|shame|depressed|escape|loneliness|darkness|sensitivity|lupus|autism|jealousy|paranoia|"
                      "postpartum|hysteria|asthma|narcissism|pain mood|aggression|immature|ruthless|insecurity|mirage|"
                      "cheating|hidden|negative affect|affect lability|emotional instability|emotional stories|"
                      "emotional support|aggressiveness|snappy|agitated|irritable mood|altered mood|mood changes|mood swing|anger|"
                      "frustration|apathy|loss of interest|indifference|bliss|elation|euphoria|warm fuzziness|calmness|depressed mood|"
                      "depression|down feelings|feeling low|feel low|felt low|melancholy|miserable|sadness|feeling empty|fussiness|"
                      "hopelessness|stress|suicidal ideation)",
        'insomnia': "(abnormal dreams|nightmares|vivid dreams|asthenia|disturbed sleep|insomnia|sleep problems|early awakening|"
                    "drowsiness|lassitude|listlessness|exhaustion|fatigue|lethargic|sluggishness|somnolence|tiredness|"
                    "weariness|hypersomnia)",
        'abuse': "(substance dependence|physical dependence|psychological dependence|harmful use|withdrawal state|addiction|"
                 "addictive behaviour|reinforcing|rewarding|psychoactive substances|depressants|stimulants|alcohol and drug dependence|"
                 "abstinent|heavy drink|drinker|alcoholism|alcohol intake|alcohol misuse|alcohol consumption|alcohol addiction|destroyer|"
                 "trippy|alcohol dependence|alcoholic| risky drinking|harmful drinking|chronic alcohol use|drinking behavior|"
                 "behavior impairment|chronic alcoholic intoxication|problem alcohol use|alcohol-meat|drinking for pleasure|"
                 "avoidance behaviors|occupational impairment|marijuana addict|cocaine addict|heroin addict|cannabis addict|"
                 "hallucinogen|opioid abuse|war on drugs|illicit use of drugs|drug affliction|narcotics abuse|drug cues|"
                 "drug-seeking|weakening self-regulation|drug abuse vulnerability|drug addiction|prescription drug abuse|"
                 "drug habituation|substance-induced|drug misuse|ecstasy|illicit drug|chronic drug problem|drug involvement|"
                 "drug reinforcement|drug relapse|rehab|rehabilitation|nicotine|harmful smoking|cigarette smoking|tobacco consumption|"
                 "tobacco chewing|alternative tobacco product|dual-tobacco use|poly-tobacco use|tobacco dependent|"
                 "electric cigarette use|vape pens|e-pens|e-hookah and vape sticks|smokeless tobacco|hookah|cigars|"
                 "cigarillos and little cigars|daily smoking|tobacco use disorder|quitting smoking|internet gaming disorders|"
                 "gaming disorder|internet addiction|social media addictions|smartphone addiction|attention deficit disorder|"
                 "problematic online gaming|disordered gamer|gaming craving|video game addiction|internet game disorder|"
                 "maladaptive player game|problem internet use|pathological game use|online game genres|video-game exposure|"
                 "game addiction|recreational game user|addictive game behaviors|gaming community|gain ability to challenge and dominate others|"
                 "acquire status and power|immersion|escape real life|gambling disorder|pathological gambling|gambling harm|"
                 "problem gambling|problematic online gambling|disordered gamblers|compulsive gambling|gambling craving|"
                 "silent addiction|problem gambler|gambling behavior|preoccupation with gambling|chronic gambler|gambling addiction|"
                 "gamble harm up|mounting losses|gambling-motivated crime|at-risk gambling|persistent gambling|recurrent gambling|"
                 "gambling-related cognitive distortion|uncontrolled gambling|compulsive gambling|internet addiction|"
                 "problematic use|problematic phone use|social media addiction|addiction)"
    }

# Filter mental health related tweets
def mental(data):
    prefix = "( |,|;|\.|\!|^)"
    suffix = "( |,|;|\.|\!|$)"
    pattern_keywords_negative = "(no|not|n't|n’t|non|than|neither|nor|instead of)"
    
    for status, pattern in mental_pattern.items():
        neg_pattern = pattern_keywords_negative + " (\w+\s){0,3}" + pattern+suffix
        data[status] = (data['full_text'].str.contains(prefix + pattern + suffix, na=False, case=False) ^ data['full_text'].str.contains(neg_pattern, na=False, case=False))
    data_mental = data[(data['anxiety']|data['depression']|data['insomnia']|data['abuse'])]
    return data, data_mental
# count the daily tweets and count the tweets including geo information monthly

def count(data_clean):
    data_clean['month'] = data_clean['time'].apply(lambda x:str(x)[0:7])
    data_clean_count = data_clean.groupby('time').agg({'id':'count'}).reset_index()
    data_clean_count.columns = ['time', 'clean']
    data_state_count = data_clean.groupby(['month', 'state']).agg({'id': 'count'}).reset_index()
    data_state_count.columns = ['month', 'state', 'clean']
    symptom = ['anxiety', 'depression', 'insomnia', 'abuse']
    for i in symptom:
        df = data_clean[data_clean[i]]
        df_time_count = df.groupby('time').agg({'id': 'count'}).reset_index()
        df_time_count.columns = ['time', i]
        df_state_count = df.groupby(['month', 'state']).agg({'id': 'count'}).reset_index()
        df_state_count.columns = ['month', 'state', i]
        data_clean_count = pd.merge(data_clean_count, df_time_count, on='time', how='outer')
        data_state_count = pd.merge(data_state_count, df_state_count, on=['month', 'state'], how='outer')
    return data_clean_count, data_state_count

data_path = "/data1/data_clean"
for file in os.listdir(data_path):
    file_path = os.path.join(data_path, file)
    data = pd.read_csv(file_path, low_memory=False, lineterminator="\n")
    data1 = state(data)
    data_clean, data_mental = mental(data1)
    time_count, state_count = count(data_clean)
    data_mental.to_csv(f"/data2/lmh/covid_review/result/data_mental{file}",index=False)
    time_count.to_csv(f"/data2/lmh/covid_review/result/time_count{file}",index=False)
    state_count.to_csv(f"/data2/lmh/covid_review/result/state_count{file}", index=False)
