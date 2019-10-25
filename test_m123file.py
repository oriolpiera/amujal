import pytest
from m123file import M123File
import pandas as pd

def test_dropColumn():
    mfile = M123File(file_path="testfiles/llista_arx_123.txt",column_list=['date','second_sent','type','mmsi','status','turn', 'speed','lon','lat','course','heading'])
    
    mfile.dropColumn(['type','status'])

    assert (mfile.getColumns() == ['date','second_sent','mmsi','turn', 'speed','lon','lat','course','heading']).all()

