# caipiao

> 抓取了500彩票网的双色球数据

> 执行命令：

    scrapy crawl cp500dcb -o store/double_color_ball.csv --logfile "log/cp500dcb_20170909.log" -a all=True

    all:True 代表抓取历史所有期数, False或者不传则只抓取最新一期