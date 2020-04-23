#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Les Warren @warre112
ABE65100 Tutorial
Created on Wed Apr 22 21:45:09 2020

This script is designed to go along with Tutorial #1: Using Excel with Python and
Pandas
"""
import pandas as pd

excel_file = 'movies.xls'
movies = pd.read_excel(excel_file)

movies.head()

movies_sheet1= pd.read_excel(excel_file, sheetname=0, index_col=0)
movies_sheet1.head()
#remember sheet # always starts at 0
movies_sheet2= pd.read_excel(excel_file, sheetname=1, index_col=0)
movies_sheet3= pd.read_excel(excel_file, sheetname=2, index_col=0)

movies= pd.concat([movies_sheet1, movies_sheet2, movies_sheet3])

sorted_by_gross= movies.sort_values(['Gross Earnings'], ascending= False)

import matplotlib.plyplot as plt

sorted_by_gross['Gross Earnings'].head(10).plot(kind="barh")
plt.show

movies.describe()

movies_skip_rows = pd.read_excel("movies-no-header-skip-rows.xls", header=None, skiprows=4)
movies_skip_rows.head(5)

movies_subset_columns = pd.read_excel(excel_file, parse_cols=6)
movies_subset_columns.head()

#Pivot Table
movies_subset = movies[['Year', 'Gross Earnings']]
movies_subset.head()

earnings_by_year = movies_subset.pivot_table(index=['Year'])
earnings_by_year.head()

movies.to_excel('output.xlsx')

writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
movies.to_excel(writer, index=False, sheet_name='report')
workbook = writer.bookworksheet = writer.sheets['report']
writer.save()