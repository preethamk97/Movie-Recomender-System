# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 23:25:37 2018

@author: Preetham
"""
#import libraries
import numpy as np
import pandas as pd 

column_names = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv('u.data', sep='\t', names=column_names)                       #get user data stored in u.data file
df.head()                                                                      #view starting 5 datapoints in u.data

movie_titles = pd.read_csv('Movie_Id_Titles')                                  #read ,get the data syored in movie_id_titles which contains id and name of the movies
movie_titles.head()                                                            #shows starting 5 datapoints of the dataset
 
df = pd.merge(df, movie_titles, on='item_id')                                  #merge the datasets resulting dataset df would have columns from both the datasets
df.head()                                                                      #shows starting 5 datapoints of the dataset

#importing vizualisation libraries
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')

df.groupby('title')['rating'].mean().sort_values(ascending=False).head(10)     #grouping the dataset by attributes mentioned not in ascending order ,showing starting 10 records
df.groupby('title')['rating'].count().sort_values(ascending=False).head(10)    #grouping by id and number of reviews it got

ratings =pd.DataFrame(df.groupby('title')['rating'].mean())                    #calculating the average rating of each movie
ratings.head()                                                                 #showing starting 5 datapoints of the dataframe
ratings['rating_numbers'] = pd.DataFrame(df.groupby('title')['rating'].count())#total rating per mobie
ratings.head()
 
ratings['rating_numbers'].hist(bins=70)                                        #plotting hisyogram on rating numbers 
ratings['rating'].hist(bins=70)                                                #Relationship between the average rating and the actual number of ratings
sns.jointplot(x='rating', y='rating_numbers', data=ratings, alpha=0.5)         #plot rating vs no of rating

#recomemding similar movie
moviemat = df.pivot_table(index='user_id', columns='title', values='rating')   #create a matrix that has the user ids on one access and the movie title on another axis. Each cell will then consist of the rating the user gave to that movie. The NaN values are due to most people not having seen most of the movies.
moviemat.head()
ratings.sort_values('rating_numbers', ascending=False).head(10)                #most rated movies with ratings

# choosing two movies for our system: Starwars, a sci-fi movie. And Liar Liar, a comedy.
starwars_user_ratings = moviemat['Star Wars (1977)']
liar_liar_user_ratings =moviemat['Liar Liar (1997)']
starwars_user_ratings.head()

similar_to_starwars = moviemat.corrwith(starwars_user_ratings)                 #correlation of every other movie to that specific user behaviour on the StarWars movie
similar_to_starwars.head()

similar_to_liarliar = moviemat.corrwith(liar_liar_user_ratings)                #correlation of every other movie to that specific user behaviour on the Liar Liar movie
similar_to_liarliar.head()

#remove the NaN values and use a DF instead of Series
corr_starwars = pd.DataFrame(similar_to_starwars, columns=['Correlation'])
corr_starwars.dropna(inplace=True)
corr_starwars.head()


#most likely these movies happen to have been seen only by one person who also happend to rate StarWars 5 stars
corr_starwars.sort_values('Correlation', ascending=False).head(10)

corr_starwars = corr_starwars.join(ratings['rating_numbers'], how='left', lsuffix='_left', rsuffix='_right')         #joining the 'number of ratings' column to our dataframe
corr_starwars.head()
print("recomended movies for star wars:-")
corr_starwars[corr_starwars['rating_numbers']>100].sort_values('Correlation', ascending=False).head()                #setting threshold to no ratings more than 100

#similarly doing the same to liar liar
corr_liarliar = pd.DataFrame(similar_to_liarliar, columns=['Correlation'])
corr_liarliar.dropna(inplace=True)
corr_liarliar.head()

corr_liarliar.sort_values('Correlation', ascending=False).head(10)

corr_liarliar = corr_liarliar.join(ratings['rating_numbers'], how='left',lsuffix='_left', rsuffix='_right')
corr_liarliar.head()
print("recomended movies for liar liar:-")
corr_liarliar[corr_liarliar['rating_numbers']>100].sort_values('Correlation', ascending=False).head()