import mysql.connector
from coinmetrics import CoinMetricsAPI
import datetime

cm = CoinMetricsAPI()
CONFIG = {
	"host": "localhost",
  	"user": "root",
 	"passwd": "zheliang415",
 	"database": "coindb"
}

class Mydatabase:
	def __init__(self, initial):
		if initial:
			self.mydb = mysql.connector.connect(
  				host=CONFIG["host"],
  				user=CONFIG["user"],
 				passwd=CONFIG["passwd"]
			)
			self.mycursor = self.mydb.cursor()
			try:
				self.mycursor.execute("CREATE DATABASE coindb")
			except:
				self.mycursor.execute("DROP DATABASE coindb")
				self.mycursor.execute("CREATE DATABASE coindb")

		self.mydb = mysql.connector.connect(
  			host=CONFIG["host"],
  			user=CONFIG["user"],
 			passwd=CONFIG["passwd"],
 			database=CONFIG["database"]
		)
		self.mycursor = self.mydb.cursor()

	def commit(self):
		self.mydb.commit()


def createtable(asset, mycursor):
	types = cm.get_available_data_types_for_asset(asset)
	attrs = "timestamp INT PRIMARY KEY"
	for attr in types:
		attr = attr.replace("(", "_")
		attr = attr.replace(")", "")
		attrs = attrs + ", " + attr + " VARCHAR(255)"
	sql = "CREATE TABLE " + str(asset) + " (" + attrs + ")"
	mycursor.execute(sql)

def get_history_data_for_asset(asset):
	yesterday = datetime.datetime.today() - datetime.timedelta(1)
	begin_timestamp = int(datetime.datetime(2009, 1, 1).timestamp())
	#end_timestamp = int(datetime.datetime(2009, 1, 2, 23, 59).timestamp())
	end_timestamp = int(datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59).timestamp())
	alldata = cm.get_all_data_types_for_assets(str(asset), begin_timestamp, end_timestamp)[str(asset)]
	return alldata

def get_yesterday_data_for_asset(asset):
	yesterday = datetime.datetime.today() - datetime.timedelta(2)
	begin_timestamp = int(datetime.datetime(yesterday.year, yesterday.month, yesterday.day).timestamp())
	end_timestamp = int(datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59).timestamp())
	alldata = cm.get_all_data_types_for_assets(str(asset), begin_timestamp, end_timestamp)[str(asset)]
	return alldata

def store_data_for_asset(asset, alldata, mydb, mycursor):
	types = cm.get_available_data_types_for_asset(str(asset))
	types_str = 'timestamp, ' + str(types).replace("[", "").replace("]", "").replace("(", "_").replace(")", "").replace("'", "")
	types_str2 = '%s'
	for type in types:
		types_str2 = types_str2 + ', %s'

	sql = "INSERT INTO " + str(asset) + " (" + types_str +") VALUES (" + types_str2 + ')'
	# val_list = []

	data_dic = {}
	index = 1
	for type in types:
		for data in alldata[type]:
			if data[1] == None:
				continue
			if data[0] not in data_dic:
				#make a new list
				ls = get_list(len(types))
				ls[0] = data[0]
				data_dic[data[0]] = ls
			data_dic[data[0]][index] = str(data[1])
		index+=1


	for value in data_dic.values():
		print(value)
		mycursor.execute(sql, value)
		mydb.commit()



def get_list(num):
	ls = [""]
	for i in range(num):
		ls.append("")
	return ls





