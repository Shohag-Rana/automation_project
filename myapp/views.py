from selenium import webdriver
import csv
import time
from selenium.webdriver.common.by import By


class Class1:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def disp_class1(self):
        self.driver.get("https://www.bedroomvillas.com/all/usa/florida")
        self.driver.close()
