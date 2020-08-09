# Automatic-Health-Card

帮助不方便打开网页的同学，让大家都能正确填写健康卡，及时汇报健康信息，全力配合学校做好新型冠状病毒感染的肺炎疫情防控工作。

本软件仅用于当前健康信息相比上次提交健康卡时未发生变化的同学，若健康情况有所变化，请及时在网页版上进行填报。

**本项目仅用于学习和交流，以及各种充满正能量的目的，请勿滥用**

## 下载

`git clone https://github.com/JLUZHAnalytica/Automatic-Health-Card.git`

`cd Automatic-Health-Card`

## 本地如何使用

### 验证你的身份（手动法）

在浏览器打开 https://work.jluzh.com/default/work/jlzh/jkxxtb/jkxxcj.jsp 并登陆

登陆成功后打开浏览器的开发者工具，在如下图所示的位置找到 JSESSIONID，并复制到 setting.py 里面对应的位置

![image](img/WX20200809-171001@2x.png)

程序启动后，询问是否自动打开浏览器获取时，选择不打开，将自动从 setting.py 中读取。


### 启动程序

`python auto_health.py`

如果只想填写一个人的健康卡，填写范围时逗号两边一样即可。

**请谨慎填写学号范围！！！**

## Web版本

普通接口:`/username=<username>&password=<password>/number=<number>`

*<username>*:学号

*<password>*:密码(一般为身份证后六位)

*<number>*:需要填写健康卡的学号

批量接口:`/username=<username>&password=<password>/start=<start>&end=<end>`

*<username>*:学号

*<password>*:密码(一般为身份证后六位)

*<start> <end>*:需要批量填写健康卡的学号范围