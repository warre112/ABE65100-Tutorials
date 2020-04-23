#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Les Warren @warre112
ABE65100 Tutorial
Created on Thu Apr 23 11:10:39 2020

This script is designed to go along with Tutorial #2: Using SQLite with Python and
Pandas
@author: warre112
"""

import sqlite3
import pandas as pd
from mpl_toolkits.basemap import Basemap


conn = sqlite3.connect("flights.db")

cur = conn.cursor()

cur.execute("select * from airlines limit 5;")

results = cur.fetchall()
print(results)

cur.close()
conn.close()

##Maping Airport
coords = cur.execute("""
select cast(longitude as float),
cast(latitude as float)
from airports;""").fetchall()

m = Basemap(
projection='merc',
llcrnrlat=-80,
urcrnrlat=80,
llcrnrlon=-180,
urcrnrlon=180,
lat_ts=20,
resolution='c')
m.drawcoastlines()
m.drawmapboundary()

x, y = m(
[l[0] for l in coords],
[l[1] for l in coords])
m.scatter(
x,
y,
1, marker='o',
color='red')

##Maping Routes
df = pd.read_sql_query("select * from airlines limit 5;", conn)

routes = pd.read_sql_query("""
select cast(sa.longitude as float) as source_lon,
cast(sa.latitude as float) as source_lat,
cast(da.longitude as float) as dest_lon,
cast(da.latitude as float) as dest_lat
from routes
inner join airports sa on sa.id = routes.source_id
inner join airports da on da.id = routes.dest_id;
""",
conn)

m = Basemap(
projection='merc',
llcrnrlat=-80,
urcrnrlat=80,
llcrnrlon=-180,
urcrnrlon=180,
lat_ts=20,
resolution='c'
)
m.drawcoastlines()

for name, row in routes[:3000].iterrows():
    if abs(row["source_lon"] - row["dest_lon"]) < 90:
# Draw a great circle between source and dest airports.
        m.drawgreatcircle(
                row["source_lon"],
                row["source_lat"],
                row["dest_lon"],
                row["dest_lat"],
                linewidth=1,
                color='b'
                )
##Modifying the DF
cur = conn.cursor()
cur.execute("insert into airlines values (6048, 19846, 'Test flight', '', '', null, null, null, 'Y')")


pd.read_sql_query("select * from airlines where id=19846;", conn)

name = "Test Flight"
cur.execute("insert into airlines values (6049, 19847, {0}, '', '', null, null, null, 'Y')".format(name))
conn.commit()

values = ('USA', 19847)
cur.execute("update airlines set country=? where id=?", values)
conn.commit()

#Creating Tables
pd.read_sql_query("select * from airlines where id=19846;", conn)
pd.read_sql_query("select * from daily_flights;", conn)

from datetime import datetime
df = pd.DataFrame(
[[1, datetime(2016, 9, 29, 0, 0) ,
datetime(2016, 9, 29, 12, 0), 'T1', 1]],
columns=["id", "departure", "arrival", "number", "route_id"])

df.to_sql("daily_flights", conn, if_exists="replace")

#Altering Tables

cur.execute("alter table airlines add column airplanes integer;")
pd.read_sql_query("select * from airlines limit 1;", conn)

df = pd.read_sql("select * from daily_flights", conn)
df["delay_minutes"] = None
df.to_sql("daily_flights", conn, if_exists="replace")


