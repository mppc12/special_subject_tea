import json
import pandas as pd

class Teaproduction:
    
    def __init__(self):
        pass
    
    def production(self):
        
        frame_f = self.production_1()
        frame_e = self.production_2()
        
        frame = pd.concat([frame_f , frame_e])
        frame.columns = ['生產重量']
        frame.index.name = '日期'
        
        return frame
    
    def production_1(self):
        
        # 處理 2003到2010年的茶葉產量，使用pandas開啟 excel
        year = ['2003','2004','2005','2006','2007','2008','2009','2010']
        tea ={}
        for i in range(2,10):
            df = pd.read_excel('9{:d}年.xls'.format(i))
            tea[year[i-2]]=float(df['Unnamed: 6'][8])
        
        frame = pd.DataFrame.from_dict(tea, orient='index')
        
        return frame
        
    def production_2(self):
        
        # 處理 2011 到2019的茶葉產量
        with open('DataFileService.json', encoding='utf8') as jsonfile:
            
            data = json.load(jsonfile)
        
        frame = pd.DataFrame(data)
        frame.replace({'-':0}, inplace = True)
        frame_g_t = frame.groupby(['特用作物類別']).get_group('茶葉')
        
        # 強制轉換格式 float64
        for i in frame_g_t.columns[3:7]:
            frame_g_t = frame_g_t.astype({i:'float64'})
        
        frame_n = frame_g_t.groupby(['年度'])
        frame_t = []
        list_year = list(set(frame['年度']))
        list_year.sort(reverse = False)
        for i in list_year:
            frame_s = frame_n.get_group(i)['產量'].sum()
            frame_t.append(frame_s)
        
        frame_e = pd.DataFrame(frame_t, index=list_year)
        
        return frame_e
