import time
import csv
import configparser

class ChromeDriverPath:
    def __init__(self):
        # OSの判定
        import os
        def get_midpath():
            if (os.name == 'nt'):
                # Windows
                return '\\chromedriver_win32\\chromedriver.exe'
            if (os.name == 'posix'):
                # MacOS
                return '\\chromedriver_mac64\\chromedriver'
        # chromeのバージョン判定
        import iniclient as ini
        config = ini.Config()
        chrome_ver = config.get_version()
        self.driver_path = 'chromedriver\\' + chrome_ver[:2] + get_midpath()
    
    def get_driver_path(self):
        return self.driver_path

#ASIN、商品名のリスト
class Itemlist:
    def __init__(self, list1, list2):
        self.asinlist = list1
        self.namelist = list2
    def get_Itemlist(self):
        itemlist = []
        for i in range(len(self.asinlist)):
            items = {'asin': self.asinlist[i], 'product_name': self.namelist[i]}
            itemlist.append(items)
        return itemlist

def invoke(driver, sellerid, loop, wait_sec, headless):
    def go_nextpg(driver):
        next_elem = driver.find_element_by_class_name('a-last')
        next_elem.click()

    def search(driver):
        asinlist = []
        elems_asin = driver.find_elements_by_class_name('s-result-item.s-asin')
        for elem in elems_asin:
            asin = elem.get_attribute("data-asin")
            asinlist.append(asin)
        namelist = []
        elems_name = driver.find_elements_by_class_name('a-size-medium.a-color-base.a-text-normal')
        for elem in elems_name:
            namelist.append(elem.text)
        itemlist = Itemlist(asinlist, namelist)
        return itemlist.get_Itemlist()

    filename = 'data/' + sellerid + '.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['asin', 'product_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        last_item = ''
        for i in range(loop):
            time.sleep(wait_sec)
            print(str(i + 1) + 'ページ目を検索中...')
            itemlist = search(driver)
            if (last_item == itemlist[-1]):
                print('同一ページの繰り返しのため検索を終了します。')
                break
            try:
                writer.writerows(itemlist)
            except UnicodeEncodeError:
                print('無効な文字列を発見しました')
            last_item = itemlist[-1]
            itemlist.clear()
            go_nextpg(driver)

def execute(sellerid, loop, headless):
    from selenium import webdriver
    cdp = ChromeDriverPath()
    if headless == True:
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=options, executable_path=cdp.get_driver_path())
    else:
        driver = webdriver.Chrome(executable_path=cdp.get_driver_path())
    driver.get('https://www.amazon.co.jp/s?i=merchant-items&me=' + sellerid)
    try:
        invoke(driver=driver, sellerid=sellerid, loop=loop, wait_sec=1.1, headless=headless)
    except PermissionError:
        print('csvファイルの書き込みに失敗しました。別のプログラムでファイルを開いています。')
    driver.quit()

def remove_file(filekey):
    import os
    path = 'data/' + filekey + '.csv'
    os.remove(path)

# if __name__ == "__main__":
#     execute(sellerid='A27252DAP8H3K8', loop=3, headless=False)