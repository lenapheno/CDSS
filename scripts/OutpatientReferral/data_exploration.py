
import pandas as pd
pd.set_option('display.width', 1000)

from collections import Counter

'''
Scenario: upon referral
Query to obtain all primary-care encounters that referred the patient to a different unit

select 
    distinct t1.pat_enc_csn_id_coded 
from
  datalake_47618.order_proc t1,
  datalake_47618.encounter t2, 
  datalake_47618.dep_map t3 
where 
  t1.pat_enc_csn_id_coded = t2.pat_enc_csn_id_coded
  and t1.ordering_date_jittered < '2016-07-01'
  and t1.ordering_date_jittered >= '2016-01-01'
  and lower(t1.description) like '%referral%'
  and t2.department_id = t3.department_id
  and t3.specialty = 'Primary Care'
;
'''

# df = pd.read_csv('data/pat_enc_primary2other.csv')
# print df.shape
# print df.head()
#
# df = df.drop_duplicates()
# df.to_csv('data/pat_enc_primary2other.csv', index=False)

'''
Scenario: upon consultation
How does t1.description map to t3.specialty? 
'''

'''
(1) How many order_proc descriptions are there?
select 
    description
from 
    datalake_47618.order_proc t1
where
    t1.ordering_date_jittered < '2016-07-01'
    and t1.ordering_date_jittered >= '2016-01-01'
;
'''

# df = pd.read_csv('data/all_orderProc_descriptions_firstHalf2016.csv')
# print df.shape
#
# from collections import Counter
# cnter = Counter(df['description'].values.tolist())
# df_counter = pd.DataFrame.from_dict(cnter, orient='index').reset_index().rename(columns={0:'cnt'}).sort_values('cnt', ascending=False)
# print df_counter.head()
# df_counter.to_csv('data/counter_all_orderProc_descriptions_firstHalf2016.csv', index=False)

'''
(2) How many order_proc descriptions (that contains "referral") are there?
'''
# df = pd.read_csv('data/counter_all_orderProc_descriptions_firstHalf2016.csv')
# df_referral = df[df['index'].str.contains('REFERRAL')]
# print df_referral
# df_referral.rename(columns={'index':'description'}).to_csv('data/counter_all_referrals_descriptions_firstHalf2016.csv')

'''
(3) How many departments are there?
'''
# df = pd.read_csv('data/dep_map.csv')
# df['specialty'].drop_duplicates().to_csv('data/deduplicated_specialties.csv', index=False)

'''
(4) Mapping referrals and specialties 
'''
# from editdistance import distance
# df_referral = pd.read_csv('data/counter_all_referrals_descriptions_firstHalf2016.csv')
# referrals = df_referral['description'].values.tolist()
# print 'numbers of unique referrals: ', len(referrals)
#
# df_specialty = pd.read_csv('data/deduplicated_specialties.csv').rename(columns={'Unnamed: 0':'specialty'})
# specialties = df_specialty['specialty'].values.tolist()
# print 'number of unique specialties: ', len(specialties)
#
# all_dists = {}
# all_res = []
# for referral in referrals:
#     referral_cleaned = referral.replace("REFERRAL TO ", "").lower()
#     cur_dists = {}
#     for specialty in specialties:
#         specialty_cleaned = specialty.lower()
#         cur_dists[specialty] = distance(referral_cleaned, specialty_cleaned)/float(len(specialty_cleaned))
#
#     top_10_mapped = sorted(cur_dists.items(), key=lambda (k,v):v)[:10]
#     all_dists[referral] = top_10_mapped
#     all_res.append([referral] + top_10_mapped)
#
# df_mapping = pd.DataFrame(all_res, columns=['referral']+[str(x+1) for x in range(10)])
# df_mapping.to_csv('data/map_referral_to_specialties.csv', index=False)


'''
Next step: write trustable mapping into the database, 
and then...
'''



'''
Helping table: icd10 mapping
'''
# from medinfo.db import DBUtil
# columns = ('icd10', 'short_description', 'icd10_code')
#
# query_str = "select %s, %s, %s " \
#             "from stride_icd10_cm " \
#
#
# db_cursor = DBUtil.connection().cursor()
# db_cursor.execute(query_str % columns)
#
# all_rows = db_cursor.fetchall()
# df_icd10_mapping = pd.DataFrame(all_rows, columns=columns)
# df_icd10_mapping.to_csv('data/icd10_mapping.csv', index=False)
# quit()


'''
Per Jonathan Chen's suggestion 03/18/2019
- what was the Referral Diagnosis/Reason. 
You could guess by seeing what are the Top 10 diagnoses at 
the referring visit that entered the referral order.

select 
    t1.description, t2.icd9, count(t1.pat_enc_csn_id_coded) as cnt
from
  datalake_47618.order_proc t1,
  datalake_47618.diagnosis_code t2
where 
  t1.pat_enc_csn_id_coded = t2.pat_enc_csn_id_coded
  and t1.ordering_date_jittered < '2017-01-01'
  and t1.ordering_date_jittered >= '2016-01-01'
  and lower(t1.description) like '%referral%'
group by 
    t1.description, 
    t2.icd9
'''

# df = pd.read_csv('data/JCquestion_20190318/referral_icd10_cnt_2016.csv')
# # description, icd10, cnt
# print df.shape
# all_referrals = df['description'].drop_duplicates().values.tolist()
#
# df_icd10_mapping = pd.read_csv('data/icd10_mapping.csv')
# icd10_mapping_dict = dict(zip(df_icd10_mapping.icd10_code, df_icd10_mapping.short_description))
#
# df['icd10descript'] = df['icd10'].apply(lambda x: icd10_mapping_dict.get(x,'?'))
#
# all_res = []
# for referral in all_referrals:
#     cur_df = df[df['description']==referral]
#
#     cur_icds = cur_df['icd10descript'].values.tolist()
#     cur_cnts = cur_df['cnt'].values.tolist()
#     top_10_pairs = sorted(zip(cur_icds, cur_cnts), key=lambda (icd,cnt):cnt)[::-1][:10]
#
#     all_res.append([referral] + top_10_pairs)
# #all_referrals = df['']
# df_top10_diagnoses = pd.DataFrame(all_res, columns=['referral']+[str(x+1) for x in range(10)])
# print df_top10_diagnoses.head()
# df_top10_diagnoses.to_csv('data/top10_diagnoses.csv', index=False)


'''
- For each Referral to A Specialty Order, look ahead 3 or 6 months, what are the most common New Patient 
Visit departments. That should give a good guess of which referrals lead to which specialty visits Most 
doable with SQL queries, also report conditional prevalence (support and confidence stats) will make it 
easy to filter later.

select 
    p.description, d.specialty, count(e2.pat_enc_csn_id_coded) as cnt
from 
    datalake_47618.order_proc p,
    datalake_47618.encounter e1,
    datalake_47618.encounter e2,
    datalake_47618.dep_map d
where
    lower(p.description) like '%referral%' 
    and p.pat_enc_csn_id_coded = e1.pat_enc_csn_id_coded
    and e1.jc_uid = e2.jc_uid
    and e1.pat_enc_csn_id_coded != e2.pat_enc_csn_id_coded
    and e1.appt_when_jittered <= e2.appt_when_jittered
    and DATE_ADD(date(timestamp(e1.appt_when_jittered)), INTERVAL 3 month) > date(timestamp(e2.appt_when_jittered))
    and e2.department_id = d.department_id
    and e1.appt_when_jittered < '2017-01-01'
    and e1.appt_when_jittered >= '2016-01-01'
group by
    p.description, 
    d.specialty
'''
df = pd.read_csv('data/JCquestion_20190318/referral_specialty_cnt_2016.csv')
print df.head()
all_referrals = df['description'].drop_duplicates().values.tolist()

all_res = []
for referral in all_referrals:
    cur_df = df[df['description']==referral]

    cur_icds = cur_df['specialty'].values.tolist()
    cur_cnts = cur_df['cnt'].values.tolist()
    top_10_pairs = sorted(zip(cur_icds, cur_cnts), key=lambda (icd,cnt):cnt)[::-1][:10]

    all_res.append([referral] + top_10_pairs)

df_top10_specialties = pd.DataFrame(all_res, columns=['specialty']+[str(x+1) for x in range(10)])
print df_top10_specialties.head()
df_top10_specialties.to_csv('data/top10_specialties.csv', index=False)

