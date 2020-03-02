import string

from flask import Flask
from flask import jsonify
from flask import render_template
from jieba.analyse import extract_tags

import util

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("main.html")


@app.route('/time')
def get_time():
    return util.get_time()


@app.route('/keyword')
def get_keyword_data():
    data = util.get_keyword_data()
    return jsonify({"confirm": int(data[0]), "suspect": int(data[1]), "heal": int(data[2]), "dead": int(data[3])})


@app.route('/map')
def get_map_data():
    res = []
    for tup in util.get_map_data():
        # print(tup)
        res.append({"name": tup[0], "value": int(tup[1])})
    return jsonify({"data": res})


@app.route('/total')
def get_total_data():
    data = util.get_total_data()
    day, confirm, suspect, heal, dead = [], [], [], [], []
    for da, co, su, he, de in data[7:]:
        day.append(da.strftime("%m-%d"))
        confirm.append(co)
        suspect.append(su)
        heal.append(he)
        dead.append(de)
    return jsonify({"day": day, "confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead})


@app.route('/add')
def get_add_data():
    data = util.get_add_data()
    day, confirm_add, suspect_add = [], [], []
    for da, ca, sa in data[7:]:
        day.append(da.strftime("%m-%d"))
        confirm_add.append(ca)
        suspect_add.append(sa)
    return jsonify({"day": day, "confirm_add": confirm_add, "suspect_add": suspect_add})


@app.route('/rank')
def get_rank_data():
    data = util.get_rank_data()
    city, confirm = [], []
    for ci, co in data:
        city.append(ci)
        confirm.append(int(co))
    return jsonify({"city": city, "confirm": confirm})


@app.route('/hot')
def get_hot_data():
    data = util.get_hot_data()
    ls = []
    for item in data:
        k = item[0].rstrip(string.digits)  # 移除热搜数字
        v = item[0][len(k):]  # 获取热搜数字
        hots = extract_tags(k)  # 使用jieba提取关键字
        for word in hots:
            if not word.isdigit():
                ls.append({"name": word, "value": v})
    return jsonify({"hotword": ls})


if __name__ == '__main__':
    app.run()
