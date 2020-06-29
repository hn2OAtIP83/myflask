from flask import Flask, render_template, request, redirect, session
import pandas as pd
import requests
from bokeh.plotting import figure
from bokeh.embed import components
#import simplejson as json
import json
import quandl

quandl.ApiConfig.api_key = "fK6eeHbvyzUgszZDrHhj"

#import pandas_datareader as pdr

app = Flask(__name__)

app.vars = {}

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/graph', methods=['POST'])
def graph():
  symbol = "GOOG"
  data = quandl.get_table('WIKI/PRICES', qopts = { 'columns': ['ticker', 'date', 'open', 'close', 'low', 'high'] }, ticker = [symbol], date = { 'gte': '2016-01-01', 'lte': '2016-12-31' })
  df = pd.DataFrame(data)
  print(df.head())
  #jsondata = data.json()
  #print(jsondata)
  ### test
  #columnNames = jsondata['column_names']
  #df = pd.DataFrame.from_dict(jsondata['data'])
  #df.set_axis(columnNames, axis=1, inplace=True)

  ### test
  #df = pd.DataFrame(jsondata['data'], columns=jsondata['column_names'])

  #df = pdr.get_data_yahoo('GOOG')

  df['date'] = pd.to_datetime(df['date'])

  x, y = df['date'].values, df['close'].values

  plot = figure(title='%s Historical Open Quandl WIKI set' % symbol,
              x_axis_label='date',
              x_axis_type='datetime')

  plot.line(x, y, line_width=2, legend_label="Close")

  script, div = components(plot)

  return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)
