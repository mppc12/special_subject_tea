import pandas as pd
from group import Group


class Frames:
    
    def __init__(self, frame=None):
        self.cleanups = Cleanup()
        self.groups = Group()

class Cleanup:
    
    def __init__(self, frame=None):
        self.frame = frame
 

    def __call__(self, frame):
        self.frame = frame
        return self
    
  
    def dropcol(self):
        column = ['貨品號列', '重量(公噸)', '英文貨名', '數量(限11碼貨品)', '數量單位']
        frame = self.frame.drop(column, axis=1, inplace=False)
        return frame
    
    def droprow(self):
        rowitem = ['普洱茶，每包不超過３公斤',
                   '普洱茶，每包超過３公斤',
                   '茶或馬黛茶之萃取物、精、濃縮物及以茶、馬黛茶之萃取物、精、濃縮物或以茶、馬黛茶為主要成分之調製品']
        frame = self.frame[self.frame['中文貨名'].isin(rowitem) == False]
        return frame

    def modifydate(self):
        rc_to_vi = {'92年':'2003', '93年':'2004', '94年':'2005', '95年':'2006', 
                    '96年':'2007', '97年':'2008', '98年':'2009', '99年':'2010',
                    '100年':'2011', '101年':'2012', '102年':'2013', '103年':'2014', 
                    '104年':'2015', '105年':'2016', '106年':'2017', '107年':'2018', 
                    '108年':'2019'}
        frame = self.frame.replace(rc_to_vi, inplace = False)
        return frame
            
    def dtypeint(self):
        dtypes = ['重量(公斤)', '美元(千元)']
        for i in dtypes:
            self.frame[i] = pd.to_numeric(self.frame[i])
        frame = self.frame
        return frame
    
    def modifyitem(self):
        item = {'其他綠茶（未發酵），每包超過３公斤': '綠茶（未發酵），每包超過３公斤',
                '薰芬綠茶，每包超過３公斤' : '綠茶（未發酵），每包超過３公斤'}
        frame = self.frame.replace(item, inplace = False)
        return frame


