import requests
import os
from lxml import etree
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
from selenium.webdriver.common.touch_actions import TouchActions
from multiprocessing import Pool
hrefxp = '//div[@id="thumbs"]/div/a/img'
booknamexp = '//*[@id="main"]/div/section/div[1]/div[2]/div/div[1]/h1/span/text()'
clickxp = '/html/body/div[6]/div[11]/div/button'		

while True:
		url = input('请输入上架需要的图片地址')
		r = requests.get(url)
		r.encoding = r.apparent_encoding
		t = etree.HTML(r.text)
		name = t.xpath(booknamexp)[0]
		option = webdriver.ChromeOptions()
		option.add_argument('headless')
		driver = webdriver.Chrome(chrome_options=option)
		driver.get(url)
		driver.find_element_by_xpath(clickxp).click()
		driver.maximize_window()
		hrefl = driver.find_elements_by_xpath(hrefxp)
		imgl = [i.get_attribute('src') for i in hrefl]
		if not os.path.exists(name):
				os.makedirs(name)
		for i in range(len(imgl)):
			im = requests.get(imgl[i])
			f = open('./' +name+'/'+ str(i)+'.jpg','wb')
			f.write(im.content)
			print(f'第{i}张图片写入完成')
		print(f'{name}已保存完成')
		driver.close()
		print('\n')