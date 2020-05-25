# requests のインポート
import requests
# Beautiful Soupのインポート
from bs4 import BeautifulSoup
# datetime のインポート
from datetime import datetime, date, timedelta
# csv のインポート
import csv

# 今日の年月日を取得
today = datetime.today()
# 昨日の年月日を取得
yesterday = today - timedelta(days=1)

# 年を取得
year = str(yesterday.year)
# 月を取得
month = str(yesterday.month)
# 日を取得
day = int(yesterday.day)

#元 URL
url = 'https://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=&month='

#元 URL の year= と month= を 'year=年' 'month=月' にそれぞれ置換する
url = url.replace('year=', f'year={year}').replace('month=', f'month={month}')

# スクレイピング対象の URL にリクエストを送り HTML を取得する
res = requests.get(url)

# レスポンスの HTML から BeautifulSoup オブジェクトを作る
soup = BeautifulSoup(res.content, 'html.parser')

# 空配列
records = []
# class 属性が mtx である tr タグを対象に
for tr in soup('tr', class_='mtx'):
	# 空配列
	rec = []
	# class 属性が a_print の div タグを対象に
	for div in tr('div', class_='a_print'):
		# a タグを対象に
		for a in div('a'):
			# 配列の末尾に a タグの日付を追加
			rec.append(a.renderContents())
	# class 属性が data_0_0 である td タグを対象に
	for td in tr('td', class_='data_0_0'):
		# 各データを両端の空白文字を取り除いた状態で取得
		data = td.renderContents().strip()
		rec.append(data)
	# rec 配列が空白でない場合 records 配列に rec 配列の値を追加
	if rec != []:records.append(rec)

#ファイル名は年月日.csv
with open(f'{year}{month}{day}.csv','w',newline='') as f:
	# records 配列に取得したデータを出力する
	for rec1 in records:
		try:
			# 空配列
			rec2 = []
			# csv 書き込みの定義
			writer = csv.writer(f)
			# records 配列の1列目の値が '日' と一致した場合のみ続ける
			if int(rec1[0].decode()) == day:
				# rec1 配列のデータとともにインデックスを取得する
				for i, data1 in enumerate(rec1):
					# 日(0列目)、最高気温(7列目)、最低気温(8列目)、天気概況(昼)(19列目)のみ出力する
					if i in [0,7,8,19]:
						# rec2 配列に byte 型から utf-8 に変換した値を追加
						rec2.append(data1.decode('utf-8'))
				print(rec2)
				#rec2 配列の値をcsvファイルに追記
				writer.writerow(rec2)
		except ValueError:
			pass
