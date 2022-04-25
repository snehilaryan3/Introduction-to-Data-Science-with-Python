# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 12:37:12 2022

@author: aryan

Assignment 2
For this assignment you'll be looking at 2017 data on immunizations from the CDC. 
Your datafile for this assignment is in assets/NISPUF17.csv. 
A data users guide for this, which you'll need to map the variables in the data to the questions being asked, 
is available at assets/NIS-PUF17-DUG.pdf. 
"""

import pandas as pd
import numpy as np

df =pd.read_csv("NISPUF17.csv")

############QUESTION 1 ###############################

"""Question 1
Write a function called proportion_of_education which returns the proportion of children in the dataset who had a mother with the education levels equal to less than high school (<12), high school (12), more than high school but not a college graduate (>12) and college degree.

This function should return a dictionary in the form of (use the correct numbers, do not round numbers):

    {"less than high school":0.2,
    "high school":0.4,
    "more than high school but not college":0.2,
    "college":0.2}
    
"""

#df =  df["EDUC1"]
#less_high_mask = df == 1
#df.where(less_high_mask, inplace = True)
#df = df.dropna()


def get_count(x):
    df = pd.read_csv("NISPUF17.csv")
    df = df["EDUC1"]
    total = df.shape[0]
    mask = df == x
    df.where(mask, inplace = True)
    df = df.dropna()
    return df.shape[0] / total

def proportion_of_education():
    less_high = get_count(1)
    high = get_count(2)
    more_high  = get_count(3)
    college    = get_count(4)
    prop_edu_moms = {"Less than high school" :less_high, 
                     "high school" : high, 
                     "more than high school but not college" : more_high, 
                     "college" : college}
    return prop_edu_moms


result = proportion_of_education()

###########QUESTION2#####################################
"""Question 2
Let's explore the relationship between being fed breastmilk as a child and getting a seasonal influenza vaccine 
from a healthcare provider. 
Return a tuple of the average number of influenza vaccines for those children we know received breastmilk 
as a child and those who know did not.

This function should return a tuple in the form (use the correct numbers:

(2.5, 0.1)
"""




df_bf_inf = df[["CBF_01", "P_NUMFLU"]]
#df_bf_inf["CBF_01"].unique()
#df_bf_inf["P_NUMFLU"].unique()
df_bf_inf = df_bf_inf[df_bf_inf["P_NUMFLU"].notna()]

mask_bf = df["CBF_01"] == 1
df_bf = df_bf_inf.where(mask_bf, inplace = False)
df_bf = df_bf[df_bf["CBF_01"].notna()]

mask_nbf = df["CBF_01"] == 2
df_nbf = df_bf_inf.where(mask_nbf, inplace = False)
df_nbf = df_nbf[df_nbf["CBF_01"].notna()]

result = (df_bf["P_NUMFLU"].mean(), df_nbf["P_NUMFLU"].mean())




df_bf_inf.where(mask_bf, inplace = True)
df_bf_inf = df_bf_inf[df_bf_inf["CBF_01"].notna()]
total = df_bf_inf.shape[0]
sum_bf = df_bf_inf["P_NUMFLU"].sum()
avg_bf = sum_bf/total 

def average_influenza_doses():
    df_bf_inf = df[["CBF_01", "P_NUMFLU"]]

    df_bf_inf = df_bf_inf[df_bf_inf["P_NUMFLU"].notna()]

    mask_bf = df["CBF_01"] == 1
    df_bf = df_bf_inf.where(mask_bf, inplace = False)
    df_bf = df_bf[df_bf["CBF_01"].notna()]

    mask_nbf = df["CBF_01"] == 2
    df_nbf = df_bf_inf.where(mask_nbf, inplace = False)
    df_nbf = df_nbf[df_nbf["CBF_01"].notna()]

    result = (df_bf["P_NUMFLU"].mean(), df_nbf["P_NUMFLU"].mean())
    return result

###################################################################################################################################################
"""
Question 3
It would be interesting to see if there is any evidence of a link between vaccine effectiveness and sex of the child. 
Calculate the ratio of the number of children who contracted chickenpox but were vaccinated against it (at least one varicella dose) 
versus those who were vaccinated but did not contract chicken pox. Return results by sex.

This function should return a dictionary in the form of (use the correct numbers):

    {"male":0.2,
    "female":0.4}    
"""

df_cp_sex = df[["SEX","P_NUMVRC","HAD_CPOX"]]
mask_vax = df_cp_sex["P_NUMVRC"] > 0
df_cp_sex.where(mask_vax, inplace = True)
df_cp_sex = df_cp_sex[df_cp_sex["P_NUMVRC"].notna()] 
df_cp_sex.drop("P_NUMVRC", axis = 1, inplace = True);

mask_cp = df_cp_sex["HAD_CPOX"]== 1
df_cp = df_cp_sex.where(mask_cp, inplace = False)
df_cp = df_cp[df_cp["HAD_CPOX"].notna()]

mask_ncp = df_cp_sex["HAD_CPOX"]== 2
df_ncp = df_cp_sex.where(mask_ncp, inplace = False)
df_ncp = df_ncp[df_ncp["HAD_CPOX"].notna()]

ar_cp = df_cp.to_numpy()
ar_ncp = df_ncp.to_numpy()

##male calculation

cnt_male_cp = 0
for i in range (0, ar_cp.shape[0]):
    if(ar_cp[i, 0] == 1):
        cnt_male_cp = cnt_male_cp + 1

cnt_female_cp = ar_cp.shape[0] - cnt_male_cp

cnt_male_ncp = 0
for i in range (0, ar_ncp.shape[0]):
    if(ar_ncp[i, 0] == 1):
        cnt_male_ncp = cnt_male_ncp + 1
        
cnt_female_ncp = ar_ncp.shape[0] - cnt_male_ncp

result = {"male" : cnt_male_cp/cnt_male_ncp,
          "female" : cnt_female_cp/cnt_female_ncp}



########################################################################################################
import scipy.stats as stats
import numpy as np
import pandas as pd

df_corr =df[["P_NUMVRC","HAD_CPOX"]]

        # this is just an example dataframe
df_corr=pd.DataFrame({"had_chickenpox_column":df["HAD_CPOX"],
                       "num_chickenpox_vaccine_column":df["P_NUMVRC"]})

mask_cp = (df_corr["had_chickenpox_column"] == 1) |(df_corr["had_chickenpox_column"] == 2)
df_corr.where(mask_cp, inplace = True)
df_corr = df_corr[df_corr["had_chickenpox_column"].notna()]
df_corr = df_corr[df_corr["num_chickenpox_vaccine_column"].notna()]



        # here is some stub code to actually run the correlation
corr, pval=stats.pearsonr(df_corr["had_chickenpox_column"],df_corr["num_chickenpox_vaccine_column"])




       








    


    










   
    