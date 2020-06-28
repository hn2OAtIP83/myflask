from flask import Flask, render_template, request, redirect
import pandas as pd
import requests
from bokeh.plotting import figure
from bokeh.embed import components
import simplejson as json

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

  stock = "GOOG"
  api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % stock
  session = requests.Session()
  session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
  data = session.get(api_url)
  jsondata = data.json()
  df = pd.DataFrame(jsondata['data'], columns=jsondata['column_names'])

  df['Date'] = pd.to_datetime(df['Date'])

  x = df['Date'].values
  y = df['Open'].values

  plot = figure(title='Data from Quandle WIKI set',
              x_axis_label='date',
              x_axis_type='datetime')

  plot.line(x, y, line_width=2, legend_label="Close")

  script, div = components(plot)

  return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)
