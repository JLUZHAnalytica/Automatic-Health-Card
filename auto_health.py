import requests
import json
import time
import sys
import os
from setting import *

headers = {
    "x-requested-with": "XMLHttpRequest",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) ,Chrome/84.0.4147.105 Safari/537.36",
    "content-type": "text/json",
    "origin": "https://work.jluzh.edu.cn",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://work.jluzh.edu.cn/default/work/jlzh/jkxxtb/jkxxcj.jsp",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-length": "896",
}
error_list = []


def query_record(number, headers, only_today=True):
    # number =   # 学号
    # is_today = False   # 是否只查询当天

    if only_today:
        querySqlId = "com.sudytech.work.jlzh.jkxxtb.jkxxcj.queryToday"
    else:
        querySqlId = "com.sudytech.work.jlzh.jkxxtb.jkxxcj.queryNear"

    url = "https://work.jluzh.edu.cn/default/work/jlzh/jkxxtb/com.sudytech.portalone.base.db.queryBySqlWithoutPagecond.biz.ext"
    payloads = '{"params":{"empcode":"' + \
        str(number)+'"},"querySqlId":"'+querySqlId+'"}'
    r = requests.post(url, headers=headers, data=payloads)

    try:
        data = r.json()["list"]
        print(
            f"查询学号 {number} 成功，共计查询到 {len(data)} 份记录。 仅查询今日={only_today}")
    except Exception as e:
        if "统一身份认证平台" in r.text:
            print("JSESSIONID失效，请重新获取")
        else:
            print("遇到错误: "+str(e))
            print(r.text)
        return

    return data


def submit(payloads):
    url = "https://work.jluzh.edu.cn/default/work/jlzh/jkxxtb/com.sudytech.portalone.base.db.saveOrUpdate.biz.ext"
    r = requests.post(url, headers=headers, data=payloads.encode("utf-8"))
    if r.json()["result"] == "1":
        return True
    else:
        print("提交遇到问题，提交请求返回数据为：")
        print(r.text)
        return False


def complete(number):
    if len(query_record(number, headers)) != 0:
        print(f"学号 {number} 今日已经提交过健康卡，程序将不再提交")
        return False
    last_card = query_record(number, headers, False)[0]
    health_card_data = {
        "entity": {
            "sqrid": last_card["SQRID"],
            "sqbmid": last_card["SQBMID"],
            "fdygh": last_card["FDYGH"],
            "rysf": last_card["RYSF"],
            "bt": time.strftime("%Y-%m-%d", time.localtime()) + last_card["BT"][10:],
            "sqrmc": last_card["SQRMC"],
            "gh": last_card["GH"],
            "xb": last_card["XB"],
            "sqbmmc": last_card["SQBMMC"],
            "nj": last_card["NJ"],
            "zymc": last_card["ZYMC"],
            "bjmc": last_card["BJMC"],
            "fdymc": last_card["FDYMC"],
            "ssh": last_card["SSH"],
            "lxdh": last_card["LXDH"],
            "tbrq": time.strftime("%Y-%m-%d", time.localtime()),
            "tjsj": time.strftime("%Y-%m-%d %H:%M", time.localtime()),
            "xjzdz": last_card["XJZDZ"],
            "jqqx": last_card["JQQX"],
            "sfqwhb": last_card["SFQWHB"],
            "sfjchbjry": last_card["SFJCHBJRY"],
            "sfjwhy": last_card["SFJWHY"],
            "sfjwhygjdq": last_card["SFJWHYGJDQ"],
            "xrywz": last_card["XRYWZ"],
            "jtdz": last_card["JTDZ"],
            "grjkzk": last_card["GRJKZK"],
            "jrtw": last_card["JRTW"],
            "qsjkzk": last_card["QSJKZK"],
            "jkqk": last_card["JKQK"],
            "cn": [
                "本人承诺登记后、到校前不再前往其他地区"
            ],
            "bz": last_card["BZ"],
            "_ext": "{}",
            "__type": "sdo:com.sudytech.work.jlzh.jkxxtb.jkxxcj.TJlzhJkxxtb"
        }
    }
    if not submit(json.dumps(health_card_data, ensure_ascii=False)):
        print(f"学号 {number} 提交失败")
        error_list.append(number)
        return False
    print(f"学号 {number} 提交成功！！！")
    return True


def output_error():
    if len(error_list) != 0:
        with open("error_list.json", 'w') as fd:
            fd.write(json.dumps(error_list, indent=4, ensure_ascii=False))
        print("已将发生错误的学号输出至 error_list.json")


if __name__ == "__main__":
    print("为了全力做好学校新型冠状病毒感染的肺炎疫情防控工作，您承诺使用本软件提交的健康信息全部属实。")
    print("如果需要填报的健康表的同学健康信息相比上次提交时有更新，请停止使用本软件，并及时在网页上进行填报。\n若需要填报与上次提交时一样的健康信息，请继续使用。")
    # if len(sys.argv) > 1 or input("是否需要打开浏览器自动获取 JSESSIONID (若是请输入1): ") == '1':
        # try:
    from getcookie import get_cookie
    JSESSIONID = get_cookie(os.environ['USERNAME'], os.environ['PASSWORD'])
        # except Exception as e:
            # print("自动提取遇到错误，请使用手动提取 JSESSIONID 方式。 \n错误：" + str(e))
    headers.update({"cookie": "JSESSIONID=" + JSESSIONID})
    # if len(sys.argv) > 1 or input("请选择填写模式：\nA. 从 setting.py 中读取 number_lsit\nB. 手动输入学号范围\n请输入你的选择（默认B）: ") == "A":
    #     for number in number_lsit:
    #         complete(number)
    #     print(f"总计填写 {len(number_lsit)} 份健康表，其中错误 {len(error_list)} 份")
    #     output_error()
    # else:
    # ran = eval(input('请输入需要填写健康卡的学号范围(格式："19200101","19200130"):'))
    rangeEnv = os.environ['RANGE']
    # if len(ran[0]) != 8:
    #     print("学号输入格式错误，请重新输入。")
    # else:
    if ':' in rangeEnv:
        idx = rangeEnv.find(':')
        startNo = rangeEnv[:idx]
        stopNo = rangeEnv[idx+1:]
        ran = [startNo, stopNo]
    else:
        complete(rangeEnv)
        output_error()
        exit()
    arrNo = []
    if ran[0][0] == '0':
        for i in range(int(startNo), int(stopNo)):
            arrNo.append('0' + str(i))
    else:
        for i in range(int(startNo), int(stopNo)):
            arrNo.append(str(i))
    arrNo.append(stopNo)
    for number in arrNo:
        complete(number)
    print(f"总计填写 {len(arrNo)} 份健康表，其中错误 {len(error_list)} 份")
    output_error()
