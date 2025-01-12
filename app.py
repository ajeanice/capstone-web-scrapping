from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/exchange-rate-history/usd-idr')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', attrs={'class':'history-rates-data'})
row = table.find_all('a',attrs={'class':'w'})
row_length = len(row)

temp = [] #initiating a list 

for i in range(1, row_length):
#insert the scrapping process here
	#get dates
   date = table.find_all('a',attrs={'class':'w'})[i].text
   #get exchange rate
   exchange_rate = table.find_all('span',attrs={'class':'w'})[i].text
   # exchange_rate == exchange_rate.strip() #to remove excess white space

   temp.append((date,exchange_rate))

temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp, columns = ('date','exchange_rate'))

#insert data wrangling here
data['exchange_rate'] = data['exchange_rate'].str.replace('1 USD = ', '').str.replace('IDR','')
data['exchange_rate'] = data['exchange_rate'].str.replace(',','')
data['exchange_rate'] = data['exchange_rate'].astype('int')

data = data.set_index('date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{data["exchange_rate"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = data.plot(figsize = (9,7)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)