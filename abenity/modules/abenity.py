# Import necessary libraries
import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from azure.storage.blob import BlobServiceClient
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
abenity_username = config.get('production','abenity_username')
abenity_password = config.get('production','abenity_password')
azure_storage_account_name = config.get('production','azure_storage_account_name')
azure_storage_account_key = config.get('production','azure_storage_account_key')

class Abenity:
    def __init__(self) -> None:
        pass

    def getCromDriver(self):
        URL = "https://backoffice.abenity.com/account/members/export"
        # Set up Chrome options for file download
        options = Options()
        # prefs = {"download.default_directory": "/member_export"}
        prefs = {"download.default_directory": r"/home/ubuntu/abenity - automation/member_export"}
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("detach", True)
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        # Set up the Chrome WebDriver with the specified options
        service = Service(executable_path='./chromedriver-linux64/chromedriver')
        # service = Service(executable_path=r'G:\My Drive\0PI_PROJECTS\Yuya Omari\Abenity - Automation\chromedriver\chromedriver.exe')
        driver = webdriver.Chrome(options=options,service=service)
        return driver

    def getMemberList(self):
        URL = "https://backoffice.abenity.com/account/members/export"
        driver = self.getCromDriver()
        # Maximize the browser window
        driver.maximize_window()
        # Access the specified URL
        driver.get(URL)
        # Sleep for a random time between 8 and 10 seconds
        time.sleep(random.randint(8, 10))
        # Locate the username input field by ID and enter the username
        driver.find_element(By.ID, "username").send_keys(abenity_username)
        # Sleep for a random time between 1 and 3 seconds
        time.sleep(random.randint(1, 3))
        # Locate the password input field by ID and enter the password
        driver.find_element(By.ID, "password").send_keys(abenity_password)
        # Sleep for a random time between 2 and 5 seconds
        time.sleep(random.randint(2, 5))
        # Locate and click the submit button by ID
        driver.find_element(By.ID, "submit_form").click()
        # Sleep for a random time between 3 and 5 seconds
        time.sleep(random.randint(3, 5))
        # Locate and click the submit button with class name "submit"
        driver.find_element(By.CLASS_NAME, "submit").click()
        # Sleep for a random time between 5 and 10 seconds
        time.sleep(random.randint(5, 10))
        # Visit the logout URL
        driver.get('https://backoffice.abenity.com/process/logout')
        # Close the Chrome WebDriver
        driver.close()
        print('COMPLETED')

    def uploadMemberListToBlob(self):
        blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName="+azure_storage_account_name+";AccountKey="+azure_storage_account_key+";EndpointSuffix=core.windows.net")
        container_name = 'abenity'
        item = "members.csv"
        blob_client = blob_service_client.get_blob_client(container_name, item)
        with open(
                    os.path.abspath(os.path.join(r"/home/ubuntu/abenity - automation/member_export/", item)), "rb"
                ) as data:
                    try:
                        blob_client.upload_blob(data,overwrite=True)
                    except Exception as e:
                        print("Error....uploadMemberListToBlob")
                        print(e)
        data.close()
        blob_client.close()
        blob_service_client.close()
        


   