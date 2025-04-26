import pandas as pd
import os


print("Current working directory:", os.getcwd())

file = os.path.join(os.getcwd(), 'jallatte-1.xlsx')


data = pd.read_excel(file)


print(data['Code'])