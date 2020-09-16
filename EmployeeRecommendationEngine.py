# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 11:53:30 2020

@author: Sandesh
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
import re
import regex



def main():
    st.title("EI Maven")
    st.subheader("LinkedIn Employee Recommendation Engine")
    
        
    def file_selector(folder_path='.'):
        filenames = os.listdir(folder_path)
        selected_filename = st.selectbox("Select A file",filenames)
        return os.path.join(folder_path,selected_filename)
    
               
    filename = file_selector()
    st.info("You Selected {}".format(filename))
    
    #Read data
    data = pd.read_excel(filename)
    dataset = data.iloc[:, [1,3,6,8,100,101,129,130,131,132,133]]
    #Handle Duplicates
    df= dataset.drop_duplicates(subset=["Profile url"], keep="last")
        
    #Show Dataset
    if st.checkbox("Show Dataset"):
        number = st.number_input("Number of Rows to View",1,10000000000)
        st.dataframe(df.head(number))
        
    # Show Columns
    if st.sidebar.button("Column Names"):
        st.write(df.columns)
        
    # Show Shape
    if st.sidebar.checkbox("Shape of Dataset"):
        data_dim = st.sidebar.radio("Show Dimension By ",("Rows","Columns"))    
        if data_dim == 'Rows':
            st.text("Number of Rows")
            st.write(df.shape[0])
        elif data_dim == 'Columns':
            st.text("Number of Columns")
            st.write(df.shape[1])
        else:
            st.write(df.shape)  
            
    # Select Columns
    if st.checkbox("Select Columns To Show"):
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect("Select",all_columns)
        new_df = df[selected_columns]
        #st.dataframe(new_df)
        st.table(new_df)
              
        
    #Recommendation
    st.subheader('Recommendation based on scaled weighted experience and qualification score(Priority is given 50% to both)')
    from sklearn.preprocessing import MinMaxScaler
    scaling=MinMaxScaler()
    data_scaled_df=scaling.fit_transform(df[['PRO RATINGS','Education Ratings']])
    data_normalized_df=pd.DataFrame(df,columns=['PRO RATINGS','Education Ratings'])
        
    df[['normalized_experience_rating','normalized_qualification_rating']]= data_normalized_df
    

    
    #Enter Title     
    title = st.text_input("Enter Required Title:","Type Here")
    
    df=df[df['Title'].str.contains(title, na=False, flags=re.IGNORECASE, regex=True)]
    df['score'] = df['normalized_experience_rating'] * 0.5 + df['normalized_qualification_rating'] * 0.5
    dataset_scored_df = df.sort_values(['score'], ascending=False)
    dataset_scored_df[['Full name', 'Profile url', 'Title','Location','Summary_Complete','APPROX YEARS','normalized_experience_rating','normalized_qualification_rating','score']].head(50)
    
    if st.checkbox("Display Search Results"):
        st.table(dataset_scored_df)   
        
    #Candidates with PhD degree
    st.subheader('Candidates with PhD Degree')  
    data_phd=df[df.normalized_qualification_rating==100]
    dataset_phd_scored_df = data_phd.sort_values(['score'], ascending=False)
    dataset_phd_scored_df[['Full name', 'Profile url', 'Title','Location','Summary_Complete','APPROX YEARS','normalized_experience_rating','normalized_qualification_rating','score']].head(50)
    
    if st.checkbox('Display Search Results for Candidates with PhD Degree'):
        st.table(dataset_phd_scored_df)
    
    
    #Candidates with Master's degree
    st.subheader('Candidates with Master\'s Degree')  
    data_masters=df[df.normalized_qualification_rating==75]
    dataset_masters_scored_df = data_masters.sort_values(['score'], ascending=False)
    dataset_masters_scored_df[['Full name', 'Profile url', 'Title','Location','Summary_Complete','APPROX YEARS','normalized_experience_rating','normalized_qualification_rating','score']].head(50)
    
    if st.checkbox('Display Search Results for Candidates with Master\'s Degree'):
        st.table(dataset_masters_scored_df)


    #Candidates with Bachelor's degree
    st.subheader('Candidates with Bachelor\'s Degree')  
    data_bachelors=df[df.normalized_qualification_rating==50]
    dataset_bachelors_scored_df = data_bachelors.sort_values(['score'], ascending=False)
    dataset_bachelors_scored_df[['Full name', 'Profile url', 'Title','Location','Summary_Complete','APPROX YEARS','normalized_experience_rating','normalized_qualification_rating','score']].head(50)
    
    if st.checkbox('Display Search Results for Candidates with Bachelor\'s Degree'):
        st.table(dataset_bachelors_scored_df)    
        
        
    #Candidates with qualification below Bachelor's degree
    st.subheader('Candidates with qualification below Bachelor\'s Degree')  
    data_low=df[df.normalized_qualification_rating<50]
    dataset_low_scored_df = data_low.sort_values(['score'], ascending=False)
    dataset_low_scored_df[['Full name', 'Profile url', 'Title','Location','Summary_Complete','APPROX YEARS','normalized_experience_rating','normalized_qualification_rating','score']].head(50)
    
    if st.checkbox('Display Search Results for Candidates with qualification below Bachelor\'s Degree'):
        st.table(dataset_low_scored_df)


    #Search by Keywords
    keywords_no = st.sidebar.number_input("Enter Required Number of Keywords:",1,10,1)
    keywords=[]
    #print ("Enter the keywords")
    for i in range(keywords_no):
        keyword_list=st.sidebar.text_input('Enter Keyword', i)    
        keywords.append(keyword_list) 
        
    st.text('Keywords Entered:')
    st.write(keywords)
    
    dataset_withoutNAN = df.dropna(axis=0, subset=['Summary_Complete'])
    dataset_withoutNAN["Summary_Complete"]=dataset_withoutNAN["Summary_Complete"].str.casefold()
    
    #OR/AND
    if st.sidebar.checkbox('Filter Candidates'):
        choice=st.sidebar.radio('Filter by:',('ORing','ANDing'))
        if choice=='ORing':
                data_searchkeyword=dataset_withoutNAN[dataset_withoutNAN['Summary_Complete'].str.contains('|'.join(keywords))]
                data_searchkeyword_scored_df = data_searchkeyword.sort_values(['score'], ascending=False)
                data_searchkeyword_scored_df[['Full name', 'Profile url', 'Title','Location','Summary_Complete','APPROX YEARS','normalized_experience_rating','normalized_qualification_rating','score']].head(20)
                st.table(data_searchkeyword_scored_df)
        elif choice=='ANDing':
                base = r'^{}'
                expr = '(?=.*{})'
                base.format(''.join(expr.format(k) for k in keywords))
                data_searchkeyword=dataset_withoutNAN[dataset_withoutNAN['Summary_Complete'].str.contains(base.format(''.join(expr.format(k) for k in keywords)))]
                data_searchkeyword_scored_df = data_searchkeyword.sort_values(['score'], ascending=False)
                data_searchkeyword_scored_df[['Full name', 'Profile url', 'Title','Location','Summary_Complete','APPROX YEARS','normalized_experience_rating','normalized_qualification_rating','score']].head(20)
                st.table(data_searchkeyword_scored_df)
                
    #copyright
    if st.sidebar.button("©2020,Sandesh Shrestha"):
        st.sidebar.balloons()

if __name__=='__main__':
    main()