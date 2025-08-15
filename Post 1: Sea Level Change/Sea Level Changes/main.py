import os
from regression_analysis import regression_analysis
from data_transform import transform
from plotting import build_plots


# clear old data
for filename in os.listdir('.\\Processed Data\\'):
    os.remove(f'.\\Processed Data\\{filename}')

for filename in os.listdir('.\\Results\\'):
    os.remove(f'.\\Results\\{filename}')


# generate new results
transform()

regression_analysis()

build_plots()