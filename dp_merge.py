#!/usr/bin/python3
import pickle, csv

def read_tsv():
    with open('iidx30_dp.tsv', mode='r', encoding='utf-8') as f:
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

def write_tsv(dat):
    out = []
    for s in dat.keys():
        tmp = dat[s]
        tmp.insert(0, s)
        out.append(tmp)

    with open('iidx30_dp.tsv', mode='w', encoding='utf-8') as w:
        tsv_writer = csv.writer(w, delimiter='\t')
        tsv_writer.writerows(out)

dp = read_tsv()
with open('songdb.pkl', 'rb') as f:
    songdb = pickle.load(f)
with open('dp_old.pkl', 'rb') as f:
    dp_old = pickle.load(f)

for k in dp.keys():
    if k in songdb.keys():
        dp[k][1] = songdb[k][0] # lv
        dp[k][2] = songdb[k][1] # notes
        if dp[k][2] == 0:
            dp[k][2] = -1
        print(songdb[k])

for k in dp_old.keys():
    if dp_old[k][3][1] > 0: # 穴譜面のスコアあり
        sch = k+'___DPA'
        if sch in dp.keys():
            dp[sch][5] = dp_old[k][3][0]
            dp[sch][6] = dp_old[k][3][1]
    if dp_old[k][4][1] > 0: # 墓譜面のスコアあり
        sch = k+'___DPL'
        if sch in dp.keys():
            dp[sch][5] = dp_old[k][4][0]
            dp[sch][6] = dp_old[k][4][1]

# write_tsv(dp)