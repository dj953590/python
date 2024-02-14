# %%
import seaborn as sb
import numpy as np
import os
# Distribution Plots
# distplot
# jointplot
# pairplot
# rugplot
# kdeplot

tips = sb.load_dataset('tips')
tips.head()
#allows to provide the distribution univariate
# kernel density estimate - kde
sb.displot(tips['total_bill'], kde=True)
#two distribution by default its scattered
sb.jointplot(x='total_bill', y='tip', data=tips)

#pair plot takes all the numerical columns and draws plots
sb.pairplot(tips)
#rugplot shows the density of the bill
sb.rugplot(tips['total_bill'])

# Categorical Data Plots
#  factorplot
#  boxplot
#  violinplot
#  stripplot
#  swarmplot
#  barplot
#  countplot
sb.barplot(x='sex', y='total_bill', data=tips)
# count plot just counts the occurances
sb.countplot(x='sex', data=tips)
# %%
sb.violinplot(x='day', y='total_bill', data=tips)
# %%
sb.stripplot(x='day', y='total_bill', data=tips, jitter=True)
# %%
sb.swarmplot(x='day', y='total_bill', data=tips)
# %%
# Matrix Plots
#Matrix plots allow you to plot data as color-encoded matrices and can also be used to indicate clusters within the data (later in the machine learning section we will learn how to formally cluster data).
flights = sb.load_dataset('flights')
flights.head()
# %%
fc = flights.pivot_table(index='month', columns='year',values='passengers')
sb.heatmap(fc)

#Grids are general types of plots that allow you to map plot types to rows and columns of a grid, this helps you create similar plots separated by features.
# %%
iris = sb.load_dataset('iris')
sb.pairplot(iris)

# Regression Plot

# %%
tips.head()
# %%
sb.lmplot(x='total_bill', y = 'tip', data=tips, hue='sex')
# %%
