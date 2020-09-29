from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as waiter
from selenium.webdriver.support.expected_conditions import (
    visibility_of_element_located as visibility,
    element_to_be_clickable as clickable
)


def get_videos_url(driver, playlist_url):

    # enter youtube playlist
    driver.get(playlist_url)

    # wait for playlist, and get it
    waiter(driver, 60).until(visibility((By.ID, 'playlist')))
    playlist = driver.find_element_by_id('playlist')

    css_sel = 'a[class$="panel-video-renderer"]'
    waiter(driver, 60).until(visibility((By.CSS_SELECTOR, css_sel)))
    videos_url = playlist.find_element_by_css_selector(css_sel)
    videos_url = [i.get_attribute('href') for i in videos_url]

    # list comprehension
    videos_url = [i.get_attribute('href') for i in videos_url]

    # get videos name
    css_sel = 'a[class$="panel-video-renderer"]'
    waiter(driver, 60).until(visibility((By.CSS_SELECTOR, css_sel)))
    videos_name = playlist.find_element_by_css_selector(css_sel)
    videos_name = [i.get_attribute('title') for i in videos_url]

    return url_lst


def download_mp3(video_url):
    return


def define_driver():

    return Chrome(executable_path='./chromedriver')


# define driver
driver = define_driver()
playlist_url = 'https://www.youtube.com/watch?v=9Ojb8t3T2Ng&list=PLdpyypChI7Hj1e0bheQ4gQXUMAm2erWWV&index=1'

url_lst = get_videos_url(driver, playlist_url)

for i in url_lst:
        print(i)


# close driver
driver.quit()
