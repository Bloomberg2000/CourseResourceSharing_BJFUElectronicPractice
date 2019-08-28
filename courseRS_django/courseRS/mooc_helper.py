import time, re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as BS

from courseRS.models import Course


def PhantomJS_web(url):
    # 无头浏览器爬取
    driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
    driver.set_page_load_timeout(5)
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)


def crawl_mooc():
    url = 'http://www.icourse163.org/category/all'
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(100)
    try:
        driver.get(url)
    except TimeoutException:
        print('time out after 30 seconds when loading page')
        driver.execute_script('window.stop()')
    driver.maximize_window()
    driver.implicitly_wait(10)  # 控制间隔时间，等待浏览器反应

    kc_names, kc_schools, kc_teachers, kc_introductions, kc_stunums, kc_start_times, kc_links, kc_id_nums = [], [], [], [], [], [], [], []
    page_num, max_page_num = 1, 1
    while True:
        if page_num > 100 or page_num > max_page_num:  # 设置爬取页数
            print('已爬取MOOC课程' + str(page_num - 1) + '页！')
            break
        htm_const = driver.page_source
        soup = BS(htm_const, 'lxml')
        if page_num == 1:
            max_page_num = int(soup.find_all(name='a', attrs={'class': 'th-bk-main-gh'})[-2].string)
        c_names = soup.find_all(name='img', attrs={'height': '150px'})
        c_schools = soup.find_all(name='a', attrs={'class': 't21 f-fc9'})
        c_introductions = soup.find_all(name='span', attrs={'class': 'p5 brief f-ib f-f0 f-cb'})
        c_stunums = soup.find_all(name='span', attrs={'class': 'hot'})
        c_start_times = soup.find_all(name='span', attrs={'class': 'txt'})
        c_links = soup.find_all(name='span', attrs={'class': 'u-course-name f-thide'})
        for i in range(len(c_names)):
            kc_names.append(c_names[i]['alt'])
            kc_schools.append(c_schools[i].string)
            if c_introductions[i].string is None:
                c_introduction = ''
            else:
                c_introduction = c_introductions[i].string
            kc_introductions.append(c_introduction)
            c_stunum = re.compile('[0-9]+').findall(c_stunums[i].string)[0]
            kc_stunums.append(int(c_stunum))
            kc_start_times.append(c_start_times[i].string)
            kc_links.append('http:' + c_links[i].parent['href'])
            c_id_num = re.compile('[0-9]{4,}').findall(c_links[i].parent['href'])[0]
            kc_id_nums.append(int(c_id_num))
        try:

            time.sleep(3)
            next_page = WebDriverWait(driver, 10).until(
                EC.visibility_of(driver.find_element_by_link_text('下一页'))
            )
            next_page.click()
            time.sleep(3)
        except Exception as e:
            print(e)
            break
        page_num += 1
    kc_info = [kc_names, kc_schools, kc_introductions, kc_stunums, kc_start_times, kc_links]
    save_mysql(kc_info)
    driver.quit()


def save_mysql(kc_info):
    for i in range(len(kc_info[0])):
        new_class = Course(name=kc_info[0][i], subordinateSchoolAndCollege=kc_info[1][i], info=kc_info[2][i],
                           checkInNum=kc_info[3][i], currentStatus=kc_info[4][i], link=kc_info[5][i])
        new_class.save()
