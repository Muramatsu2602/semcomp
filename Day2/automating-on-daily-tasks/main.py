from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as waiter
from selenium.webdriver.support.expected_conditions import (
    visibility_of_element_located as visibility,
    element_to_be_clickable as clickable
)

import io
import os
import time


def get_videos_url(driver, playlist_url):

    # enter youtube playlist
    driver.get(playlist_url)

    # wait for playlist, and get it
    waiter(driver, 60).until(visibility((By.ID, 'playlist')))
    playlist = driver.find_element_by_id('playlist')

    css_sel = 'a[class$="panel-video-renderer"]'
    waiter(driver, 60).until(visibility((By.CSS_SELECTOR, css_sel)))
    videos_url = playlist.find_elements_by_css_selector(css_sel)
    videos_url = [i.get_attribute('href') for i in videos_url]

    # get videos name
    css_sel = 'span[id="video-title"]'
    waiter(driver, 60).until(visibility((By.CSS_SELECTOR, css_sel)))
    videos_name = playlist.find_elements_by_css_selector(css_sel)
    videos_name = [i.get_attribute('title') for i in videos_name]

    # # for in C mode
    # for video in videos_url:
    #     videos_url_lst.append(video.get_attribute())

    return list(zip(videos_url, videos_name))



def download_mp3(driver, video_url, video_name, download_path):

    mp3_path = os.path.join(download_path, video_name + '.mp3')
    if os.path.exists(mp3_path):
        return "Download ALREADY COMPLETED: " + video_name

    # log into video2mp3
    driver.get('https://video2mp3.net')
    driver.switch_to.default_content()

    for _ in range(2):
        waiter(driver, 60).until(visibility((By.CSS_SELECTOR, 'iframe[id="inneriframe"]')))
        iframe = driver.find_element_by_css_selector('iframe[id="inneriframe"]')
        driver.switch_to.frame(iframe)

    # change input
    waiter(driver, 60).until(clickable((By.ID, 'input')))
    input_el = driver.find_element_by_id('input')
    driver.execute_script('arguments[0].value = `%s`' % video_url, input_el)
    waiter(driver, 60).until(clickable((By.ID, 'submit')))
    driver.find_element_by_id('submit').click()

    # download element
    xpath = "//a[contains(text(),'Download')]"
    waiter(driver, 60).until(clickable((By.XPATH, xpath)))
    driver.find_element_by_xpath(xpath).click()

    # wait for download
    for _ in range(5 * 60):
        if os.path.exists(mp3_path):
            break
        time.sleep(1)

    return "Download COMPLETED: " + video_name




# define chrome webdriver
def define_driver(download_path):

    # define download path
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    # options
    options = ChromeOptions()

    # define all settings for webdriver
    # options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_experimental_option(
        "prefs", {
            "download.default_directory": download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
        }
    )

    # creating of webdriver obj
    return Chrome(options=options, executable_path='chromedriver.exe')



# define driver
download_path = os.path.join(os.getcwd(), 'videos')
driver = define_driver(download_path)
playlist_url = 'https://www.youtube.com/watch?v=9Ojb8t3T2Ng&list=PLdpyypChI7Hj1e0bheQ4gQXUMAm2erWWV&index=1'

url_lst = get_videos_url(driver, playlist_url)

for url, name in url_lst:
    print(download_mp3(driver, url, name, download_path))

# close driver
driver.quit()