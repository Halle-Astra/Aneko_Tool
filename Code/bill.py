while True:
	x = input('请输入要日元数及其操作，若操作为1则视为含税')
	x = x+' 0'
	x,y = x.split()
	x = eval(x)
	y = eval(y)
	if not  y:
		print(f'加税后为：{x*1.08*0.065}')
	else:
		print(f'视为含税计算结果为：{x*0.065}')
	print('\n')
