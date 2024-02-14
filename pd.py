import numpy as np
import pandas as pd
# Pandas Series

labels = ['a','b','c']
my_data = [10,20,30]
arr = np.array(my_data)
d = {'a':10,'b':20,'c':30}

pd.Series(data = my_data)
pd.Series(data = my_data, index=labels)
pd.Series(d)

#part 1 -> Data Frames
from numpy.random import randn
np.random.seed(101)

df = pd.DataFrame(randn(5,4),['A','B','C','D','E'], ['W','X','Y','Z'])
print(df)
#Data frames is combination of Series
df['W']
#Extract Data frames from the dataframe
df[['W','X']]

# Add in new columns
df['A'] = df['W'] + df['X']
df             
#to get the data from particular row and column             
df.loc['B', 'Y']
df.loc[['A', 'B'], ['W','Y']]


# part 2 - >conditional selection of Data frames
bool_df = df > 0
bool_df
df[df>0] # not common
# generally it is (give me all the values in colum W where the it is greater then 0)
df[df['W']>0]
df[df['Z']<0]

# so with multiple conditions we dont use 'and' but use & as 'and' operator is only for True and False
# for data frames use & (and), |(or) operator 
True and  False
df[(df['W']>0) & (df['Y']>1)]
df[(df['W']>0) | (df['Y']>1)]

# part 3 -> Data frames index hierarchy
# Index Levels
outside = ['G1','G1','G1','G2','G2','G2']
inside = [1,2,3,1,2,3]
hier_index = list(zip(outside,inside))
hier_index = pd.MultiIndex.from_tuples(hier_index)
df = pd.DataFrame(randn(6,2), hier_index, ['A', 'B'])
df
df.loc['G1']

# Missing Data in Pandas 
#dictionaries 
d = {'A' :[1,2,np.nan], 'B' :[5,np.nan,np.nan],'C' :[1,2,3]}
df = pd.DataFrame(d);

df.dropna()
#fillna method allows you to fill the NA values
#you can call any statistical function
df['A'].fillna(value=df['A'].mean())

#GroupBy
# Create dataframe
data = {'Company':['GOOG','GOOG','MSFT','MSFT','FB','FB'],
       'Person':['Sam','Charlie','Amy','Vanessa','Carl','Sarah'],
       'Sales':[200,120,340,124,243,350]}
df = pd.DataFrame(data)
df
byComp = df.groupby('Company')
byComp.sum()
byComp.std()

#Merging, Jonining & Concatenating

#Operations for Panda
df = pd.DataFrame({'col1':[1,2,3,4],'col2':[444,555,666,444],'col3':['abc','def','ghi','xyz']})
df.head()
df
#important function here is apply
df['col2'].apply(lambda x : x*2)

#sorting the data frame
df.sort_values('col2')

# Data Input and output Pands can write to csv,excel,html,sql
df = pd.read_csv('example')
df


