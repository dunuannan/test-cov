import time

import pymysql


def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年", "月", "日")


def get_conn():
    """
    :return: 连接，游标
    """
    # 建立连接
    conn = pymysql.connect(host="cdb-l4vaj5m4.bj.tencentcdb.com",
                           port=10048,
                           user="root",
                           password="Dnn+12055693",
                           db="cov")
    # 创建游标，默认是元组型
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def query(sql, *args):
    """
    封装通用查询
    :param sql:
    :param args:
    :return: 返回查询到的结果，((),())的形式
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)

    return res


def get_keyword_data():
    """
    :return: 返回大屏 div id=key-word 的数据
    """
    # 因为会更新多次数据，取时间戳最新的那组数据
    sql = "SELECT SUM( confirm )," \
          "( SELECT suspect FROM history ORDER BY ds DESC LIMIT 1 )," \
          "SUM( heal )," \
          "SUM( dead ) " \
          "FROM  details " \
          "WHERE update_time=(SELECT update_time FROM details ORDER BY update_time DESC LIMIT 1)"

    res = query(sql)
    return res[0]


def get_map_data():
    """
    :return: 返回各省的数据
    """
    # 因为会更新多次数据，取时间戳最新的那组数据
    sql = "SELECT province, SUM( confirm ) FROM details " \
          "WHERE update_time =( SELECT update_time FROM details ORDER BY update_time DESC LIMIT 1 ) " \
          "GROUP BY province"

    res = query(sql)
    return res


def get_total_data():
    """
    :return: 返回累计数据
    """
    sql = "SELECT ds, confirm, suspect,heal,dead FROM history"

    res = query(sql)
    return res


def get_add_data():
    """
    :return: 返回新增数据
    """
    sql = "SELECT ds, confirm_add, suspect_add FROM history"

    res = query(sql)
    return res


def get_rank_data():
    """
    :return: 返回非武汉地区城市确诊人数前10名
    """
    sql = 'SELECT city,confirm FROM ' \
          '(SELECT city,confirm FROM details ' \
          'WHERE update_time=(SELECT update_time FROM details ORDER BY update_time DESC LIMIT 1) ' \
          'AND province NOT IN ("湖北","北京","上海","天津","重庆") ' \
          'UNION ALL ' \
          'SELECT province,SUM(confirm) FROM details ' \
          'WHERE update_time=(SELECT update_time FROM details ORDER BY update_time DESC LIMIT 1) ' \
          'AND province IN ("北京","上海","天津","重庆") GROUP BY province) as a ' \
          'ORDER BY confirm DESC LIMIT 10'

    res = query(sql)
    return res


def get_hot_data():
    """
    :return: 返回最近的20条热搜
    """
    sql = "SELECT content FROM hotsearch ORDER BY id DESC LIMIT 20"

    res = query(sql)  # 返回tuple格式 (('安徽全省退出高风险地区51112',), ('大邱医院改造集装箱收治患者55592',))
    return res


def test():
    pass


if __name__ == "__main__":
    print(get_hot_data())
