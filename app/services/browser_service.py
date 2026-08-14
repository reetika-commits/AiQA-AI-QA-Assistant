from selenium import webdriver

class BrowserService():
    def __init__(self):
        self.driver=webdriver.Chrome()
       
    def open_url(self,app_url):
        print(app_url)
        self.driver.get(app_url)

    def get_dom(self):
        return self.driver.page_source

    def take_screenshots(self,path):
        self.driver.save_screenshot(path)

    def get_page_text(self):
        return self.driver.find_element("tag name","body").text

    def close(self):
        self.driver.quit()