import openpyxl
import pandas as pd

SHEET = "Housing_Price_Data"

FILE = "Housing_Price_Data.xlsx"

wb = openpyxl.load_workbook(FILE, data_only=True)
ws = wb[SHEET]

data = {}
for col in ws.iter_cols(values_only=True):
    data[col[0]] = col[1:]

df = pd.DataFrame(data)
print(df)
