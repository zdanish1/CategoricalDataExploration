import pandas as pd
import numpy as np
import plotly.plotly as py
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(font_scale=1.5)  
sns.set_style("whitegrid")

######################################################
###################### PART 2 ########################
######################################################

# - 2.1: Code for filtering schools
# - 2.2: Code for healthcare analysis

# 2.1

#Fig 1.2.1 - Filtering using 6-digit NAICS for Schools (returns 39,461 rows)
df_education = data[(data['category_code'].str[:6] == '611110')]
#print df_education.shape

#Step 1.2.2: Filtering the NAICS 611110 data by keywords including 
#'school', 'high', 'academy', 'elementary' and 'charter' (returns 1720 rows)
df_education = df_education[(df_education['name'].str.contains("school", na = False, case = False)) | \
                            (df_education['name'].str.contains("high", na = False, case = False)) | \
                            (df_education['name'].str.contains("elementary", na = False, case = False))|\
                           (df_education['name'].str.contains("academy", na = False, case = False))|\
                           (df_education['name'].str.contains("charter", na = False, case = False))]
#print df_education.shape

# 2.2

#Filtering out all healthcare practices from the dataset without using NAICS
df = data[(data['name'].str.contains(" hospital", na = False, case = False)) | \
    (data['name'].str.contains(" clinic", na = False, case = False)) | \
    (data['name'].str.contains(" DDS", na = False, case = False))|\
    (data['name'].str.contains(" dentist", na = False, case = False))|\
    (data['name'].str.contains(" MD", na = False, case = False))|\
    (data['name'].str.contains(" MBBS", na = False, case = False))|\
    (data['name'].str.contains(" OD", na = False, case = False))|\
    (data['name'].str.contains(" DPM", na = False, case = False))|\
    (data['name'].str.contains(" BDS", na = False, case = False))|\
    (data['name'].str.contains(" DMD", na = False, case = False))|\
    (data['name'].str.contains(" therapist", na = False, case = False))]

df = df[~(df['revenue'].isin(['',' ','0',0,None,'none','null'])| 
          df['state'].isin(['',' ','0',0,None,'none','null'])|
          df['headcount'].isin(['',' ','0',0,None,'none','null'])|
         df['time_in_business'].isin(['',' ','0',0,None,'none','null']))]

def h_type(x):
    if ' hospital' in x.lower():
        return 'Hospital'
    elif ' clinic' in x.lower():
        return 'Clinic'
    return 'Private Practice'
    

##Dictionaries created to convert revenue and headcount to numeric variables:

revenue_dict = {'Less Than $500,000': [250000], '$500,000 to $1 Million': [500000,1000000], \
                '$1 to 2.5 Million': [1000000, 2500000],'$2.5 to 5 Million': [2500000,5000000],\
                '$5 to 10 Million': [5000000,10000000], '$10 to 20 Million': [10000000,20000000],\
                '$20 to 50 Million': [20000000,50000000], '$50 to 100 Million': [50000000,100000000], 
                '$100 to 500 Million': [100000000,500000000], 'Over $500 Million': [500000000,1000000000], 
                'Over $1 Billion': [1000000000]}

headcount_dict = {'1 to 4': [1,4], '10 to 19': [10,19], '100 to 249': [100,249],\
                  '20 to 49':[20,49],'250 to 499': [250,499],'5 to 9': [5,9], \
                  '50 to 99': [50,99], '500 to 999': [500,999], 'Over 1,000':[1000]}

#Creating a type variable by checking parts of string using the h_type function to classify in hospital, clinic and private practice

df['Type'] = df['name'].apply(lambda x: h_type(x))

#Creating a catergory variable which records whether an entry was recorded under the healthcare NAICS code or otherwise

df['health_category'] = df['category_code'].apply(lambda x: 'Healthcare' if x[:2] == '62' else 'Other')

#Creating revenue variables in various forms

df['max_revenue_per_head'] = df.apply(lambda x: float(max(revenue_dict[x['revenue']]))/min(headcount_dict[x['headcount']]), axis=1)

df['min_revenue_per_head'] = df.apply(lambda x: float(min(revenue_dict[x['revenue']]))/max(headcount_dict[x['headcount']]), axis=1)                                             

df['average_revenue'] = df['revenue'].apply(lambda x: np.mean(revenue_dict[x]))

df['min_revenue_per_head_lg'] = np.log10(df['min_revenue_per_head'])

df['average_revenue_lg'] = np.log10(df['average_revenue'])

#Code for Fig 2.2.1 - countplot of healthcare type

f2_2_1 = sns.countplot(x='health_category',data=df, order = 
             ['Healthcare', 'Other'], color = '#a2cffe')
f2_2_1.set(xlabel='NAICS Category', ylabel='Number of Healthcare Records')

#Code for Fig 2.3.1 - percentage plot of time_in_business

dfc = df.copy(deep=True) #this copy is created to add an extra column of 1's to help create a %age bar-graph
dfc['cnt'] = 1
f2_3_1 = sns.barplot(y="time_in_business", x="cnt", data=dfc, estimator=lambda y: sum(y)*100/len(dfc), \
                  order=['1-2 years', '3-5 years', '6-10 years','10+ years'], color = '#90e4c1', orient = 'h')
f2_3_1.set(xlabel="Percent", ylabel="Time in Business")

#Code for Fig 2.3.2 - percentage plot of revenue ranges

f2_3_2 = sns.barplot(y="revenue", x="cnt", data=dfc, estimator=lambda y: sum(y)*100/len(dfc), \
                  order = ['Less Than $500,000', '$500,000 to $1 Million','$1 to 2.5 Million',
              '$2.5 to 5 Million','$5 to 10 Million', '$10 to 20 Million',
                '$20 to 50 Million', '$50 to 100 Million', '$100 to 500 Million', 
              'Over $500 Million','Over $1 Billion'], color = '#ffb07c', orient = 'h')

f2_3_2.set_yticklabels(['< 0.5', '0.5 - 1','1 - 2.5',
              '2.5 - 5','5 - 10', '10 - 20',
                '20 - 50', '50 - 100', '100 - 500', 
              '500 - 1000','> 1000'])
f2_3_2.set(xlabel="Percent", ylabel="Revenue ($ Millions)")

#Code for Fig 2.3.3 & 2.3.4 after slight tweaking (can only be created by a plotly account holder) - US Maps

df_state_type = df[['state','category_code','name','Type','average_revenue']]
df_state_type = pd.get_dummies(df_state_type[['state','Type','average_revenue']], columns=['Type'], prefix='ty')
df_state_type = df_state_type.groupby(['state'], as_index=False)[['ty_Clinic', 'ty_Hospital', 'ty_Private Practice','average_revenue']].sum()
df_state_type['ratio'] = df_state_type['ty_Hospital']/df_state_type['ty_Private Practice'].astype('float')

#The following file is read solely for the purpose of joining state abbreviations to state names

d = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')

for col in df_state_type.columns:
    df_state_type[col] = df_state_type[col].astype(str)

df_state_type['text'] = df_state['state_x'] + '<br>' +\
    'Hospitals: ' + df_state_type['ty_Hospital'] + '<br>' +\
    'Clinic: ' + df_state_type['ty_Clinic'] + '<br>' +\
    'Private Practice: ' + df_state_type['ty_Private Practice']
       
scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]
data1 = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = False,
        locations = df_state_type['code'],
        z = df_state_type['ratio'].astype(float),
        locationmode = 'USA-states',
        text = df_state_type['text'],
        marker = dict(
            line = dict(color = 'rgb(255,255,255)',
                width = 2)),
                  colorbar = dict(title = "Ratio of Hospitals to Private Practice"))]

layout = dict(
        title = 'US Healthcare Services by State<br>(Hover for breakdown by Revenue)',
        geo = dict(scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'))
    
fig = dict( data=data1, layout=layout )
py.iplot( fig, filename='d3-hosp_private' )

#Code for Fig 2.4.1 - violinplot -> time_in_business vs log(average revenue)

f2_4_1 = sns.violinplot(y="time_in_business", x="average_revenue_lg", order = ['1-2 years', '3-5 years',\
                                                                     '6-10 years','10+ years'],\
                    data=df, orient = 'h')
f2_4_1.set(ylabel="Years of Service", xlabel="Revenue (Powers of 10)", title = "Healthcare Services in the US")
f2_4_1

#Code for Fig 2.4.2 - factorplots -> time_in_business vs log(average revenue) for types of healthcare

f2_4_2 = sns.factorplot(x="time_in_business", y="average_revenue_lg", order = ['1-2 years', '3-5 years',\
                                                                     '6-10 years','10+ years'],\
                    data=df, col = 'Type', kind = 'point', col_order=['Hospital', 'Clinic', 'Private Practice'],
                     aspect = 1.5)
f2_4_2.set(ylabel="Revenue (Powers of 10)", xlabel="Time In Business")
f2_4_2

#Code for Fig 2.4.3 - factorplots -> time_in_business vs log(average revenue) for types of healthcare (top 3 states)

f2_4_3 = sns.factorplot(x="time_in_business", y="average_revenue_lg", order = ['1-2 years', '3-5 years',\
                                                                     '6-10 years','10+ years'], hue = 'state',\
                    data=df[(df['state'].isin(['CA','TX','FL']))], col = 'Type', col_order=['Hospital', 'Clinic', 'Private Practice']
                      ,kind = 'point',palette = 'Set2', aspect = 1.5)
f2_4_3.set(ylabel="Revenue (Powers of 10)", xlabel="Time In Business")
f2_4_3

#Code for Fig 2.4.4 - factorplots -> headcount vs log(average revenue) for types of healthcare

f2_4_4 = sns.factorplot(x="headcount", y="average_revenue_lg", order = ['1 to 4','5 to 9','10 to 19',\
                                                             '20 to 49', '50 to 99','100 to 249',\
                                                             '250 to 499','500 to 999','Over 1,000'],\
                    data=df, color = "plum", col = 'Type', kind = 'point', 
                     col_order=['Hospital', 'Clinic', 'Private Practice'], aspect = 1.5)
f2_4_4.set(ylabel="Revenue (Powers of 10)", xlabel="Number of Employees")
f2_4_4.set_xticklabels(['3','7','15','30', '75','175','375','750','1000'])
f2_4_4


#Code for Table 2.5 - factorplots -> headcount vs log(average revenue) for types of healthcare

df_cities = df[['state','city','zip','Type','average_revenue']].copy(deep = True)

df_cities = df_cities[df_cities['state'] == 'CA']

df_cities = pd.get_dummies(df_cities, columns=['Type'], prefix = 'type')

for col in ['type_Clinic', 'type_Hospital', 'type_Private Practice']:
    df_cities['r_'+ col] = df_cities[col]*df_cities['average_revenue']

df_cities = df_cities.groupby(['city'], as_index = False)[['type_Clinic', 'type_Hospital', 'type_Private Practice','r_type_Clinic', 'r_type_Hospital', 'r_type_Private Practice']].sum()

df_cities['Count'] = df_cities[['type_Clinic', 'type_Hospital', 'type_Private Practice']].sum(axis=1)

df_cities['Total Revenue'] = df_cities[['r_type_Clinic', 'r_type_Hospital', 'r_type_Private Practice']].sum(axis=1)

df_cities['Average Revenue'] = df_cities['Total Revenue']/df_cities['Count']

#change 'Total Revenue' to 'Count' or 'Average Revenue' to see the ranking for each (add 1 to index for rank)

df_cities = df_cities.sort_values(by='Total Revenue', ascending=False).reset_index(drop = True) 

print df_cities[df_cities['city'].isin(['SAN FRANCISCO','SAN DIEGO', 'LOS ANGELES'])]


