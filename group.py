import pandas as pd
import numpy as np

class Group:
    
    def __init__(self, frame=None):
        self.frame = frame
        self.item = ['綠茶（未發酵），每包不超過３公斤', 
                     '綠茶（未發酵），每包超過３公斤', 
                     '其他紅茶（發酵），每包不超過３公斤',
                     '其他紅茶（發酵），每包超過３公斤',
                     '部分發酵茶，每包不超過３公斤',
                     '部分發酵茶，每包超過３公斤']


    def __call__(self, frame):
        self.frame = frame
        return self
    
    def frame_group(self, data):
        
        item = ['進出口別', '中文貨名']
        frame_g = data.groupby(item)
        return frame_g
        
    def get_group(self, sort, dtype):
        
        frame_g = self.frame_group(self.frame)
        
        frame_t = []
        for i in self.item:
            frame_get_g = frame_g.get_group((sort, i))
            # 更改 serise name
            name_item = frame_get_g.groupby(['日期'])[dtype].sum()
            name_item.name = i
            frame_t.append(name_item)
        
        frame_plt = self.frame_fix(frame_t)
        
        return frame_plt
    
    def frame_group_nation(self, data):
        
        item = ['進出口別', '國家']
        frame_n = data.groupby(item)
        return frame_n    
    
    def get_group_nation(self, sort, dtype):
        
        frame_n = self.frame_group_nation(self.frame)
        item_n = list(set(self.frame['國家']))
        
        frame_t = []
        for i in item_n:
            try:
                frame_get_n = frame_n.get_group((sort, i))
                name_nation = frame_get_n.groupby(['日期'])[dtype].sum()
                name_nation.name = i
                frame_t.append(name_nation)
            except:
                pass
        
        frame_plt = self.frame_fix(frame_t)
    
        return frame_plt
    
    def frame_fix(self, data):
        
        # 將多組 series 合併成 Dataframe 
        data_frame = pd.concat(data, axis=1, ignore_index=False)
        
        # 填補為 0
        data_frame.replace(np.nan, 0, inplace = True)
        
        # 依照 Index 排序
        frame = data_frame.sort_index()
        
        return frame
    

        
