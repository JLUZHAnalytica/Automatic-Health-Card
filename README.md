# Automatic-Health-Card

自动填写学校健康卡

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

## Web版本