from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
selenium_wait_time = 5


def check_enroll(url):
    timeout = time.time() + 30
    while time.time() < timeout:
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(selenium_wait_time)
        if '<span>Buy now</span>' in driver.page_source:
            driver.close()
            return False
        elif '<span>Enroll now</span>' in driver.page_source:
            driver.close()
            return True
        driver.close()


def get_urls_from_html(source):
    urls = {}
    soup = BeautifulSoup(source, 'html.parser')
    for i in soup.find_all('a', href=True):
        url = i['href']
        if 'udemy.com' in url and url not in urls:
            urls[url] = True
    return urls


def insert_links_to_files(urls, name):
    valid_list, invalid_list, unloaded_list = get_files()
    count = 0
    for url in urls.keys():
        # checks that the url does not already exist
        if f'{url}\n' not in valid_list and f'{url}\n' not in invalid_list and f'{url}\n' not in unloaded_list:
            count += 1
            print(f'{name} links progress: {int(count * 100 / len(urls))}%')
            res = check_enroll(url)
            if res is True:
                with open(r'udemy_links/valid_links.txt', 'a') as fd:
                    fd.write(f'{url}\n')
            elif res is False:
                with open(r'udemy_links/invalid_links.txt', 'a') as fd:
                    fd.write(f'{url}\n')
            else:
                with open(r'udemy_links/unloaded_links.txt', 'a') as fd:
                    fd.write(f'{url}\n')


def telegram():
    file_path = r'udemy_links/telegram_chat_history.html'
    # ensure the chat file exist
    while True:
        try:
            readfile(file_path)
            break
        except:
            file_path = input('Please enter telegram chat history file path: ')
    # copy input chat history to udemy folder.
    if file_path != r'udemy_links/telegram_chat_history.html':
        with open(file_path, 'r', encoding='utf-8') as fd1:
            with open(r'udemy_links/telegram_chat_history.html', 'w', encoding='utf-8') as fd2:
                fd2.write(fd1.read())
    # get links from chat history
    with open(r'udemy_links/telegram_chat_history.html', encoding='utf-8') as fd:
        source = fd.read()
    urls = get_urls_from_html(source)
    insert_links_to_files(urls, 'telegram')


def yofreesamples():
    driver = webdriver.Chrome()
    driver.get('https://yofreesamples.com/courses/free-discounted-udemy-courses-list/')
    driver.execute_script("updateUdemyListSearch('CDevelopment');")
    time.sleep(1)
    urls = get_urls_from_html(driver.page_source)
    driver.execute_script("updateUdemyListSearch('ITSoftware');")
    time.sleep(1)
    urls |= get_urls_from_html(driver.page_source)
    insert_links_to_files(urls, 'yofreesamples')
    driver.close()


def readfile(filename):
    with open(filename, 'r', encoding='utf-8') as fd:
        return fd.readlines()


def get_files():
    valid_list = readfile(r'udemy_links/valid_links.txt')
    invalid_list = readfile(r'udemy_links/invalid_links.txt')
    unloaded_list = readfile(r'udemy_links/unloaded_links.txt')
    return valid_list, invalid_list, unloaded_list


def create_file(file_name):
    try:
        readfile(file_name)
    except:
        with open(file_name, 'w') as fd:
            pass


def create_dir_and_files():
    try:
        os.mkdir('udemy_links')
    except:
        pass
    create_file(r'udemy_links/valid_links.txt')
    create_file(r'udemy_links/invalid_links.txt')
    create_file(r'udemy_links/unloaded_links.txt')


def main():
    create_dir_and_files()
    while True:
        chooise = input('Enter the number of your chooise:\n'
                        '1. only telegram\n'
                        '2. only yofreesample\n'
                        '3. both\n')
        if chooise == '1':
            telegram()
            break
        if chooise == '2':
            yofreesamples()
            break
        if chooise == '3':
            telegram()
            yofreesamples()
            break


if __name__ == '__main__':
    main()
