#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 12:48:38 2019

@author: anna
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

#%% MMSI NUMBERS COVERING THE ROUTE BCN-BALEARS
mmsi_i = [209042000, 224637000, 247230200, 209462000, 224882000, 209115000, 225423000 ,209293000] #see pg 29 noteebook   
title = ['Ciudad de Palma', 'Martin i Soler', 'Tenacia', 'Hypatia de Alejandria','Ciudad de Mahon','Sicilia','Volcan de Tinamar','Rosalind Franklin']

#%% lat-lon barcelona, palma, maó, alcúdia eivissa
lon = [2.15,2.650544,4.26583,3.12138,1.43296]
lat = [41.39,39.571625,39.88853,39.85316,38.90883]

#%% READ FILES
#m_f = pd.read_csv('./out/filtered_messages.csv',sep=",", usecols = ['month', 'day', 'hour','minute','second_received','second_sent','mmsi','lon','lat'])
m_b = pd.read_csv('./out/m123_badtstamp.csv',sep=",", usecols = ['month', 'day', 'hour','minute','second_received','second_sent','mmsi','lon','lat'])
m_all = pd.read_csv('./out/m123_clean.csv',sep=",", usecols = ['month', 'day', 'hour','minute','second_received','second_sent','mmsi','lon','lat'])

#%% getting m123 messages of mmsi_i
m123_n = pd.DataFrame()
m123_b = m123_n

for num in mmsi_i:
#    aux = np.where(m_f.mmsi == num)
#    m123_aux = m_f[m_f.index.isin(aux[0])]
    aux = np.where(m_all.mmsi == num)
    m123_aux = m_all[m_all.index.isin(aux[0])]
    m123_n = m123_n.append(m123_aux) 
    
    aux = np.where(m_b.mmsi == num)
    m123_aux = m_b[m_b.index.isin(aux[0])]
    m123_b = m123_b.append(m123_aux) 

#%% entire basemap
fig, ax = plt.subplots(figsize=(10,6))

m = Basemap(projection='merc', lat_0=40.5, lon_0= 2.5, resolution = 'l', area_thresh = 1000.0, llcrnrlon=0.9, llcrnrlat=38.5, urcrnrlon=5.0, urcrnrlat=41.5)    

plt.figure(1) 
m.drawparallels(np.arange(38., 41.5, 0.5), labels=[1,0,0,0], fontsize=7)
m.drawmeridians(np.arange(0.9, 5., 0.5), labels=[0,0,0,1], fontsize=7)
m.drawcoastlines()
m.drawcountries()
    
lon, lat = m(lon, lat)
m.plot(lon,lat,'o', markersize=10, color='deeppink')

a, b = m(np.array(m123_n.lon), np.array(m123_n.lat))
plt.scatter(a,b, s = 100, c = m123_n.mmsi, marker = '+')

plt.savefig('./out/figures/bcn_palma.png')

#%% basemaps according to ships
i = 0
j = 2
for num in mmsi_i:
    fig, ax = plt.subplots(figsize=(10,6))
    plt.figure(j)
    m.drawparallels(np.arange(38., 41.5, 0.5), labels=[1,0,0,0], fontsize=7)
    m.drawmeridians(np.arange(0.9, 5., 0.5), labels=[0,0,0,1], fontsize=7)
    m.drawcoastlines()
    m.drawcountries()
        
    m.plot(lon,lat,'o', markersize=10, color='deeppink')
    
    aux = m123_n.index[(m123_n.mmsi==num)].tolist()
    a, b = m(np.array(m123_n.lon[aux]), np.array(m123_n.lat[aux]))
    s = plt.scatter(a,b, s = 100, c = m123_n.day[aux] ,marker = '+')
    legend1 = ax.legend(*s.legend_elements(),
                    loc="center left",  bbox_to_anchor=(1, 0.5), title="day")
    ax.add_artist(legend1)
    plt.title(title[i],loc = 'center')

    
#    plt.savefig('./out/figures/bcn_palma_'+str(num)+'.png')
    plt.savefig('./out/figures/bcn_palma_'+str(num)+'_all.png')

    i = i+1
    j = j+1




#%% plot lat-lon data

#fig, ax = plt.subplots(figsize=(10,6))
##for category, selection in btime.groupby('shiptype'):
##    ax.plot(btime.lon, btime.lat, marker='o', markersize=5, alpha=0.5, linestyle='', label=category, markeredgewidth=0)
#ax.grid(True)
# 
#scatter = ax.scatter(m123_b.lon, m123_b.lat, s = 100, c = m123_b.mmsi, marker = 'o',   edgecolors='k', alpha = 0.2, vmin= m123_b.mmsi.min(), vmax= m123_b.mmsi.max(), label = m123_b.mmsi)  
#scatter = ax.scatter(m123_n.lon, m123_n.lat, s = 100, c = m123_n.mmsi, marker = '+',  vmin= m123_n.mmsi.min(), vmax= m123_n.mmsi.max(), label = m123_n.mmsi) 
#
##plot barcelona and monte toro coordinates
#bcn  = np.array([2.15, 41.39]) #barcelona
##mt = np.array([4.11, 39.985]) # monte toro
#pm = np.array([2.650544, 39.571625]) #palma mallorca
#mo = np.array([4.26583, 39.88853]) #maó
#al = np.array([3.12138, 39.85316]) #alcúdia
#ei = np.array([1.43296, 38.90883]) #eivissa
#
#ax.scatter(bcn[0], bcn[1], color = 'r', marker = 'o', s = 50)
##ax.scatter(mt[0], mt[1], c = 'r', marker = 'o', s = 50)
#ax.scatter(pm[0], pm[1], color = 'r', marker = 'o', s = 50)
#ax.scatter(mo[0], mo[1], color = 'r', marker = 'o', s = 50)
#ax.scatter(al[0], al[1], color = 'r', marker = 'o', s = 50)
#ax.scatter(ei[0], ei[1], color = 'r', marker = 'o', s = 50)
#
#
## produce a legend with the unique colors from the scatter
#legend1 = ax.legend(*scatter.legend_elements(),
#                    loc="upper right", title="mmsi")
#ax.add_artist(legend1)
#ax.set_xlim((0.7, 5))
#plt.xlabel('longitude')
#plt.ylabel('latitude')
# 
#plt.show()
#    
fig.savefig('./out/figures/bcnpalma.png')
