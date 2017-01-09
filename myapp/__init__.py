from flask import Flask, request, redirect, render_template
import pandas as pd
import quandl

from bokeh.plotting import figure
from bokeh.embed import components, file_html
from bokeh.charts import TimeSeries

app = Flask(__name__)

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
  return render_template('index.html')

@app.route('/output', methods=['GET', 'POST'])
def output():
    myticker = request.form['ticker_symbol']
    quandlstr = "WIKI/"+myticker+".11"
    startDate = "2016-11-30"
    endDate = "2016-12-30"
    try:
        df = quandl.get(quandlstr, start_date=startDate, end_date=endDate)
        #Fixed TimeSeries display https://github.com/bokeh/bokeh/issues/4344
        df['dates'] = df.index.to_datetime()
        fig = TimeSeries(df, x='dates')
        script, div =components(fig)
        title = 'Closing price for {} in the last month'.format(myticker)
        return render_template('plot.html', script=script, div=div, title=title)
    except:
        return render_template('error.html')

@app.route('/mainpage', methods=['GET', 'POST'])
def mainpage():
    return redirect('/index')
