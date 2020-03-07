import json
import sys
import time
import traceback

import pymysql
import requests
from selenium.webdriver import Chrome, ChromeOptions


def get_conn():
    """
    :return: 连接，游标
    """
    # 建立连接
    conn = pymysql.connect(host="cdb-l4vaj5m4.bj.tencentcdb.com",
                           port=10048,
                           user="root",
                           password="",
                           db="cov")
    # 创建游标，默认是元组型
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def get_tencent_data():
    """
    :return: 返回历史数据和当日详细数据
    """
    url_h5 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    url_other = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"
    }
    r_h5 = requests.get(url_h5, header)
    r_other = requests.get(url_other, header)

    # json字符串转字典
    res_h5 = json.loads(r_h5.text)
    res_other = json.loads(r_other.text)

    data_h5 = json.loads(res_h5["data"])
    data_other = json.loads(res_other["data"])

    history = {}  # 历史数据 从disease_other中获取
    for i in data_other["chinaDayList"]:
        ds = "2020." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds] = {
            "confirm": confirm,
            "suspect": suspect,
            "heal": heal,
            "dead": dead
        }

    for i in data_other["chinaDayAddList"]:
        ds = "2020." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds].update({
            "confirm_add": confirm,
            "suspect_add": suspect,
            "heal_add": heal,
            "dead_add": dead
        })

    details = []  # 当日详细数据 从disease_h5中获取
    update_time = data_h5["lastUpdateTime"]
    data_country = data_h5["areaTree"]  # list 42个国家
    data_province = data_country[0]["children"]
    for pro_infos in data_province:
        province = pro_infos["name"]  # 省名
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]
            confirm = city_infos["total"]["confirm"]
            confirm_add = city_infos["today"]["confirm"]
            heal = city_infos["total"]["heal"]
            dead = city_infos["total"]["dead"]
            details.append([update_time, province, city, confirm, confirm_add, heal, dead])
    return history, details


def update_details():
    """
    更新 details 表
    :return:
    """
    cursor = None
    conn = None
    try:
        ls = get_tencent_data()[1]  # 索引 0 是历史数据字典， 1 是最新详细数据列表
        conn, cursor = get_conn()
        sql = "INSERT INTO details(update_time,province,city,confirm,confirm_add,heal,dead) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select %s=(SELECT update_time FROM details ORDER BY id DESC LIMIT 1)"  # 对比当前最大的时间戳
        cursor.execute(sql_query, ls[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()} 开始更新最新数据")
            for item in ls:
                cursor.execute(sql, item)
            conn.commit()  # 提交事务 update delete insert 操作
            print(f"{time.asctime()} 更新最新数据完毕")
        else:
            print(f"{time.asctime()} 已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def insert_history():
    """
    插入历史数据
    :return:
    """
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]  # 索引 0 是历史数据字典， 1 是最新详细数据列表
        print(f"{time.asctime()} 开始插入历史数据")
        conn, cursor = get_conn()
        sql = "INSERT INTO history(ds,confirm,confirm_add,suspect,suspect_add,heal,heal_add,dead,dead_add) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for k, v in dic.items():
            # item 格式 {'2020-01-03':{'confirm':41, 'suspect':0, 'dead':1}}
            cursor.execute(sql, [k, v.get('confirm'), v.get('confirm_add'), v.get('suspect'), v.get('suspect_add'),
                                 v.get('heal'), v.get('heal_add'), v.get('dead'), v.get('dead_add')])
        conn.commit()
        print(f"{time.asctime()} 插入历史数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def update_history():
    """
    更新历史数据
    :return:
    """
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]  # 索引 0 是历史数据字典， 1 是最新详细数据列表
        print(f"{time.asctime()} 开始更新历史数据")
        conn, cursor = get_conn()
        sql = "INSERT INTO history(ds,confirm,confirm_add,suspect,suspect_add,heal,heal_add,dead,dead_add) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "SELECT confirm FROM history WHERE ds=%s"
        for k, v in dic.items():
            # item 格式 {'2020-01-03':{'confirm':41, 'suspect':0, 'dead':1}}
            if not cursor.execute(sql_query, k):
                cursor.execute(sql, [k, v.get('confirm'), v.get('confirm_add'), v.get('suspect'), v.get('suspect_add'),
                                     v.get('heal'), v.get('heal_add'), v.get('dead'), v.get('dead_add')])
        conn.commit()
        print(f"{time.asctime()} 插入更新数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def get_baidu_hot():
    """
    :return:返回百度疫情热搜
    """
    option = ChromeOptions()  # 创建谷歌浏览器实例
    option.add_argument("--headless")  # 隐藏浏览器
    option.add_argument("--no-sandbox")

    d = int(time.strftime("%d", time.localtime())) - 1  # 应对 more_btn 地址的变化

    url = "https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1"
    browser = Chrome(options=option, executable_path="chromedriver.exe")
    browser.get(url)

    # 找到展开按钮
    more_btn = browser.find_element_by_css_selector(
        '#ptab-0 > div > div.VirusHot_1-5-4_32AY4F.VirusHot_1-5-4_2RnRvg > section > div')
    # more_btn = browser.find_element_by_css_selector('#ptab-0 > div > div.VirusHot_1-5-%d'%(d)+'_32AY4F.VirusHot_1-5-%d'%(d)+'_2RnRvg > section > div')
    more_btn.click()
    time.sleep(1)  # 等待1秒

    # 找到热搜标签
    infos = browser.find_elements_by_xpath('//*[@id="ptab-0"]/div/div[2]/section/a/div/span[2]')
    context = [i.text for i in infos]
    return context


def update_hotsearch():
    """
    将疫情热搜插入数据库
    :return:
    """
    cursor = None
    conn = None
    try:
        context = get_baidu_hot()
        print(f"{time.asctime()}开始更新热搜数据")
        conn, cursor = get_conn()
        sql = "INSERT INTO hotsearch(dt,content) VALUES(%s,%s)"
        ts = time.strftime("%Y-%m-%d %X")
        for i in context:
            cursor.execute(sql, (ts, i))  # 插入数据
        conn.commit()  # 提交事务保存数据
        print(f"{time.asctime()}热搜数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


if __name__ == '__main__':
    l = len(sys.argv)
    if l == 1:
        s = """
            参数说明:
            up_his 更新历史数据表
            up_det 更新详细数据表
            up_hot 更新实时热搜表
        """
        print(s)
    else:
        order = sys.argv[1]
        if order == "up_his":
            update_history()
        elif order == "up_det":
            update_details()
        elif order == "up_hot":
            update_hotsearch()
