#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

class M123File(object):

    def __init__(self, file_path, column_list, sep=",", header=None):
        self.mfile = pd.read_csv(file_path, sep, header)
        self.mfile.columns = column_list

    def dropColumns(self, column_list):
        self.mfile = self.mfile.drop(columns = column_list)

    def getColumns(self):
        return self.mfile.columns
        

