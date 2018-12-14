import falcon
import json
import logging
import quandl
import requests

quandl.ApiConfig.api_key = "WN-AGXtxyZSPnya2pAG_"

class BTCResource(object):
	BTC_DB_CODE = "BCHAIN"

	def get_timeframe(self, params):
		start = params["start_date"]
		end = params["end_date"]
		return start, end

	def on_get(self, req, resp):
		start_date, end_date = self.get_timeframe(req.params)
		
		# Create dataframe for BTC
		data_frame = DataFrameGenerator(start_date, 
											end_date, BTCResource.BTC_DB_CODE)
		
		btc_price = data_frame.get_price(start_date, end_date)
		btc_volume = data_frame.get_output_volume(start_date, end_date)
		btc_address_count = data_frame.get_unique_addresses(start_date, end_date)
		complete_dataset = data_frame.combined_datasets(btc_price, btc_volume, btc_address_count)

		temp = {"start": start_date, "end": end_date}
		resp.body = json.dumps(complete_dataset, ensure_ascii=False)
		resp.status = falcon.HTTP_200

# """
class DataFrameGenerator(object):
	"""Generate Data for the provided type (BTC in this case) """
	# URL = "https://www.quandl.com/data/{}/{}?start_date={}&end_date={}"
	URL = "https://www.quandl.com/api/v3/datasets/{db}/{ds}/data.json?api_key=WN-AGXtxyZSPnya2pAG_&start_date={start}&end_date={end}"

	def __init__(self, start, end, db_code):
		self.start_date = start
		self.end_date = end
		self.db_code = db_code
		
	def combined_datasets(self, price_data=[], output_volume=[], unique_addresses=[]):
		# Empty data set
		# temp = {elem[0]:[elem[1]] for elem in price_data}
		res = {}
		# all data sets should be the same length
		for i in range(len(price_data)):
			res[price_data[i][0]] = [price_data[i][1], output_volume[i][1], unique_addresses[i][1]]
		return res

	def get_price(self, start_date, end_date):
		print("debug action=get_btc_price start_date={} end_date={}"
				.format(start_date, end_date))
		query = DataFrameGenerator.URL.format(	db = self.db_code, 	# Database
												ds = "MKPRU", 		# Dataset
												start = self.start_date, 	# timeframe start
												end = self.end_date)		# timeframe end
		
		print("debug action=get_btc_price query={}".format(query))

		# Issue GET request to retreive 
		response = requests.get(query)
		response_as_json = response.json()

		# Array of time-stamped nodes containing date and price for that day
		price_data = response_as_json['dataset_data']['data']
		return price_data


	def get_output_volume(self,start_date, end_date):
		print("debug action=get_output_volume start_date={} end_date={}"
				.format(start_date, end_date))

		query = DataFrameGenerator.URL.format(	db = self.db_code, 	# Database
												ds = "TOUTV", 		# Dataset
												start = self.start_date, 	# timeframe start
												end = self.end_date)		# timeframe end
		response = requests.get(query).json()
		volume_data = response['dataset_data']['data']

		return volume_data

	def get_unique_addresses(self, start_date, end_date):
		print("debug action=get_unique_addresses start_date={} end_date={}"
				.format(start_date, end_date))

		query = DataFrameGenerator.URL.format(	db = self.db_code, 	# Database
												ds = "NADDU", 		# Dataset
												start = self.start_date, 	# timeframe start
												end = self.end_date)		# timeframe end
		response = requests.get(query).json()
		volume_data = response['dataset_data']['data']
		return volume_data

api = application = falcon.API()

btcr = BTCResource()
api.add_route('/api/btc', btcr)


