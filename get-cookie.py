#from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import FirefoxOptions
from lib.database import *

#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--disable-extensions')
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--profile-directory=Default')
#chrome_options.add_argument("--incognito")
#chrome_options.add_argument("--disable-plugins-discovery");
#chrome_options.add_argument("--headless")
#driver = webdriver.Chrome("/usr/local/bin/chromedriver",chrome_options=chrome_options)
opts = FirefoxOptions()
opts.add_argument("--headless")
try:
	driver = webdriver.Firefox(firefox_options=opts)
	driver.delete_all_cookies()
	#driver.set_window_size(800,800)
	#driver.set_window_position(0,0)
	driver.get('https://admin-official.line.me')
	print('Starting task')
	cookie = {'_trmccid' : '7c16c24ab1214980', 'LC' : 'ff6332cde66a668991cbfe6cf26977bc3301aa656ce191013f52dd47349d3cbb', 'cert' : '52a42c3d83ace3c512b62dd26d23e91a1f887850ed8eacdf8f700ca7624f0afe', '__try__' : '1530482521524'}
	for x in cookie:
		driver.add_cookie({ 'name' : x ,'value' : cookie[x]})
	element = driver.find_element_by_name("tid")
	element.send_keys('kucingmeongbunyinya@gmail.com')
	element = driver.find_element_by_name("tpasswd")
	element.send_keys("fdu477pq48")
	element = driver.find_element_by_class_name("MdBtn03Login")
	element.click()
	print('Login in')
	try:
		element = WebDriverWait(driver, 5).until(
			EC.title_contains("MANAGER")
		)
		cookies_list = driver.get_cookies()
		cookies_dict = "" #{}
		for cookie in cookies_list:
			cookies_dict+=cookie['name']+"="+cookie['value']+";"
		dbcursor.execute("""UPDATE cookie SET cookie='{0}' WHERE 1""".format(cookies_dict))
		print('Task success')
	except TimeoutException as err:
		print("Task Error: Can't login")
	finally:
		print('Task done')
	#	driver.save_screenshot('ss2.png')
	#	print(driver.current_url)
	#driver.get('https://admin-official.line.me')
	#driver.save_screenshot('ss.png')
finally:
	print('Closing driver')
	driver.close()
	db.commit()
	dbcursor.close()
	db.close()