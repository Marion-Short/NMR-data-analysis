#!/usr/bin/env python
# coding: utf-8

from TopSpin_to_dataframe import TopSpin_to_dataframe
import pandas as pd
import numpy as np
from Integral_to_conc import Integral_to_conc
import matplotlib.pyplot as plt

# Input experiment code
code = 'MS307'
dataframes = TopSpin_to_dataframe(code) # use TopSpin_to_dataframe to output dictionary of dataframes

# Convert all DataFrame values in the dictionary to float
for key, df in dataframes.items():
    dataframes[key] = df.astype(float)
    
# Access the data frames by their labels
df0 = dataframes['df0']
df1 = dataframes['df1']

# Add column names
df0.columns = ['formate_start', 'acetate_start']
df1.columns = ['formate_end', 'propanoate_end','acetate_end']

# Set row indicies - look to see what you're working with
df0.index = [1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 3.1, 3.2, 4.1, 4.2]
df1.index = [1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 3.1, 3.2, 4.1, 4.2]

# Join dataframes
df2 = pd.concat([df0, df1], axis=1)

df3 = df2.copy()
df3.insert(1, 'propanoate_start', 0)

# Insert a new row at index 1
df3.loc[3.3] = 0
df3.loc[4.3] = 0

# Sort index to align properly
df3 = df3.sort_index()
df3.replace(0, np.nan, inplace=True)

# input dataframe and weight percent of TSP
df10 = Integral_to_conc(df3, 0.75)

# Averages
# create a column for grouping, i.e if the index starts with 1 e.g. 1.1, the column sill contain 1
df11 = df10.copy()
df11['Sample'] = df11.index // 1

# get averages
df_mean = df11.groupby('Sample').mean()
df_stdev = df11.groupby('Sample').std()

# save data in excel spreadsheets
with pd.ExcelWriter(f'{code} NMR data.xlsx') as writer:
    df3.to_excel(writer, sheet_name='Integrals')
    df10.to_excel(writer, sheet_name='Concentrations')
    df_mean.to_excel(writer, sheet_name='Mean')
    df_stdev.to_excel(writer, sheet_name='Stdev')

# Plotting
plt.rcParams["font.family"] = "arial"

x_axis_tick_labels = ['PETC', 'MESNa', 'H-PETC', 'H-MESNa']

# Number of categories
n_categories = len(x_axis_tick_labels)

# Position of bars on x-axis
x = np.arange(n_categories)

# Width of a bar
width = 0.35

fig, ax = plt.subplots(figsize=(4, 4), linewidth=2)

# Plotting the bars
ax.bar(x - width/2, df_mean['acetate_start'], width, yerr=df_stdev['acetate_start'], label='start',
       capsize = 5, linewidth=2, edgecolor='black', color ='cornflowerblue')
ax.bar(x + width/2, df_mean['acetate_end'], width, yerr=df_stdev['acetate_end'], label='end', capsize=5,
      linewidth=2, edgecolor='black', color ='plum')

# Adding labels, title, and custom x-axis tick labels
ax.set_xlabel('Sample', fontsize=14)
ax.set_ylabel('[AcO$^-$] (mM)', fontsize=14)
#ax.set_title('Title')
ax.set_xticks(x)
ax.set_xticklabels(x_axis_tick_labels, fontsize=11)
ax.tick_params(axis='x', width=2)
ax.tick_params(axis='y', direction='out', width=2, labelsize=14, length=5, right=False)
ax.legend(fontsize='large', edgecolor='white', framealpha=0, loc='best')

#Set axis linewidths
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(2)

# create the x-axis for where the points should be positioned (i.e. over the bars)
x_start = x - width/2
x_end = x + width/2
repeated_start = list(np.repeat(x_start, 3))
repeated_end = list(np.repeat(x_end, 3))

# add individual data points
# Plot with customized markers
ax.plot(repeated_start, df10['acetate_start'].tolist(), marker='o',
        linestyle='None', markersize = 4, color = 'black')
ax.plot(repeated_end, df10['acetate_end'].tolist(), marker='o', linestyle='None', markersize = 4, color = 'black')

fig.tight_layout()
#plt.show()

# Save the plot
plt.savefig(f'{code} NMR Acetate.png')
plt.close()

