import csv
# import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from frames import Frames
from teaproduction import Teaproduction

# 全區域設定中文
plt.rcParams['font.family'] = 'Microsoft YaHei'
plt.rcParams['font.size'] = 12
    
# 全區域設定顏色
plt.rcParams['axes.facecolor'] = 'lightcyan'
plt.rcParams['savefig.facecolor'] = 'lightcyan'

def opencsv(fn):
    with open(fn) as teafile:
        # 讀取csv資料
        reader = csv.reader(teafile)
        # 轉成 list
        tea_list = list(reader)

    # 先將 list 資料整理存成 pd
    col = tea_list.pop(0)
    data = tea_list
    frame = pd.DataFrame(data, columns=col)
        
    return frame

def clean(frame):

    f = Frames()
    frame = f.cleanups(frame).dropcol()
    frame = f.cleanups(frame).droprow()
    frame = f.cleanups(frame).modifydate()
    frame = f.cleanups(frame).dtypeint()
    frame = f.cleanups(frame).modifyitem()
    
    return frame

# dtype = '進口','出口' item = '重量(公斤)','美元(千元)'   
def groupby_item(frame, dtype, item):    

    frame_f = frame.groupby(['進出口別']).get_group(dtype)
    plt_type = pd.DataFrame(frame_f.groupby(['日期'])[item].sum())
    plt_type.columns = [dtype + '重量']
   
    return plt_type

# dtype = '進口','出口' item = '重量(公斤)','美元(千元)'   
def groupby_product(frame, dtype, item):    
    
    f = Frames()
    plt_type = f.groups(frame).get_group(dtype, item)
    return plt_type

# dtype = '進口','出口' item = '重量(公斤)','美元(千元)'   
def groupby_nation(frame, dtype, item):    
    
    f = Frames()
    plt_type = f.groups(frame).get_group_nation(dtype, item)
    return plt_type

def tea_frame():
    fcsv = '茶葉進出口_20200912103234.csv'
    frame = opencsv(fcsv)
    frame = clean(frame)
    
    return frame

def main_1():
    frame = tea_frame()
    
    plt_import_yield = groupby_item(frame,'進口','重量(公斤)')/1000
    plt_export_yield = groupby_item(frame,'出口','重量(公斤)')/1000
    
    t = Teaproduction()
    plt_production = t.production()
    
    plt.figure(figsize= (10, 6), dpi=300)
    
    # 調整標題跟軸稱
    plt.title("每年總重量(公噸)",size=20)
    plt.xlabel('年份',size=16)
    plt.ylabel('重量(公噸)',size=16)
    plt.ylim(0, 35000)
    plt.yticks([0,5000,10000,15000,20000,25000,30000,35000], 
               ["","5000","10000","15000","20000","25000","30000",""])
    
    plt.plot(plt_import_yield,'b-o', label = '進口重量', alpha=0.8)
    plt.plot(plt_export_yield,'r-v', label = '出口重量', alpha=0.8)
    plt.plot(plt_production, 'g-*', label = '生產重量', alpha=0.8)
    
    plt.legend(fontsize = 'x-small', loc = 'upper left')
    plt.grid()
    plt.show()

def main_2():
    frame = tea_frame()

    plt_import_dollar = groupby_item(frame,'進口','美元(千元)')
    plt_export_dollar = groupby_item(frame,'出口','美元(千元)')
    
    plt.figure(figsize= (10, 6), dpi=300)
    
    # 調整標題跟軸稱
    plt.title("每年總金額(美元)",size=20)
    plt.xlabel('年份',size=16)
    plt.ylabel('美元(千元)',size=16)
    plt.ylim(0, 130000)
    plt.yticks([0,20000,40000,60000,80000,100000,120000,130000], 
            ["","20000","40000","60000","80000","100000","120000",""])
    
    plt.plot(plt_import_dollar,'b-o', label = '進口金額', alpha=0.8)
    plt.plot(plt_export_dollar,'r-v', label = '出口金額', alpha=0.8)
    
    plt.legend(fontsize = 'x-small', loc = 'upper left')
    plt.grid()
    plt.show()
    
def main_3():
    frame = tea_frame()

    plt_import_product = groupby_product(frame,'進口','重量(公斤)')
    plt_export_product = groupby_product(frame,'出口','重量(公斤)')

    item = {'綠茶（未發酵），每包不超過３公斤': ['darkgreen', 'o'], 
            '綠茶（未發酵），每包超過３公斤' : ['green','v'],
            '其他紅茶（發酵），每包不超過３公斤' : ['darkred', '*'],
            '其他紅茶（發酵），每包超過３公斤' : ['red', '^'],
            '部分發酵茶，每包不超過３公斤' : ['blue', 's'],
            '部分發酵茶，每包超過３公斤' : ['royalblue', 'x']}

    plt.figure(figsize= (10, 6), dpi=300)    
    # 調整標題跟軸稱
    plt.title("每年主要茶葉進口重量",size=20)
    plt.xlabel('年份',size=16)
    plt.ylabel('重量(公噸)',size=16)

    frame_y = 0
    for i in item:
        plt.bar(plt_import_product[i].index, 
                plt_import_product[i]/1000, 
                bottom = frame_y, width = 0.5, 
                label=i, color=item[i][0], alpha=0.8)
            
        frame_y += (plt_import_product[i]/1000).copy()
        
        # label 設定
        plt.legend(fontsize = 'x-small', loc = 'upper left')
    
    plt.grid()
    plt.show()
    
    plt.figure(figsize= (10, 6), dpi=300)    
    # 調整標題跟軸稱
    plt.title("每年主要茶葉出口重量",size=20)
    plt.xlabel('年份',size=16)
    plt.ylabel('重量(公噸)',size=16)

    frame_y = 0
    for i in item:
        plt.bar(plt_export_product[i].index, 
                plt_export_product[i]/1000, 
                bottom = frame_y, width = 0.5, 
                label=i, color=item[i][0], alpha=0.8)
            
        frame_y += (plt_export_product[i]/1000).copy()
   
    plt.legend(fontsize = 'x-small', loc = 'upper left')
    plt.grid()
    plt.show()

def main_3_1():
    frame = tea_frame()

    plt_import_product = groupby_product(frame,'進口','美元(千元)')
    plt_export_product = groupby_product(frame,'出口','美元(千元)')

    item = {'綠茶（未發酵），每包不超過３公斤': ['darkgreen', 'o'], 
            '綠茶（未發酵），每包超過３公斤' : ['green','v'],
            '其他紅茶（發酵），每包不超過３公斤' : ['darkred', '*'],
            '其他紅茶（發酵），每包超過３公斤' : ['red', '^'],
            '部分發酵茶，每包不超過３公斤' : ['blue', 's'],
            '部分發酵茶，每包超過３公斤' : ['royalblue', 'x']}

    plt.figure(figsize= (10, 6), dpi=300)    
    # 調整標題跟軸稱
    plt.title("每年主要茶葉進口金額",size=20)
    plt.xlabel('年份',size=16)
    plt.ylabel('美元(千元)',size=16)

    frame_y = 0
    for i in item:
        plt.bar(plt_import_product[i].index, 
                plt_import_product[i], 
                bottom = frame_y, width = 0.5, 
                label=i, color=item[i][0], alpha=0.8)
            
        frame_y += (plt_import_product[i]).copy()
        
        # label 設定
        plt.legend(fontsize = 'x-small', loc = 'upper left')
    
    plt.grid()
    plt.show()
    
    plt.figure(figsize= (10, 6), dpi=300)    
    # 調整標題跟軸稱
    plt.title("每年主要茶葉出口金額",size=20)
    plt.xlabel('年份',size=16)
    plt.ylabel('美元(千元)',size=16)

    frame_y = 0
    for i in item:
        plt.bar(plt_export_product[i].index, 
                plt_export_product[i], 
                bottom = frame_y, width = 0.5, 
                label=i, color=item[i][0], alpha=0.8)
            
        frame_y += (plt_export_product[i]).copy()
   
    plt.legend(fontsize = 'x-small', loc = 'upper left')
    plt.grid()
    plt.show()

def main_4():
    frame = tea_frame()
    
    plt_import_product = groupby_product(frame,'進口','重量(公斤)')
    plt_import_dollar = groupby_product(frame,'進口','美元(千元)') 
    plt_export_product = groupby_product(frame,'出口','重量(公斤)')
    plt_export_dollar = groupby_product(frame,'出口','美元(千元)')     

    item = {'綠茶（未發酵），每包不超過３公斤': ['darkgreen', 'o'], 
            '綠茶（未發酵），每包超過３公斤' : ['green','v'],
            '其他紅茶（發酵），每包不超過３公斤' : ['darkred', '*'],
            '其他紅茶（發酵），每包超過３公斤' : ['red', '^'],
            '部分發酵茶，每包不超過３公斤' : ['blue', 's'],
            '部分發酵茶，每包超過３公斤' : ['royalblue', 'x']}    

    plt.figure(figsize= (10, 6), dpi=300)    
    # 調整標題跟軸稱
    plt.title("每年主要茶葉進口單價",size=20)
    plt.xlabel('年份',size=16)
    plt.ylabel('美元/公斤',size=16)
    
    for i in item:
        plt.plot((plt_import_dollar[i]*1000)/plt_import_product[i],
                 color = item[i][0],
                 marker = item[i][1],
                 linestyle = '--',
                 label = i, alpha = 0.8)

    plt.legend(fontsize = 'x-small', loc = 'upper left')
    plt.grid()
    plt.show()
    
    plt.figure(figsize= (10, 6), dpi=300)    
    # 調整標題跟軸稱
    plt.title("每年主要茶葉出口單價",size=20)
    plt.xlabel('年份',size=16)
    plt.ylabel('美元/公斤',size=16)

    for i in item:
        plt.plot((plt_export_dollar[i]*1000)/plt_export_product[i],
                 color = item[i][0],
                 marker = item[i][1],
                 linestyle = '--',
                 label = i, alpha = 0.8)

    plt.legend(fontsize = 'x-small', loc = 'upper left')
    plt.grid()
    plt.show()

def main_5():
    frame = tea_frame()
    
    plt_import_product = groupby_nation(frame,'進口','重量(公斤)')
    plt_import_dollar = groupby_nation(frame,'進口','美元(千元)') 
    
    item = [['b','o'],['g','v'],['r','^'],
            ['c','s'],['m','*'],['y','p'],
            ['k','x'],['purple','h'],['orange','d'],
            ['gold','.']]
    
    nation = ['越南','斯里蘭卡','日本','印度','印尼',
              '波蘭','肯亞','緬甸','中國大陸','英國']

    plt.figure(figsize= (10, 6), dpi=300)    
    # 調整標題跟軸稱
    plt.title("每年各國茶葉進口重量",size=20)
    plt.xlabel('年份',size=16)
    plt.ylabel('重量(公噸)',size=16)
    
    n = 0
    for i in nation[0:7]:
        plt.plot(plt_import_product[i]/1000,
                 color = item[n][0],
                 marker = item[n][1],
                 linestyle = '--',
                 label = i, alpha = 0.8)
        n += 1

    plt.legend(fontsize = 'x-small', loc = 'upper left')
    plt.grid()
    plt.show()
 
    plt.figure(figsize= (10, 6), dpi=300)    
    # 調整標題跟軸稱
    plt.title("每年各國茶葉進口金額",size=20)
    plt.xlabel('年份',size=16)
    plt.ylabel('美元(千元)',size=16)

    n = 0
    for i in nation[0:7]:

        plt.plot(plt_import_dollar[i],
                 color = item[n][0],
                 marker = item[n][1],
                 linestyle = '--',
                 label = i, alpha = 0.8)
        n += 1

    plt.legend(fontsize = 'x-small', loc = 'upper left')
    plt.grid()
    plt.show()

def main_6():
    frame = tea_frame()
    
    plt_export_product = groupby_nation(frame,'出口','重量(公斤)')
    plt_export_dollar = groupby_nation(frame,'出口','美元(千元)') 
    
    item = [['b','o'],['g','v'],['r','^'],
            ['c','s'],['m','*'],['y','p'],
            ['k','x'],['purple','h'],['orange','d'],
            ['gold','.']]
    
    nation = ['中國大陸','美國','日本','香港','菲律賓',
              '馬來西亞','越南','加拿大','澳大利亞','新加坡']

    plt.figure(figsize= (10, 6), dpi=300)    
    # 調整標題跟軸稱
    plt.title("每年各國茶葉出口重量",size=20)
    plt.xlabel('年份',size=16)
    plt.ylabel('重量(公噸)',size=16)
    
    n = 0
    for i in nation[6:10]:
        plt.plot(plt_export_product[i]/1000,
                 color = item[n][0],
                 marker = item[n][1],
                 linestyle = '--',
                 label = i, alpha = 0.8)
        n += 1

    plt.legend(fontsize = 'x-small', loc = 'upper left')
    plt.grid()
    plt.show()

    
    plt.figure(figsize= (10, 6), dpi=300)    
    # 調整標題跟軸稱
    plt.title("每年各國茶葉出口金額",size=20)
    plt.xlabel('年份',size=16)
    plt.ylabel('美元(千元)',size=16)

    n = 0
    for i in nation[6:10]:

        plt.plot(plt_export_dollar[i],
                  color = item[n][0],
                  marker = item[n][1],
                  linestyle = '--',
                  label = i, alpha = 0.8)
        n += 1

    plt.legend(fontsize = 'x-small', loc = 'upper left')
    plt.grid()
    plt.show()
    
    return plt_export_product
  
def main_7():
    
    frame = tea_frame()
    item = {'綠茶（未發酵），每包不超過３公斤': ['darkgreen', 'o'], 
            '綠茶（未發酵），每包超過３公斤' : ['green','v'],
            '其他紅茶（發酵），每包不超過３公斤' : ['darkred', '*'],
            '其他紅茶（發酵），每包超過３公斤' : ['red', '^'],
            '部分發酵茶，每包不超過３公斤' : ['blue', 's'],
            '部分發酵茶，每包超過３公斤' : ['royalblue', 'x']}
    
    frame_1 = frame.groupby(['進出口別', '國家'])
    
    nation = ['越南','斯里蘭卡','日本','印度','印尼']

    for i in nation:
        frame_1_1 = frame_1.get_group(('進口',i))
        frame_2 = frame_1_1.groupby(['中文貨名'])
        
        plt.figure(figsize= (10, 6), dpi=300)    
        plt.title("{:s}每年茶葉進口重量".format(i),size=20)
        plt.xlabel('年份',size=16)
        plt.ylabel('重量(公噸)',size=16)
        
        for j in item:
            frame_2_2 = frame_2.get_group(j)
            frame_3 = frame_2_2.groupby(['日期'])['重量(公斤)'].sum()
            frame = pd.DataFrame(frame_3)
            # 使用 reindex 自訂義標籤，可以使在 plt 可按照順序排列
            frame = frame.reindex(['2003', '2004', '2005', '2006', '2007',
                                    '2008', '2009', '2010', '2011', '2012',
                                    '2013', '2014', '2015', '2016', '2017',
                                    '2018', '2019'])
            plt.plot(frame/1000,
                     color = item[j][0],
                     marker = item[j][1],
                     linestyle = '--',
                     label = j, alpha = 0.8)
        
        plt.legend(fontsize = 'x-small', loc = 'upper left')
        plt.show()    

def main_8():
    
    frame = tea_frame()
    
    plt_export_product = groupby_nation(frame,'出口','重量(公斤)') 
    a = plt_export_product.loc['2015':'2019'].sum().sort_values(ascending=False)
    frame_n = pd.DataFrame(a, columns=['產量'])
    
    import matplotlib.font_manager as fm
    
    font_path = 'C:\Windows\Fonts\kaiu.ttf'
    font_prop = fm.FontProperties(fname=font_path)
    font_prop.set_style('normal')
    font_prop.set_size('8')   
    
    plt.rcdefaults()
    
    fig, ax = plt.subplots(figsize= (6, 20), dpi=600)
    
    # Example data
    nation = np.array(frame_n.index)
    y_pos = np.arange(len(nation))
    ax.ticklabel_format(style='plain')
    ax.barh(y_pos, frame_n.T.astype(int).values[0]/1000)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(nation, fontproperties=font_prop)
    ax.invert_yaxis()

    plt.show()
    
def main_9():
    
    frame = tea_frame()
    
    frame_t = frame.groupby(['進出口別'])
    frame = frame_t.get_group('進口')
    
    item = {'綠茶（未發酵），每包不超過３公斤': ['darkgreen', 'o'], 
            '綠茶（未發酵），每包超過３公斤' : ['green','v'],
            '其他紅茶（發酵），每包不超過３公斤' : ['darkred', '*'],
            '其他紅茶（發酵），每包超過３公斤' : ['red', '^'],
            '部分發酵茶，每包不超過３公斤' : ['blue', 's'],
            '部分發酵茶，每包超過３公斤' : ['royalblue', 'x']}    
        
    nations = ['越南','斯里蘭卡','日本','印度','印尼']

    for nation in nations:
        
        frame_n = frame.groupby(['國家'])
        frame_n_t = frame_n.get_group(nation)

        plt.figure(figsize= (10, 6), dpi=300)    
        plt.title("{:s}主要茶葉進口單價".format(nation) ,size=20)
        plt.xlabel('茶的種類',size=16)
        plt.ylabel('美元/重量(公斤)',size=16)
        
        for i in item:
            frame_i = frame_n_t.groupby(['中文貨名'])
            frame_i_d = frame_i.get_group(i)['美元(千元)'].sum()
            frame_i_w = frame_i.get_group(i)['重量(公斤)'].sum()

            plt.bar(i, frame_i_d*1000/frame_i_w,
                    width = 0.5, label=i, color=item[i][0], alpha=0.8)

        plt.xticks(['綠茶（未發酵），每包不超過３公斤',
                    '綠茶（未發酵），每包超過３公斤',
                    '其他紅茶（發酵），每包不超過３公斤',
                    '其他紅茶（發酵），每包超過３公斤',
                    '部分發酵茶，每包不超過３公斤',
                    '部分發酵茶，每包超過３公斤'],
                   ['綠茶(小)','綠茶(大)',
                    '紅茶(小)','紅茶(大)',
                    '其他(小)','其他(大)'])
         
        plt.legend(fontsize = 'x-small', loc = 'upper left')
        plt.grid()
        plt.show()
        
def main_10():
    frame = tea_frame()
    frame_t = frame.groupby(['進出口別'])
    
    frame = frame_t.get_group('進口')
    frame_t = frame.groupby(['國家'])

    items = {'綠茶（未發酵），每包不超過３公斤': ['darkgreen', 'o'], 
            '綠茶（未發酵），每包超過３公斤' : ['green','v'],
            '其他紅茶（發酵），每包不超過３公斤' : ['darkred', '*'],
            '其他紅茶（發酵），每包超過３公斤' : ['red', '^'],
            '部分發酵茶，每包不超過３公斤' : ['blue', 's'],
            '部分發酵茶，每包超過３公斤' : ['royalblue', 'x']}    
    
    dates = ['2003','2004','2005','2006','2007','2008','2009','2010',
             '2011','2012','2013','2014','2015','2016','2017','2018',
             '2019']

    nations = ['越南','斯里蘭卡','日本','印度','印尼']
   
    for n in nations:
        frame_n = frame_t.get_group(n)
        frame_n_d = frame_n.groupby(['日期', '中文貨名'])
        
        plt.figure(figsize= (10, 6), dpi=300)    
        plt.title("{:s}主要茶葉進口單價".format(n) ,size=20)
        plt.xlabel('年份',size=16)
        plt.ylabel('美元/重量(公斤)',size=16)
        
        for i in items:
            dw = []
            for d in dates:
                try:
                    we = frame_n_d.get_group((d, i))['重量(公斤)'].sum()
                    da = frame_n_d.get_group((d, i))['美元(千元)'].sum()
                    if we < 80000: da = 0
                    dw.append(da*1000/we)
                except:
                    dw.append(0)
                    print((n, d, i), "無此項目")

            plt.plot(dates, np.array(dw), label=i, 
                     color=items[i][0], marker=items[i][1],
                     linestyle = '--',)
            
        plt.legend(fontsize = 'x-small', loc = 'upper left')
        plt.grid()
        plt.show()

def main_11():
    frame = tea_frame()
    item = {'綠茶（未發酵），每包不超過３公斤': ['darkgreen', 'o'], 
            '綠茶（未發酵），每包超過３公斤' : ['green','v'],
            '其他紅茶（發酵），每包不超過３公斤' : ['darkred', '*'],
            '其他紅茶（發酵），每包超過３公斤' : ['red', '^'],
            '部分發酵茶，每包不超過３公斤' : ['blue', 's'],
            '部分發酵茶，每包超過３公斤' : ['royalblue', 'x']}
    
    frame_1 = frame.groupby(['進出口別', '國家'])
    
    nation = ['中國大陸','美國','日本','香港','菲律賓']
              # '馬來西亞','越南','加拿大','澳大利亞','新加坡']

    for i in nation:
        frame_1_1 = frame_1.get_group(('出口',i))
        frame_2 = frame_1_1.groupby(['中文貨名'])
        
        plt.figure(figsize= (10, 6), dpi=300)    
        plt.title("{:s}每年茶葉出口重量".format(i),size=20)
        plt.xlabel('年份',size=16)
        plt.ylabel('重量(公噸)',size=16)
        plt.ylim(0, 1300)
        
        for j in item:
            frame_2_2 = frame_2.get_group(j)
            frame_3 = frame_2_2.groupby(['日期'])['重量(公斤)'].sum()
            frame = pd.DataFrame(frame_3)
            # 使用 reindex 自訂義標籤，可以使在 plt 可按照順序排列
            frame = frame.reindex(['2003', '2004', '2005', '2006', '2007',
                                    '2008', '2009', '2010', '2011', '2012',
                                    '2013', '2014', '2015', '2016', '2017',
                                    '2018', '2019'])
            plt.plot(frame/1000,
                     color = item[j][0],
                     marker = item[j][1],
                     linestyle = '--',
                     label = j, alpha = 0.8)
        
        plt.legend(fontsize = 'xx-small', loc = 'upper left')
        plt.show()  
    
def main_12():
    frame = tea_frame()
    frame_t = frame.groupby(['進出口別'])
    
    frame = frame_t.get_group('出口')
    frame_t = frame.groupby(['國家'])

    items = {'綠茶（未發酵），每包不超過３公斤': ['darkgreen', 'o'], 
            '綠茶（未發酵），每包超過３公斤' : ['green','v'],
            '其他紅茶（發酵），每包不超過３公斤' : ['darkred', '*'],
            '其他紅茶（發酵），每包超過３公斤' : ['red', '^'],
            '部分發酵茶，每包不超過３公斤' : ['blue', 's'],
            '部分發酵茶，每包超過３公斤' : ['royalblue', 'x']}    
    
    dates = ['2003','2004','2005','2006','2007','2008','2009','2010',
             '2011','2012','2013','2014','2015','2016','2017','2018',
             '2019']

    nations = ['中國大陸','美國','日本','香港','菲律賓']
    # nations = ['馬來西亞','越南','加拿大','澳大利亞','新加坡']
   
    for n in nations:
        frame_n = frame_t.get_group(n)
        frame_n_d = frame_n.groupby(['日期', '中文貨名'])
        
        plt.figure(figsize= (10, 6), dpi=300)    
        plt.title("{:s}主要茶葉出口單價".format(n) ,size=20)
        plt.xlabel('年份',size=16)
        plt.ylabel('美元/重量(公斤)',size=16)
     
        for i in items:
            dw = []
            for d in dates:
                try:
                    
                    we = frame_n_d.get_group((d, i))['重量(公斤)'].sum()
                    da = frame_n_d.get_group((d, i))['美元(千元)'].sum()
                    if we < 1000: da = 0
                    dw.append(da*1000/we)
                    
                except:
                    dw.append(0)
                    print((n, d, i), "無此項目")

            plt.plot(dates, np.array(dw), label=i, 
                     color=items[i][0], marker=items[i][1],
                     linestyle = '--',)
            
        plt.legend(fontsize = 'x-small', loc = 'upper left')
        plt.grid()
        plt.show()    

def main_13():
    
    frame = tea_frame()
    
    frame_t = frame.groupby(['進出口別'])
    frame = frame_t.get_group('出口')
    
    item = {'綠茶（未發酵），每包不超過３公斤': ['darkgreen', 'o'], 
            '綠茶（未發酵），每包超過３公斤' : ['green','v'],
            '其他紅茶（發酵），每包不超過３公斤' : ['darkred', '*'],
            '其他紅茶（發酵），每包超過３公斤' : ['red', '^'],
            '部分發酵茶，每包不超過３公斤' : ['blue', 's'],
            '部分發酵茶，每包超過３公斤' : ['royalblue', 'x']}    
        
    nations = ['中國大陸','美國','日本','香港','菲律賓']

    for nation in nations:
        
        frame_n = frame.groupby(['國家'])
        frame_n_t = frame_n.get_group(nation)

        plt.figure(figsize= (10, 6), dpi=300)    
        plt.title("{:s}主要茶葉出口單價".format(nation) ,size=20)
        plt.xlabel('茶的種類',size=16)
        plt.ylabel('美元/重量(公斤)',size=16)
        
    
        for i in item:
            frame_i = frame_n_t.groupby(['中文貨名'])
            frame_i_d = frame_i.get_group(i)['美元(千元)'].sum()
            frame_i_w = frame_i.get_group(i)['重量(公斤)'].sum()

            plt.bar(i, frame_i_d*1000/frame_i_w,
                    width = 0.5, label=i, color=item[i][0], alpha=0.8)

        plt.xticks(['綠茶（未發酵），每包不超過３公斤',
                    '綠茶（未發酵），每包超過３公斤',
                    '其他紅茶（發酵），每包不超過３公斤',
                    '其他紅茶（發酵），每包超過３公斤',
                    '部分發酵茶，每包不超過３公斤',
                    '部分發酵茶，每包超過３公斤'],
                   ['綠茶(小)','綠茶(大)',
                    '紅茶(小)','紅茶(大)',
                    '其他(小)','其他(大)'])
         
        plt.legend(fontsize = 'x-small', loc = 'upper left')
        plt.grid()
        plt.show()
    
if __name__ == "__main__":
    main_1()
    # main_2()
    # main_3()
    # main_3_1()
    # main_4()
    # main_5()
    # main_6()
    # main_7()
    # main_8()
    # main_9()
    # main_10()
    # main_11()
    # main_12()
    # main_13()
        