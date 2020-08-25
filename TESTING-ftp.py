import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import ftplib
import os


class TestFiles(unittest.TestCase):

	#открытие сервера в браузере
	def test_open_ftp(self):
		driver=webdriver.Chrome()
		driver.get("ftp://speedtest.tele2.net/")
		self.assertEqual(bool(driver.find_element_by_id('parentDirLinkBox')), True, 'FTP-сервер не открыт')
		driver.close()

	#открытие страницы Upload
	def test_open_upload_page(self):
		driver=webdriver.Chrome()
		driver.get("ftp://speedtest.tele2.net/")
		driver.find_element_by_link_text('upload/').click()
		self.assertEqual(driver.current_url=="ftp://speedtest.tele2.net/upload/", True, 'Страница Upload не открывается')
		driver.close()

	#наличие ссылок на странице
	def test_find_files(self):
		driver=webdriver.Chrome()
		driver.get("ftp://speedtest.tele2.net/")
		files = ['1000GB','100GB','100KB','100MB','10GB','1GB','1KB','1MB','200MB','20MB','2MB','3MB','500MB','50GB','50MB','512KB','5MB']
		for name in files:
			self.assertEqual(bool(driver.find_element_by_link_text(name+".zip")), True, 'Элемент не найден')
		driver.close()

	#соответствие имени файла и ссылки
	def test_match_link_and_file(self):
		driver=webdriver.Chrome()
		driver.get("ftp://speedtest.tele2.net/")
		files = ['1000GB','100GB','100KB','100MB','10GB','1GB','1KB','1MB','200MB','20MB','2MB','3MB','500MB','50GB','50MB','512KB','5MB']
		for name in files:
			link=driver.find_element_by_link_text(name+".zip").get_attribute("href")
			self.assertEqual(link=="ftp://speedtest.tele2.net/"+name+".zip", True, 'Имя файла и ссылка не соответствуют друг другу')
		driver.close()	

	#загрузка файла на ftp-сервер
	def test_upload_file(self):
		host = 'speedtest.tele2.net'
		ftp_user = "anonymous"
		ftp_password = "anonymous@"
		ftp = ftplib.FTP(host,ftp_user,ftp_password)
		ftp.cwd('/upload')
		file_to_upload = open('UPLOAD_FILE.zip', 'rb')
		self.assertEqual(bool(ftp.storbinary('STOR ' + 'UPLOAD_FILE.zip', file_to_upload)),True,'Файл не загружен')
		file_to_upload.close()
		ftp.quit()

	#отсутствие файла после загрузки
	def test_empty_directory(self):
		host = 'speedtest.tele2.net'
		ftp_user = "anonymous"
		ftp_password = "anonymous@"
		ftp = ftplib.FTP(host,ftp_user,ftp_password)
		ftp.cwd('/upload')
		file_to_upload = open('UPLOAD_FILE.zip', 'rb')
		ftp.storbinary('STOR ' + 'UPLOAD_FILE.zip', file_to_upload)
		self.assertEqual('UPLOAD_FILE.zip' in ftp.nlst(),False,'Директория не очищена')
		file_to_upload.close()
		ftp.quit()

	#загрузка файлов с ftp-сервера	
	def test_download_file(self):
		ChromeOptions=Options()
		ChromeOptions.add_experimental_option("prefs", { "download.default_directory": os.getcwd(),"download.directory_upgrade": True,})
		driver=webdriver.Chrome(chrome_options=ChromeOptions)
		driver.get("ftp://speedtest.tele2.net/")
		files = ['1000GB','100GB','100KB','100MB','10GB','1GB','1KB','1MB','200MB','20MB','2MB','3MB','500MB','50GB','50MB','512KB','5MB']
		for name in files:
			driver.find_element_by_link_text(name+".zip").click()
			time.sleep(2)
			self.assertEqual(os.path.exists(name+".zip.crdownload") or os.path.exists(name+".zip"),True,"Файл не скачен")
		driver.close()

if __name__ == '__main__':
    unittest.main()