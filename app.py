import pandas as pd
import numpy as np
from flask import Flask, render_template, request
import csv

app = Flask(__name__, template_folder='template')

@app.route('/')
def index():
    start_year = request.args.get("start year", False)
    start_month = request.args.get("start month", False)
    end_year = request.args.get("end year", False)
    end_month = request.args.get("end month", False)
    money = request.args.get("money", False)

    df = pd.read_csv("/data/sp calculator data.csv")
    years = df['Year'].unique().tolist()
    months = df['Month'].unique().tolist()

    end = 1
    start = 1
    open_price = 1
    real_open_price = 1
    total_open = 1
    close_price = 1
    real_close_price = 1
    total_close = 1

    with open("/data/sp calculator data.csv") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if row[1] == start_year and row[2] == start_month:
                open_price = row[3]
                real_open_price = row[4]
                total_open = row[5]
                start = row[0]
            elif row[1] == end_year and row[2] == end_month:
                close_price = row[3]
                real_close_price = row[4]
                total_close = row[5]
                end = row[0]

    period = (float(end) - float(start)) / 12

    def cagr(open, close, period):
        if period == 0:
            return 'N/A'
        else:
            return '%.2f' % ((((float(close) / float(open)) ** (1/period)) - 1) * 100)


    nominal_change = '%.2f' % ((float(close_price) / float(open_price) - 1) * 100)
    nominal_cagr = cagr(open_price, close_price, period)
    money_final = '%.2f' % (float(money) * (float(close_price) / float(open_price)))

    real_change = '%.2f' % ((float(real_close_price) / float(real_open_price) - 1) * 100)
    real_cagr = cagr(real_open_price, real_close_price, period)
    real_money_final = '%.2f' % (float(money) * (float(real_close_price) / float(real_open_price)))

    total_change = '%.2f' % ((float(total_close) / float(total_open) - 1) * 100)
    total_cagr = cagr(total_open, total_close, period)
    total_money = '%.2f' % (float(money) * (float(total_close) / float(total_open)))

    return render_template('index.html',
                           years=years,
                           months=months,
                           start_year=start_year,
                           start_month=start_month,
                           end_year=end_year,
                           end_month=end_month,
                           nominal_change=nominal_change,
                           money_final=money_final,
                           nominal_cagr=nominal_cagr,
                           real_change=real_change,
                           real_cagr=real_cagr,
                           real_money_final=real_money_final,
                           total_change=total_change,
                           total_cagr=total_cagr,
                           total_money=total_money
                           )

if __name__ == "__main__":
    app.run(debug=True)
    


