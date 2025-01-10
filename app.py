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
url_get = requests.get('https://pusatdata.kontan.co.id/makroekonomi/inflasi')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div',attrs={'class':'baris-scroll'})
row = table.find_all('div', attrs={'class':'kol-konten3-1'})
row_length = len(row)

temp = [] #initiating a list 

for i in range(1, row_length):
#insert the scrapping process here
    #get period
    period = table.find_all('div', attrs={'class':'kol-konten3-1'})[i].text

    #get inflation_mom
    inflation_mom = table.find_all('div', attrs={'class':'kol-konten3-2'})[i].text
    inflation_mom = inflation_mom.strip() #to remove excess white space

    #get inflation_yoy
    inflation_yoy = table.find_all('div', attrs={'class':'kol-konten3-3'})[i].text
    inflation_yoy = inflation_yoy.strip() #to remove excess white space

    temp.append((period,inflation_mom,inflation_yoy))

temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp, columns= ('period','inflation_mom','inflation_yoy'))

#insert data wrangling here
data['inflation_mom'] = data['inflation_mom'].astype('str')
data['inflation_yoy'] = data['inflation_yoy'].astype('str')
data['period'] = data['period'].astype('datetime64[ns]')
data['inflation_mom'] = data['inflation_mom'].str.replace(",",".")
data['inflation_yoy'] = data['inflation_yoy'].str.replace(",",".")
data['inflation_mom'] = data['inflation_mom'].astype('float64')
data['inflation_yoy'] = data['inflation_yoy'].astype('float64')

data = data.set_index('period')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{data["inflation_yoy"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = data.plot(figsize = (8,7)) 
	
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