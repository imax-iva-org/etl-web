from flask import Flask, redirect, url_for, render_template
from configparser import ConfigParser
import pymysql
import datetime


app = Flask(__name__)


def get_db_odjects(config_params):
    try:
        db_conn = pymysql.connect(host=config_params['host'],
                                  port=int(config_params['port']),
                                  user=config_params['user'],
                                  passwd=config_params['passwd'],
                                  db=config_params['db'],
                                  charset=config_params['charset'])
        # db_conn = pymysql.connect(**config_params)
        db_cursor = db_conn.cursor()
    except pymysql.InternalError as e:
        print('{0}\tDB connection internal error: {1}, {2}'.format(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            e.args[0],
            e.args[1]
        ))
    except pymysql.ProgrammingError as e:
        print('{0}\tDB connection programming error: {1}, {2}'.format(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            e.args[0],
            e.args[1]
        ))

    return db_conn, db_cursor


def db_cursor_exec(db_cursor, sql_statement):

    dataset = []
    try:
        db_cursor.execute(sql_statement)
        dataset = [list(row) for row in db_cursor.fetchall()]
    except pymysql.InternalError as e:
        print('{0}\tDB connection internal error: {1}, {2}'.format(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            e.args[0],
            e.args[1]
        ))
    except pymysql.DataError as e:
        print('{0}\tDB connection data error: {1}, {2}'.format(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            e.args[0],
            e.args[1]
        ))
    except pymysql.OperationalError as e:
        print('{0}\tDB connection operational error: {1}, {2}'.format(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            e.args[0],
            e.args[1]
        ))

    return dataset


def get_dataset():

    result = []

    config = ConfigParser()
    config.read('config.ini')
    if config.has_section('DB_Connection'):
        config_params = config['DB_Connection']
    else:
        return result

    db_conn, db_cursor = get_db_odjects(config_params)
    if not db_cursor:
        return result

    result = db_cursor_exec(db_cursor, 'CALL `api_data`.`posts_count`(1);')
    return result


@app.route('/')
def index():
    return redirect(url_for('data_monitor'))


@app.route('/monitor')
def data_monitor():
    chartID = 'chart_ID'
    chart_type = 'line'
    dataset = get_dataset()
    series = [{'name': 'Date and time', 'data': dataset}]
    title = {'text': 'Posts count for last day'}
    subtitle = {'text': 'last day'}
    xAxis = {'type': 'datetime'}
    yAxis = {'title': {'text': 'Posts count'}}
    chart = {"renderTo": chartID, "type": chart_type}

    return render_template('monitoring.html',
                           chartID=chartID,
                           chart=chart,
                           series=series,
                           title=title,
                           subtitle=subtitle,
                           xAxis=xAxis,
                           yAxis=yAxis)


@app.route('/logging')
def logging():
    return render_template('logging.html')


if __name__ == '__main__':
    app.run(debug=True)
