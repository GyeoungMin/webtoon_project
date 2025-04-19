import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time

options = ChromeOptions()

options.add_argument('lang=ko_KR')
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

df_classification = pd.DataFrame()
plots = []
categories = []
titles = []

url = 'https://page.kakao.com/menu/10010/screen/82?subcategory_uid=0'
driver.get(url)

time.sleep(1)

# driver.find_element(By.XPATH, '//*[@id="gnb_login_button"]').click()

# login_id_element = driver.find_element(By.XPATH , '//*[@id="id"]')
# login_pw_element = driver.find_element(By.XPATH , '//*[@id="pw"]')
# login_id_element.send_keys(login_id)
# time.sleep(0.5)
# login_pw_element.send_keys(login_pw)
# time.sleep(0.5)
# login_pw_element.send_keys(Keys.RETURN)

# print(list(soup))
# for i in range(5):
#     driver.execute_script("window.scrollBy(0, 1000);")  # 세로 방향으로 1000px씩 내림
#     time.sleep(1)
for idx in range(2,8):
    category_xpath = '//*[@id="__next"]/div/div[2]/div/div[2]/div[1]/div/div[1]/div/a[{}]'.format(idx)
    try:
        category_element = driver.find_element(By.XPATH, category_xpath)
        category = category_element.text
        category_element.click()
        time.sleep(1)

        last_height = driver.execute_script("return document.body.scrollHeight")
        i = 1
        while True:
            webtoon_xpath = '//*[@id="__next"]/div/div[2]/div/div[2]/div[1]/div/div[4]/div/div/div/div[{}]/div/a'.format(i)
            title_xpath = '//*[@id="__next"]/div/div[2]/div[1]/div/div[1]/div[1]/div/div[2]/a/div/span[1]'

            try:
                driver.find_element(By.XPATH, webtoon_xpath).click()

                time.sleep(1)  # 3. 페이지가 완전히 바뀔 때까지 잠깐 대기
                title = None
                plot = None

                while True:
                    plot_xpath = '//*[@id="__next"]/div/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div'
                    info_xpath = '//*[@id="__next"]/div/div[2]/div[1]/div/div[2]/div[1]/div/div/div[2]/a'
                    driver.find_element(By.XPATH, info_xpath).click()

                    time.sleep(1)
                    try:
                        title = driver.find_element(By.XPATH, title_xpath).text
                        plot = driver.find_element(By.XPATH, plot_xpath).text
                    except:
                        try :
                            plot_xpath = '//*[@id="__next"]/div/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[2]/div'
                            plot = driver.find_element(By.XPATH, plot_xpath).text
                        except:
                            print('error', i)
                    if plot is not None: break
                    time.sleep(1)

                titles.append(title)
                plots.append(plot)
                categories.append(category)

                # 4. 뒤로 가기 (브라우저의 뒤로가기 기능!)
                driver.back()
                # 5. 다시 돌아온 페이지를 위해 잠깐 대기
                time.sleep(1)

                driver.back()

                time.sleep(1)

                i += 1      # i = i + 1
            except:
                print('scrolling')
                driver.execute_script("window.scrollBy(0, 1000);")  # 세로 방향으로 1000px씩 내림
                time.sleep(1)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    print(f"📌 카테고리 {category}에서 스크롤 종료")
                    break
                last_height = new_height
    except:
        pass

print(titles)
print(plots)
print(categories)

df_classification['title'] = titles
df_classification['plot'] = plots
df_classification['category'] = categories

df_classification.info()
print(df_classification.head())

df_classification.to_csv('./crawling_data/kakao_category_plot.csv',index=False)

# for i in range(5):
#     time.sleep(0.5)
#
# time.sleep(5)
#
#
# for i in range(1, 5):
#     for j in range(1, 7):
#         title_path = '//*[@id="newsct"]/div[4]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(i, j)
#         try:
#             title = driver.find_element(By.XPATH, title_path).text
#             print(title)
#         except:
#             print('error', i, j)

