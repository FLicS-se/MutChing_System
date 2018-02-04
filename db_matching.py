import sqlite3
import numpy as np
from operator import itemgetter

# --------------------
# ここから下は関数の定義
# --------------------

# 与えられた酒情報と料理情報を元に [店舗ID, 酒ID, 料理ID, マッチング結果] のリストを返す
def CalculationList(listSakeData, listRyouriData):
    tempListMutchData = []
    tempListMutchData.append(listSakeData[0])
    tempListMutchData.append(listSakeData[1])
    tempListMutchData.append(listRyouriData[1])
    tempListMutchData.append(sum(list(map(abs, np.array(listSakeData[2:]) - np.array(listRyouriData[2:])))).tolist())
    return tempListMutchData

# 与えられた2次元配列のリストに対して，n番目の要素でソートした結果を返す
def SortList(noSortList, n):
    noSortList.sort(key = itemgetter(n, 0))
    return noSortList

# 与えられた2次元配列のリストに対して,上からn番目までのリストを返す
def ListHigherOrder(higherList, n):
    return higherList[:n][:]

# 入力された2次元のリストをタプルに変換
def InListOutTuple(inList):
    outTuple = []
    for i in range(len(inList)):
        outTuple.append(tuple(inList[i][:]))
    return outTuple

# 入力された2次元のタプルをリストに変換
def InTupleOutList(inTuple):
    outList = []
    for i in range(len(inTuple)):
        outList.append(list(inTuple[i][:]))
    return outList

# テーブル削除
def DeleteTable():
    yamadaDb.executescript('''
    DROP TABLE IF EXISTS sample;
    ''')

# テーブル作成
def CreateTable():
    yamadaDb.execute('''
    CREATE TABLE sample(
    StoreID integer not null,
    SakeID integer not null,
    CuisineID integer not null,
    DifferenceTaste integer not null,
    primary key(StoreID, SakeID, CuisineID))''')

# tupleMutchDataをmutchngテーブルに挿入
def InsertTable(table):
    yamadaDb.executemany("insert into sample(StoreID, SakeID, CuisineID, DifferenceTaste) values(?, ?, ?, ?)", tupleMutchData)

# --------------------
# ここまでが関数の定義
# --------------------




# --------------------
# ここから下が実際の計算
# --------------------

# yamada.dbに接続
conn = sqlite3.connect('yamada.db')
yamadaDb = conn.cursor()

# テーブルをタプルとして代入
tupleSakeData = yamadaDb.execute('select * from sakedata').fetchall()
tupleRyouriData = yamadaDb.execute('select * from cuisinedata').fetchall()
tupleLoginData = yamadaDb.execute('select * from login').fetchall()

# tupleSakeDataテーブルの表示
print('tupleSakeData')
print(tupleSakeData)

# tupleRyouriDataテーブルの表示
print('tupleRyouriData')
print(tupleRyouriData)

# tupleLoginDataテーブルの表示
print('tupleLoginData')
print(tupleLoginData)


# タプルのままではデータの変更などが制限されるためタプルをリストへ変換
listSakeData = InTupleOutList(tupleSakeData)
listRyouriData = InTupleOutList(tupleRyouriData)
listLoginData = InTupleOutList(tupleLoginData)


# マッチングの計算
listMutchData = [] # 完成したマッチングテーブルのリストが代入される
for k in range(len(listLoginData)): ###
    for j in range(len(listSakeData)): # 1つのお酒に対する全ての料理のマッチング結果
        listMutchDataAll = [] # 1つのお酒に対する全ての料理のマッチング結果を代入するリスト
        if (listLoginData[k][0] == listSakeData[j][0]): ###
            for i in range(len(listRyouriData)):
                if (listSakeData[j][0] == listRyouriData[i][0]): ###
                    listMutchDataAll.append(CalculationList(listSakeData[j][:], listRyouriData[i][:]))

            # listMutchDataAllの味の違いを昇順にソート
            sortListMutchData = SortList(listMutchDataAll, 3)
        
            # ソートした結果のリストに対して上位3つを取り出す
            mutchListHigherOrder = ListHigherOrder(sortListMutchData, 3)

            # 上位3つをlistMutchDataの下にくっつけていく
            listMutchData.extend(mutchListHigherOrder)

# リストをタプルへ変換
tupleMutchData = InListOutTuple(listMutchData)
print("tupleMutchData")
print(tupleMutchData)

            
DeleteTable() # データベースのテーブルを削除
CreateTable() # データベースのテーブルを作成
InsertTable(tupleMutchData) # 作成したテーブルに値を代入

conn.commit()
conn.close()

# list(map(abs, リスト)) リストの絶対値
# len(リスト) リストの長さ
# sort(リスト) は戻り値を返さない
# sorted(リスト) は戻り値を返す
