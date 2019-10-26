import pytest
from m123file import M123File
import pandas as pd
import copy

def test_dropColumn():
    mfile = M123File(file_path="testfiles/llista_arx_123.txt",column_list=['date','second_sent','type','mmsi','status','turn', 'speed','lon','lat','course','heading'])
    
    mfile.dropColumns(['type','status'])

    assert (mfile.getColumns() == ['date','second_sent','mmsi','turn', 'speed','lon','lat','course','heading']).all()

def test_cleanColumn_TStamp():
    mfile = M123File(file_path="testfiles/llista_arx_123.txt",column_list=['date','second_sent','type','mmsi','status','turn', 'speed','lon','lat','course','heading'])

    mfile.cleanColumn('second_sent',60)

    assert mfile.toArray() == ['20190930000000', '59', '1', '224324620', '7', '-128.0', '97.0', '2.2663', '41.38423', '66.2', '511']


def test_cleanColumn_Lat():
    mfile = M123File(file_path="testfiles/llista_arx_123.txt",column_list=['date','second_sent','type','mmsi','status','turn', 'speed','lon','lat','course','heading'])

    mfile.cleanColumn('lat',91)

    assert mfile.toArray() == ['20190930000238', '60', '3', '224324620', '7', '-128.0', '97.0', '2.2663', '41.3755', '147.0', '511','20190930000000', '59', '1', '224324620', '7', '-128.0', '97.0', '2.2663', '41.38423', '66.2', '511']


def test_cleanColumn_Lat():
    mfile = M123File(file_path="testfiles/llista_arx_123.txt",column_list=['date','second_sent','type','mmsi','status','turn', 'speed','lon','lat','course','heading'])

    mfile.cleanColumn('lon',181)

    assert mfile.toArray() == ['20190930000238', '60', '3', '224324620', '7', '-128.0', '97.0', '2.2663', '41.3755', '147.0', '511','20190930000000', '59', '1', '224324620', '7', '-128.0', '97.0', '2.2663', '41.38423', '66.2', '511']


#def test_cleanTStamp():
#    mfile = M123File(file_path="testfiles/llista_arx_123.txt",column_list=['date','second_sent','type','mmsi','status','turn', 'speed','lon','lat','course','heading'])
#    print("prova")
#    #print(mfile.toString())
#    #mfile_old = copy.copy(mfile)
#    mfile.cleanTStamp(60)
#    print("resultat")
#    #print(mfile.toString())
#
#    set_diff_df = mfile.compare_dataframes(mfile_old)
#    print(set_diff_df)
#
#    assert False
