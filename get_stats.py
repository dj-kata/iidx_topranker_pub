#!/usr/bin/python3
#-*-coding:utf-8-*-
# usage: get_stats.py sp/dp
import os, pickle, datetime, sys
import numpy as np
import pandas as pd
#import dp_songdb
import csv

os.environ[ 'HOME' ] = '/home/kata/work/iidx_topranker_pub'

bpl_member = {
    'UCCHIE':'apina',
    'WELLOW':'apina',
    'CHP*1E':'apina',
    'KENTAN':'apina',

    'MIKAMO':'gamepanic',
    'PEACE':'gamepanic',
    'TAKA.S':'gamepanic',
    'FRIP':'gamepanic',

    'CORIVE':'gigo',
    'NCHO72':'gigo',
    'NUCHIO':'gigo',
    'CYBERX':'gigo',
    'LOOT':'gigo',

    '1-PIN':'leisureland',
    'DINASO':'leisureland',
    'G*':'leisureland',
    'U76NER':'leisureland',

    'U*TAKA':'round1',
    'KUREI':'round1',
    'I6VV':'round1',
    'NAGACH':'round1',

    'SEIRYU':'silkhat',
    'VELVET':'silkhat',
    'LICHT':'silkhat',
    'KIDO.':'silkhat',

    'TATSU':'supernova',
    'NIKE.':'supernova',
    'TAKWAN':'supernova',
    '46':'supernova',
    'MOMOI':'supernova',

    'KKM*':'taito',
    'RIOO':'taito',
    'RIOO*':'taito',
    '8S.':'taito',
    'RAITO.':'taito',
}

def read_tsv(filename):
    with open(filename, mode='r', encoding='utf-8') as f:
        tsv_reader = csv.reader(f, delimiter='\t')
        read_data  = [row for row in tsv_reader]
    tmp = {}
    for d in read_data:
        title = d[0]
        dat = d[1:]
        dat[0] = int(dat[0])
        for i in range(len(dat)):
            if dat[i] == "False":
                dat[i] = False
            else:
                try:
                    dat[i] = int(dat[i])
                except ValueError:
                    pass
        tmp[title] = dat
    return tmp

def set_date(filename):
    tmp = datetime.datetime.now()
    date = f"{tmp.year-2000}/{tmp.month}/{tmp.day}"
    base = 'convert -font /usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf -pointsize 26 -fill black'
    draw_0 = f' -draw " text 32,1000'
    text = f"'{date}'"
    draw_1 = f'" {filename} {filename}'
    os.system(base+draw_0+text+draw_1)

def gen_graph(data, mode, st, ed, outfile): # data:DataFrame,  mode:'sp/dp',  st,ed:1開始で順位の範囲を指定
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    font_path = "/usr/share/fonts/truetype/migmix/migmix-1p-regular.ttf"
    font_path = "/usr/share/fonts/truetype/ricty-diminished/RictyDiminished-Regular.ttf"
    font_prop = FontProperties(fname=font_path)
    matplotlib.rcParams["font.family"] = font_prop.get_name()

    # データ準備
    df_bar = data.sort_values(by='total',ascending=True).iloc[:,0:5]
    df_total = data.sort_values(by='total',ascending=True)['total']
    XLIM_MAX = df_total[-1] + 35 # 横軸の最大値
    INTERVAL = 50*int((XLIM_MAX // 4)//50) # 横軸の間隔 (SPなら50、DPなら100)
    ## stが1の時は特殊ケースなのでここで分岐しておく
    if st == 1:
        players      = list(df_total.index[-ed:]) # ランカー一覧
        bar_target   = df_bar[-ed:]
        total_target = df_total[-ed:]
    else:
        players      = list(df_total.index[-ed:1-st]) # ランカー一覧
        bar_target  = df_bar[-ed:1-st]
        total_target = df_total[-ed:1-st]

    # グラフ作成
    fig,ax = plt.subplots(figsize=(10,10))
    bar_target.plot(kind='barh', stacked=True, ax=ax, mark_right=False, fontsize=24)
    ax.legend(loc='lower right', fontsize=20)
    ax.set_title(f'IIDX {mode.upper()} 全1保持数 (TOP{st}-{ed})',fontsize=32)

    # bar右側に合計を埋め込む
    ret = data.sort_values(by='total',ascending=True)
    for n in bar_target:
        for i,tot in enumerate(total_target):
            plt.text(tot, i, str(tot), va='center', fontsize=20)

    # 各レベルの数字を埋め込む
    for rect in ax.patches:
        if rect.get_height() > 0:
            cx = rect.get_x() + rect.get_width() / 2
            cy = rect.get_y() + rect.get_height() / 2
            value = f"{rect.get_width():.0f}"
            if int(value)/INTERVAL >= 0.2:
                ax.text(cx, cy, value, color="w", ha="center", va="center", fontsize=18, fontweight="bold")

    plt.xlim([0,XLIM_MAX])
    plt.xticks(np.arange(0,XLIM_MAX, INTERVAL))
    plt.tight_layout()
    fig.subplots_adjust(left=0.15)
    plt.savefig(outfile)
    set_date(outfile)

    # アイコン埋め込み用
    players.reverse()

    for i,pl in enumerate(players):
        if pl in bpl_member:
            xx = 5 + 16*(6-len(pl))
            yy = 65+int(44.6*i)
            os.system(f'composite -geometry +{xx}+{yy} -compose over team_icon/{bpl_member[pl]}.png {outfile} {outfile}')

def get_alldata(mode='sp'):
    if mode == 'sp':
        scorefile = '/home/kata/iidx_topranker/score.pkl'
    elif mode == 'dp':
        scorefile = '/home/kata/iidx_topranker/dp/score.pkl'
    with open(scorefile, 'rb') as f:
        score = pickle.load(f)
    return score

def search_player(player):
    query = player.upper()
    with open('/home/kata/iidx_topranker/score.pkl', "rb") as f: 
        sp = pickle.load(f)
    with open('/home/kata/iidx_topranker/dp/score.pkl', "rb") as f: 
        dp = pickle.load(f)
    diff=["B","N","H","A","L"]

    cnt = 0
    for k in sp.keys():
        for i,fumen in enumerate(sp[k]):
            if fumen[0] == query:
                print(f"{k}(SP{diff[i]}): {fumen}")
                cnt += 1
    for k in dp.keys():
        for i,fumen in enumerate(dp[k]):
            if fumen[0] == query:
                print(f"{k}(DP{diff[i]}): {fumen}")
                cnt += 1
    print(f"cnt = {cnt}")

def gen_oneside(mode='sp', infile='iidx30.tsv'):
    songs = read_tsv(infile)

    # [曲名, name, score, lv, notes]のリストに変換
    ids = []
    list_zen1 = []
    list_rekidai = []

    for k in songs.keys():
        tmp = songs[k]
        if type(tmp[-2]) != bool:
            pname = tmp[-2]
            if type(tmp[-2]) == int:
                pname = str(tmp[-2])
            if (type(tmp[1]) != bool) and (tmp[1] >= 8): # sp
            #if (type(tmp[1]) != bool):
                list_zen1.append([k, pname, tmp[-1], tmp[1], tmp[3]])
                ids.append(pname)
                list_rekidai.append([k, tmp[5], tmp[6], tmp[1], tmp[3]])

    ids = list(set(ids)) # 重複除去
    ids.sort()

    stat = {}
    for id in ids:
        stat[id] = [0,0,0,0,0,0] # 8,9,10,11,12,total

    # 集計
    for s in list_zen1:
        id = s[1]
        lv = s[3]
        stat[id][lv-8] += 1
        stat[id][-1]   += 1

    out_df = pd.DataFrame(list_zen1, columns=['title', 'id', 'score', 'lv', 'notes'])
    out_df = out_df.set_index('title')
    stat_df = pd.DataFrame(stat.values(), index=stat.keys(), columns=['lv8','lv9', 'lv10', 'lv11', 'lv12', 'total'])
    ret = stat_df.sort_values(by='total',ascending=True)
    for i in range(10):
        if (i*20+1) <= ret.shape[0]:
            gen_graph(stat_df, mode, i*20+1, (i+1)*20, f'{mode}{i}.png')
    return ret

if len(sys.argv) < 2:
    print(f'usage: {sys.argv[0]} sp/dp')
else:
    mode = sys.argv[1]
    infile = 'iidx30.tsv' if mode.lower() == 'sp' else 'iidx30_dp.tsv'
    tmp = gen_oneside(mode, infile)

