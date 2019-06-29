#本代码暂时仅适用于虎穴的页面，从旧版getpicsfortora修改而来，新增多进程模式提高速度。多链接并行。
#如遇到非直接可下图像的链接，将输出提醒以便另行下载。（建议此时使用getpicsfortora）
#为了方便起见，统一将需要读取的链接文件命名为'1.txt'运行结束后会对其进行文件名修改。
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

def imgsave(i,url):
	try:
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
		return -1,''#如果成功运行则返回负值和空字符串
	except:
		return 	i,url+'#'

def main():
	print('正在读取文件1.txt以获取链接')
	urlfile = open('1.txt')
	urlls = urlfile.read()
	urlfile.close()
	urlls = urlls.split('\n')#以行为分割方式
	pool = Pool(8)
	res_l = []
	for i in range(len(urlls)):
		res = pool.apply_async(imgsave,args = (i,urlls[i]))
		res_l.append(res.get())
	pool.close()
	pool.join()
	time_s = time.strftime('%Y_%m_%d')
	wrong_out = './'+time_s+'.xls'
	wrong_num = [i[0] for i in res_l if i[0]>=0]
	wrong_num = len(wrong_num)
	with open(wrong_out,'w') as f:
		if not wrong_num:
			mes = '全部成功运行'
			f.write(mes)
		else :
			print('==========================链接运行状态如下=============================\n')
			for i in res_l:
				mes = str(i[0])+'\t'+i[1]
				print(mes)
				f.write(mes+'\n')
	os.system(f'notepad {wrong_out}')
	os.rename('1.txt',f'1_{time_s}.txt')
	
if __name__=='__main__':
	main()