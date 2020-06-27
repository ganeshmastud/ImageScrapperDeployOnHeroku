import os
import time
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui

from getpass import getpass 



# Determines if the page is loaded yet.
def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") != None


def save_img(img,target_path,cnt,search_term):
	target_folder= os.path.join(target_path, '_'.join(search_term.lower().split()))
	if not os.path.exists(target_folder):
		os.makedirs(target_folder)
		
	try:
		image_content = requests.get(img).content

	except Exception as e:
		print(f"ERROR - Could not download {img} - {e}")
	try:
		f = open(os.path.join(target_folder, search_term + "_" + str(cnt) + ".jpg"), 'wb')
		f.write(image_content)
		f.close()
		print(f"SUCCESS - saved {img} - as {target_folder}")
	except Exception as e:
		print(f"ERROR - Could not save {img} - {e}")


def get_pic(valid_urls, driver):
	print("hey")
	get_pic_counter = 0
	final_urls=set()
	time.sleep(5)
	print(len(valid_urls))
	while (get_pic_counter < len(valid_urls)):
		print(0)
		# Now, we can just type in the URL and pinterest will not block us
		for urls in valid_urls:
			driver.get(urls)

			# Wait until the page is loaded
			if driver.current_url == urls:
				wait = ui.WebDriverWait(driver, 10)
				wait.until(page_is_loaded)
				loaded = True
			print(1)
			# -----------------------------------EDIT THE CODE BELOW IF PINTEREST CHANGES---------------------------#
			# Extract the image url
			soup = bs(driver.page_source, "html.parser")
			print(2)
			for mainContainer in soup.find_all('div', {'class': "mainContainer"}):
				print(3)
				for closeupContainer in mainContainer.find_all('div', {'class': "closeupLegoContainer"}):
					print(4)
					# for heightContainer in closeupContainer.find_all("div", {"class": "FlashlightEnabledImage Module"}):
					print(5)
					for img in closeupContainer.find_all("img"):
						print(6)
						print("hello")
						img_link = img.get("src")
						if "564" in img_link:
							print("found the img url of: " + str(get_pic_counter))
							get_pic_counter += 1
							final_urls.add(img_link)
							break
	return final_urls

def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
def create_url(url):
	url=url.split()
	url="+".join(url)
	return url

def download_url(search_term):
	
	wait = ui.WebDriverWait(driver, 30)
	wait.until(page_is_loaded)
	
	x=driver.find_elements_by_class_name("zI7 iyn Hsu")   
	print(x)
	find_search= driver.find_element_by_name("searchBoxInput").send_keys(search_term, Keys.ENTER)#SearchBoxInputExperimental
	#find_search.submit()  
	#url="https://in.pinterest.com/search/pins/?q="
	#driver.get(url)
	
	image_urls = set()
	list_counter = 0
	
	beginning = time.time()
	end = time.time()
	while list_counter < 10 and beginning - end < 30:
		beginning = time.time()
		
		soup=bs(driver.page_source, "html.parser")
		for pinLink in soup.find_all("div", {"class": "Yl- MIw Hb7"}):
			for a in pinLink.find_all("a"):
				print(pinLink)
				url = ("https://pinterest.com" + str(a.get("href")))
				print(url)
				if len(url) < 60 and url not in image_urls and "A" not in url:
					
					image_urls.add(url)
					print("found the detailed page of: " + str(list_counter))
					list_counter += 1
					end = time.time()
				time.sleep(.15)
					
			driver.execute_script("window.scrollBy(0,50)")
	'''
	tag_a=x.find_element_by_tag_name('a')
	max_img=50
	
	img_count = 0
	print(f"Found: {tag_a} search results.")
	
	while img_count <= max_img:
		
		for image in tag_a:
			img_count+=1
			print(image.get_attribute('href'),img_count)
			image_urls.add(image.get_attribute('href'))
	'''	
	return image_urls


def fetch_img(search_term,target_path):
	folder_name = target_path
	file = search_term
	img_folder = folder_name + '/' + file
	list_of_folders = os.listdir(folder_name)
	list_ofimgs = []
	for i in list_of_folders:

		if i == file:
			images = os.listdir(img_folder)
			for j in images:
				list_ofimgs.append(j)
	if len(list_ofimgs)==0:
		return 0
	
	
def login(driver,username,password, search_term):
	driver.get("https://www.pinterest.com/login/?referrer=home_page")     # first perofming login for website access
	username_textbox=driver.find_elements_by_id("email")[0]				#retrive email id container 
	username_textbox.send_keys(username)								#passing user name to usernametextbox
	pass_textbox=driver.find_elements_by_id("password")[0]					#same for password
	pass_textbox.send_keys(password)
	pass_textbox.submit()	
	#login_button=driver.find_element_by_class_name("red SignupButton active")
	#login_button.submit()												#submiting the deatils
	print("Sucessfully login")
	time.sleep(5)
	
	term=create_url(search_term)
	
	img_urls=download_url(term)
	res=get_pic(img_urls, driver)
	target_path='./static'
	cnt=0
	for img in res:
		save_img(img,target_path,cnt,search_term)
		cnt+=1
	list_imgs = fetch_img(search_term, target_path)
	return list_imgs



search_term=input("Enter the image that you want to download:")
username=input("Enter your user name:")#"mastudganesh6@gmail.com"#
password=getpass("Enter your password:")#"ganesh@1"#

driver=webdriver.Chrome()
driver.delete_all_cookies() 
login(driver, username, password,search_term)





