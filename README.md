# TrainTimer用時刻データ生成用スクリプト
## 概要
公開の終了したTrainTimerというandroidアプリ用の時刻表データをYahooから取得し，生成するスクリプト

## 使い方
1．以下通りに実行し，時刻表データを取得する(平日，土曜，日曜祝日)
```
# URL例:https://transit.yahoo.co.jp/station/time/25853/?kind=4&gid=1770&q=%E5%A4%A7%E9%98%AA&tab=time
python traintimetableparser.py "URL"
```
2．result.xtにtraintimerの.dat形式の時刻表が出力されるため，以下フォーマットにし，連番.datとして保存する
```
URL=平日の時刻表データのURL
[平日]
HH:MM,普通,××,
[土曜]
HH:MM,普通,××,
[日曜・祝日]
HH:MM,普通,××,
```

3．アプリの設定よりバックアップを作成  
4．バックアップに本スクリプトを用いて生成した情報を入れ込んだデータを生成する  
4-1．traintimer.zipを解凍  
4-2．今回作成したファイルを既にある連番以降の番号名としておく  
4-3．traintimer.dbを開き，TrainTimerDataテーブルにほかのデータにならって今回作成したデータ分の情報を追加し保存する  
4-4．既にあるdatファイルと今回作成したdatファイルとtraintimer.dbをzip形式で圧縮  
5．4で作成したファイルをバックアップが作成されているディレクトリに置く  
6．アプリの設定よりバックアップから復元を実施する  