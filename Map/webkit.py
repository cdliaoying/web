# -*- coding: utf-8 -*-

"""

Author: Wayne
Ver: v0.1
Date: 2018.03.15
Description:
- this file develop some functions to simulate one js page which can translate Baidu's pix coordinate
  to the BD09's coordinate by the Baidu's API
"""
import os, time
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys  # import html action


''' ======= use phantomjs to open local page ============ '''

'''
driver = webdriver.PhantomJS()
driver.get("/Users/liaoying/Desktop/PythonProject/Baidu/dic/mct2bd09.html")
print(driver.title)
print(driver.current_url)
print(driver.name)
'''

''' ======= use headless type open the website   ============'''


firefox_options = Options()
firefox_options.add_argument('-headless')  # use the headless model(not GUI)
driver = Firefox(executable_path='geckodriver', firefox_options=firefox_options)
# if open local html file in the browser, must add the header - "file://",
# you'll get the malformed url wrong
local_url = "file://" + os.path.join(os.path.abspath('..'), "dic", "mct2bd09.html")
driver.get(local_url)
print(driver.title)
time.sleep(5)
driver.find_element_by_id('mctX').clear()
driver.find_element_by_id('mctY').clear()
driver.find_element_by_id('mctX').send_keys('11584146.4677')
driver.find_element_by_id('mctY').send_keys('3568775.09694')
driver.find_element_by_xpath("//div[2]/p[6]/input[1]").click()
time.sleep(5)
db09_x = driver.find_element_by_xpath("//p[@id=\"pointX\"]").text
db09_y = driver.find_element_by_xpath("//p[@id=\"pointY\"]").text
entertaiment = driver.find_element_by_xpath("//p[@id=\"entertaiment\"]").text
print("db09_x: %s" % db09_x)
print("db09_y: %s" % db09_y)
print("entertaiment: %s" % entertaiment)
driver.quit()



