#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 10:22:42 2019

@author: anna
"""

import numpy as np
import pandas as pd

arx = 'llista_arx_'


#%% READ FILES
m123 = pd.read_csv('/home/anna/Documents/AIS/python/out/'+arx+'123'+'.txt',sep=",",header=None)
m123.columns =['date','second_sent','type','mmsi','status','turn', 'speed','lon','lat','course','heading']
m123 = m123.drop(columns = ['type','status'])

m5 = pd.read_csv('./out/llista_arx_5.txt',sep=",")
m5.columns =['type','mmsi','shipname', 'shiptype','to_bow','to_stern', 'to_port','to_starboard', 'draught']

tstampS = np.array(m123.second_sent)

idata = len(tstampS)    #initial amount of data

#%% filter messages 123

# messages with tstamp error at the source
ind = np.where(m123.second_sent >= 60)        #bad tstamp

err = len(ind[0])

m123 = m123.drop(m123.index[ind])    #clean bad stamps


#% clean lat lon wrong values
ind = np.where(m123.lat >= 91)          # detect errors in AIS data

err = err + len(ind[0])             #accumulated error

m123 = m123.drop(m123.index[ind])  #clean bad latitude

ind = np.where(m123.lon >= 181)         # detect errors in AIS data 

err = err + len(ind[0])             #accumulated error

m123 = m123.drop(m123.index[ind])  #clean bad latitude

#% Finding lat-long boundaries
lat = np.array(m123.lat)

bounds = [39.3619611, 43.2312167]               #variables pàgina 24

ind = np.where((lat < bounds[0]) | (lat > bounds[1])) 
     
err = err + len(ind[0])             #accumulated error

m123 = m123.drop(m123.index[ind])

lon = np.array(m123.lon)

bounds = [0.152775, 4.8690028]               #variables pàgina 24

ind = np.where((lon < bounds[0]) | (lon > bounds[1]))

err = err + len(ind[0])             #accumulated error

m123 = m123.drop(m123.index[ind])

del(bounds)

m123 = m123.reset_index(drop = True)

#%% split date column into 6 columns
dat = pd.DataFrame(index = range(m123.shape[0]), columns = ['year','month','day','hour','minute','second_received'])
dat= dat.fillna(0)
#date = np.zeros((idata, 6))
aux = m123.date/1e10
dat.year = aux.round(0)

aux = m123.date/1e8 - dat.year*1e2
dat.month = aux.apply(np.floor)

aux = m123.date/1e6 - dat.year*1e4 - dat.month*1e2
dat.day = aux.apply(np.floor)

aux = m123.date/1e4 - dat.year*1e6 - dat.month*1e4 - dat.day*1e2
dat.hour =  aux.apply(np.floor)

aux = m123.date/1e2 - dat.year*1e8 - dat.month*1e6 - dat.day*1e4 - dat.hour*1e2
dat.minute = aux.apply(np.floor)

dat.second_received = m123.date - dat.year*1e10 - dat.month*1e8 - dat.day*1e6 - dat.hour*1e4- dat.minute*1e2

m123 = dat.join(m123, how='outer')
m123 = m123.drop(columns = ['date'])

del (aux,dat)

#%% joining info from messages 123 and messages 5

mmsi = np.unique(m123.mmsi, return_counts = True)
mmsi_m5 = np.unique(m5.mmsi, return_index = True)
shtyp_mmsi = m5[m5.index.isin(mmsi_m5[1])]
shtyp_mmsi = shtyp_mmsi.reset_index(drop=True)

shtyp = np.zeros((len(m123),6))

#m5nf =np.array([], dtype=np.int)       # not found mmsi numbers in m5 messages
m5nf = []

for num in mmsi[0]:
    ind = np.where(m123.mmsi == num)
    aux = np.where(shtyp_mmsi.mmsi == num)
    if len(aux[0]) == 0:
        m5nf.append(num)      
    else:  
        shtyp[ind[0],0] = shtyp_mmsi.shiptype[aux[0]]
        shtyp[ind[0],1] = shtyp_mmsi.to_bow[aux[0]]
        shtyp[ind[0],2] = shtyp_mmsi.to_stern[aux[0]]
        shtyp[ind[0],3] = shtyp_mmsi.to_port[aux[0]]
        shtyp[ind[0],4] = shtyp_mmsi.to_starboard[aux[0]]
        shtyp[ind[0],5] = shtyp_mmsi.draught[aux[0]]
    
    
shtyp = pd.DataFrame(shtyp, columns = ['shiptype','to_bow','to_stern', 'to_port','to_starboard', 'draught'])
m123 = m123.join(shtyp, how='outer')

#%% differences between received and sent timestamp that are not feasable
#tstampR = np.array(m123.second_received) % 100     #received timestamp
#tstampS = np.array(m123.second_sent)         #sent timestamp from ship

t_err = (m123.second_received<m123.second_sent)  #errors when received < sent

t1_err = m123.index[(m123.second_sent-m123.second_received)>1].tolist()   #errors when received > sent +1

m123_b = m123[m123.index.isin(t1_err)]      #bad time stamp messages

aux = m123_b.index[(m123_b.second_received==0)&(m123_b.second_sent==59)].tolist()   #correction of some bad tstamp errors that are not errors
m123_r = m123_b[m123_b.index.isin(aux)]     #recovering messages that have been considered bad in t1_err but are not

m123_g = m123.drop(m123.index[t1_err])  #remove errors when sent > received + 1
m123_g = m123_g.append(m123_r)          #add rows considered errors but not real errors since (m123_b.second_received==0)&(m123_b.second_sent==59)
#m123_g = m123_g.sort_index()          

#% remove good points from m123 bad messages
m123_b = m123_b[~m123_b.index.isin(aux)]

#%% writting the csv
tstamp = pd.DataFrame(np.c_[m123.second_received,m123.second_sent,t_err],columns = ['received','sent','errors'])

export_csv = tstamp.to_csv (r'/home/anna/Documents/AIS/python/out/tstamp.csv', index = True, header=True)


export_csv = m123.to_csv (r'/home/anna/Documents/AIS/python/out/m123_clean.csv', index = True, header=True) # bad tstamps are still in this file

export_csv = m123_g.to_csv(r'/home/anna/Documents/AIS/python/out/filtered_messages.csv', index = True, header=True)

export_csv = m123_b.to_csv (r'/home/anna/Documents/AIS/python/out/m123_badtstamp.csv', index = True, header=True) # bad tstamps are still in this file

