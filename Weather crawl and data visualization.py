import requests
from pyecharts import Bar
from bs4 import BeautifulSoup

HEADERS={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
}

def page_detail(url):
    datas=[]
    response=requests.get(url,headers=HEADERS)
    text=response.content.decode("utf-8")
    soup=BeautifulSoup(text,"html5lib")
    divEle=soup.find("div",class_="conMidtab")
    divlists=divEle.find_all("div", class_="conMidtab2")
    for div in divlists:
        trs=div.find_all("tr")[2:]
        for index,tr in enumerate(trs): #发现，第一行城市在第2个td下面，非第一行城市在第1个td下面，因此需要判断以下tr属于第几个位置
            tds=tr.find_all("td")
            if trs.index(tr)==0:
                city = tds[1].stripped_strings.__next__()   #取出标签下的字符串数据并去除空格，返回生成器
            else:
                city = tds[0].stripped_strings.__next__()   #生成器取值
            temp=tds[-2].stripped_strings.__next__()
            data={"city":city,"temp":temp}
            datas.append(data)
    return datas


def main():
    city_temp=[]
    urls=["http://www.weather.com.cn/textFC/hb.shtml",
          "http://www.weather.com.cn/textFC/db.shtml",
          "http://www.weather.com.cn/textFC/hd.shtml",
          "http://www.weather.com.cn/textFC/hz.shtml",
          "http://www.weather.com.cn/textFC/hn.shtml",
          "http://www.weather.com.cn/textFC/xb.shtml",
          "http://www.weather.com.cn/textFC/xn.shtml",
          "http://www.weather.com.cn/textFC/gat.shtml"]
    for url in urls:
        datas = page_detail(url)
        city_temp.append(datas)
    dict=city_temp[0]   #city_temp=[[{数据},{数据}....]]类型
    dict.sort(key=lambda dict:int(dict["temp"]))  #按照条件：温度从小到大排序
    dict1=dict[0:10]  #取前10组数据
    #数据可视化
    chart=Bar("中国天气数据分析")   #表名字
    citys=list(map(lambda x:x["city"],dict1))   #横坐标城市
    temps=list(map(lambda x:x["temp"],dict1))   #纵坐标温度
    chart.add("",citys,temps)
    chart.render("temp.html")



if __name__=="__main__":
    main()

