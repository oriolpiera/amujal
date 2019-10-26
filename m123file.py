#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

class M123File(object):

    def __init__(self, file_path, column_list, sep=",", header=None):
        self.mfile = pd.read_csv(file_path, sep, header)
        self.mfile.columns = column_list

    def dropColumns(self, column_list):
        self.mfile = self.mfile.drop(columns = column_list)

    def getColumns(self):
        return self.mfile.columns

    def cleanTStamp(self, value):
        self.cleanColumn('second_sent', value)

    def cleanColumn(self, column_name, value):
        ind = np.where(self.mfile[column_name] >= value)
        err = len(ind[0])
        self.mfile = self.mfile.drop(self.mfile.index[ind])

    def toArray(self):
        return self.mfile.astype(str).values.flatten().tolist()


#Other section
#
#    def toString(self):
#        return self.mfile.second_sent.to_string(index=4)
#
#    def __str__(self):
#        return self.mfile.to_string()
#
#    def __copy__(self):
#        return self.mfile.copy()
#
#    def compare_dataframes(self, dataframe):
#        return pd.concat([self.mfile, dataframe]).drop_duplicates(keep=False)
