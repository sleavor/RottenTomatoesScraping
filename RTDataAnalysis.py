# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 18:53:33 2020

@author: Shawn Leavor
"""
#import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def findMaxDiff(aList, df, column):
    
    #Intialize empty list of final values
    final = pd.DataFrame(columns=[column,
                                  'Critic Advantage Title',
                                  'Critic Advantage',
                                  'Audience Advantage Title',
                                  'Audience Advantage'])
    
    #Delete null values for the category        
    df = df[df[column].notnull()]
    
    for i in aList:
        
        #These names gives trouble, so skip it
        #Using if '?' in i does not work 
        if i == '?zgr Yildirim' or i == '?lonore Faucher':
            continue
        
        #Create dataframe for strings where they can be multiple objections
        if column == 'genre' or column =='director':
            newdf= df[df[column].str.contains(i)]
            
            #Skip if they have less than 5 movies
            if len(newdf) < 5:
                continue
            
        #Create dataframe with matches
        else:
            newdf = df[df[column] == i]
            
            #Skip if they have less than 5 movies
            if len(newdf) < 5:
                continue
        
        #Find and print the max
        criticAd = newdf[newdf['rateDiff'] == newdf['rateDiff'].max()]
        audAd = newdf[newdf['rateDiff'] == newdf['rateDiff'].min()]
        
        #If this is blank, skip to next
        if len(criticAd) == 0:
            continue
        
        #Add biggest & smallest to final list
        final = final.append({
                    column: i, 
                    'Critic Advantage Title': criticAd['title'].values[0], 
                    'Critic Advantage': criticAd['rateDiff'].values[0], 
                    'Audience Advantage Title': audAd['title'].values[0],
                    'Audience Advantage': audAd['rateDiff'].values[0]
                      },
            ignore_index=True)
    
    #return values of biggest and smallest difference for each item  
    return final

def boxPlot(df, alist, acolumn, bcolumn):
    ''' 
    Creates box and whisker plot for inputed data
    
    df - Dataframe for the data you want to plot
    alist - List that you want to sort the df by
    acolumn - Column name that you are looking for alist items in
    bcolumn - Column name that you want to grab the data of
    '''
    
    #Initiate titles and data list
    titles = []
    data = []
    
    #Makes titles for graphs
    if bcolumn == 'rateDiff':
        graph_title = 'Difference in Audience and Critic Rating'
        x_title = 'Difference in Rating \n Positive: Critic Favored - Negative: Audience Favored'
    elif bcolumn == 'audienceRate':
        graph_title = 'Average Audience Rating'
        x_title = 'Audience Rating'
    elif bcolumn == 'criticRate':
        graph_title = 'Average Critic Rating'
        x_title = 'Critic Rating'
    else:
        graph_title = bcolumn
        x_title = bcolumn
        
    #Loop through and add data to final list
    for i in alist:
        
        #Find data with needed variable
        newdf = df[df[acolumn].str.contains(i)]
        
        #Add to titles and data
        titles.append(i.replace('&amp;', 'and'))
        data.append(newdf[bcolumn])
    
    #Create graph
    fig, ax = plt.subplots()
    ax.boxplot(data, vert=0)
    ax.set_yticklabels(titles)
    ax.set_xlabel(x_title)
    plt.title(graph_title + ' by ' + acolumn.title())
    plt.show()

def createTable(df):
    #Below needs to be solved for lack of text wrapping in table
    #Create table
    cell_text = []
    for row in range(len(df)):
        cell_text.append(df.iloc[row])
    
    table = plt.table(cellText=cell_text, colLabels=df.columns.str.title(), loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(20)
    table.scale(3,3)
    plt.axis('off')

#Create dataframe
df = pd.read_csv('RottenTomatoesScrape/rtData.csv', na_values=[''])

#Create dataframe with more than 5 critic reviews and 200 audience reviews
#Should we do greater than 25 critic reviews and 1000 audience reviews?
#Cuts list from 18416 to 8646
df = df[df['numCritReviews'] > 25]
df = df[df['numAudienceReviews'] > 1000]
df.rateDiff.describe()

#Create list of all unique ratings, studios, genres, and directors
ratings = df.rating.unique()
studios = df.studio.unique()
genres = pd.unique(df['genre'].str.split(',', expand=True).stack())
directors = pd.unique(df['director'].str.split(',', expand=True).stack())

# Find the maximum differences for ratings, genres, studios, and directors
ratingDiffs = findMaxDiff(ratings, df, 'rating')
#genreDiffs = findMaxDiff(genres, df, 'genre')
#studioDiffs = findMaxDiff(studios, df, 'studio')
#directorDiffs = findMaxDiff(directors, df, 'director')

#createTable(ratingDiffs)

#Create dummy dataframe to show genres for each movie
genredf = df.set_index('title')['genre'].str.get_dummies(',')
genredf['sums'] = genredf.sum(axis=1)

#Create genre box and whisker plot
gendf = df[df['genre'].notna()]
boxPlot(gendf, genres, 'genre', 'rateDiff')
boxPlot(gendf, genres, 'genre', 'audienceRate')
boxPlot(gendf, genres, 'genre', 'criticRate')

#Get list of directors with 15 or more movies in the dataframe
#15 would leave you with 25 directors
director_counts = df.director.value_counts()
director_list = director_counts[director_counts >= 15].index
director_df = df[df['director'].isin(director_list)]

#Make box plot of most popular directors
boxPlot(director_df, director_list, 'director', 'rateDiff')

boxPlot(director_df, director_list, 'director', 'audienceRate')
boxPlot(director_df, director_list, 'director', 'criticRate')


#Find studios with more than 80 movies (21 entries)
studio_counts = df.studio.value_counts()
studio_list = studio_counts[studio_counts >= 80].index
studio_df = df[df['studio'].isin(studio_list)]

#Plot studios
boxPlot(studio_df, studio_list, 'studio', 'rateDiff')

#Custom Directors Graph
director_list=['David Lynch', 'Christopher Nolan', 'Denis Villeneuve',
               'Paul Thomas Anderson', 'Stanley Kubrick', 'Quentin Tarantino']
director_df = df[df['director'].isin(director_list)]
boxPlot(director_df, director_list, 'director', 'rateDiff')
boxPlot(director_df, director_list, 'director', 'criticRate')
