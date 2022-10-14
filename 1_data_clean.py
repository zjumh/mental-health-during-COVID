import pandas as pd
import datetime
import os
data_path = '/data_8t/COVIDTweets'
write_path1 = '/data_8t/lmh_total/data_clean/'
write_path2 = '/data_8t/lmh_total/data_cleancount/'

for file in os.listdir(data_path):
    file_path = os.path.join(data_path, file)
    data = pd.read_csv(file_path, low_memory=False, lineterminator="\n")
# Delete the unused information
    data = data.drop(['id_str', 'source', 'truncated', 'in_reply_to_status_id', 'in_reply_to_status_id_str',
                      'in_reply_to_user_id', 'in_reply_to_user_id_str', 'in_reply_to_screen_name',
                      'quoted_status_id', 'quoted_status_id_str', 'is_quote_status', 'retweeted_status',
                      'reply_count', 'favorite_count', 'favorited', 'retweeted', 'possibly_sensitive',
                      'filter_level', 'lang', 'matching_rules', 'current_user_retweet', 'scopes',
                      'withheld_copyright', 'withheld_in_countries', 'withheld_scope',
                      'contributors', 'display_text_range', 'quoted_status_permalink\r'], axis=1)  # step1:删除不需要的列
# Remove the tweets with URLs
    data = data.loc[-data['full_text'].str.contains('http', na=False)]
# Select the tweets containing keywords
    data = data.loc[data['full_text'].str.contains(
        "Coronavirus|Koronavirus|Corona|CDC|Wuhancoronavirus|Wuhanlockdown|Ncov|Wuhan|N95|Kungflu|Epidemic|outbreak|Sinophobia|covid-19|corona virus|covid|covid19|sars-cov-2|COVIDー19|pandemic|coronapocalypse|canceleverything|COVD|Coronials|SocialDistancingNow|Social Distancing|SocialDistancing|panicbuy|panic buy|panic buying|panicbuying|14DayQuarantine|DuringMy14DayQuarantine|panic shop|panic shopping|panicshop|InMyQuarantineSurvivalKit|panic-buy|panic-shop|coronakindness|quarantinelife|chinese virus|chinesevirus|stayhomechallenge|stay home challenge|sflockdown|DontBeASpreader|lock down|lockdown|sheltering in place|shelteringinplace|stay safe stay home|staysafestayhome|trumppandemic|trump pandemic|flattenthecurve|flattenthecurve|china virus|chinavirus|quarentinelife|PPEshortage|saferathome|stay at home|stayathome|stay home|stayhome|GetMePPE|covidiot|epitwitter|pandemie|wear a mask|wearamask|kung flu|covididiot|COVID__19",
        na=False, case=False)]
    data['Date'] = data['created_at'].apply(lambda x: x[26:30]+x[3:10])
# Convert the format of the timestamp
    def timechange(time):
        time_format = datetime.datetime.strptime(time, '%Y %b %d')
        end = datetime.datetime.strftime(time_format, '%Y-%m-%d')
        return end
    data['time'] = data['Date'].apply(timechange)
    data = data.drop(['Date'], axis=1)
    data.to_csv(write_path1+file, sep=',',  index=False)
#calulate the daily number of tweets
    c = data['time'].value_counts().to_frame()
    c.to_csv(write_path2+file, index=True, sep=',')