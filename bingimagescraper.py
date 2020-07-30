import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import shutil
import os

# See Browser:
# PATH = "C:\Program Files (x86)\chromedriver.exe"
# driver = webdriver.Chrome(PATH)

# Invisible Browser:
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

def userinput():
	# Prompt user to input search criteria
	global searchparam 
	searchparam = input("What are you wanting to search for? ")
	global fformat 
	fformat = input("What format do you want scraped (jpg or gif)? ")

	while True:
		global ss 
		ss = input("Do you want SafeSearch enabled? ").capitalize()
		if ss == "Y" or ss == "N":
			break

def dircreation():
	# variables
	global splist 
	global abbrfile
	global current_dir 
	global new_folder 

	# Create a unique name for the new directory and all the retrieved items by using the first and last index char
	splist = list(searchparam)
	abbrfile = f"{splist[0]}{splist[-1]}" 

	# Open current directory, make new folder with the abbreviated name, switch to that folder
	current_dir = os.getcwd()
	new_folder = abbrfile
	if not os.path.isdir(new_folder):
		os.mkdir(new_folder)
	os.chdir(new_folder)

def searchsettings():
	# Search using moderate filter and enable Auto-play gifs
	if ss == "Y":
		time.sleep(6)
		driver.find_element_by_id("id_sc").click()
		time.sleep(3)
		driver.find_element_by_css_selector("#imgqs_gifToggle_ctrl > svg > circle").click

	# Turn off SafeSearch & enable auto-play gifs
	if ss == "N":
		time.sleep(6)
		driver.find_element_by_id("id_sc").click()
		time.sleep(3)
		driver.find_element_by_css_selector("#imgqs_gifToggle_ctrl > svg > circle").click
		time.sleep(1)
		driver.find_element_by_css_selector("#HBContent > a.hb_section.hbic_safesearch_row > div > div.hb_title_col").click()
		time.sleep(3)
		driver.find_element_by_css_selector("#adlt_set_off").click()
		time.sleep(1)
		driver.find_element_by_css_selector("#sv_btn").click()
		time.sleep(1)
		driver.find_element_by_css_selector("#adlt_confirm").click()
		time.sleep(2)

	# Adjust wait times for search to allow for more time if gifs are being retrieved
	global drop1
	if fformat == "gif":
		time.sleep(35)
		drop1 = 25
	else:
		drop1 = 6

def scriptrun():
	# variables
	global search 
	global imgs 

	# Go to the bottom of the search page
	html = driver.find_element_by_tag_name("html")
	html.send_keys(Keys.END)
	time.sleep(drop1)
	html.send_keys(Keys.END)
	time.sleep(drop1)
	html.send_keys(Keys.END)
	time.sleep(drop1)

	# Find image urls and store them in a list
	search = driver.find_elements_by_class_name("mimg")
	imgs = [l.get_attribute("src") for l in search if (l.get_attribute("src")) != None]

	driver.quit()

def formatimage():
	# variables
	global picnum 

	# Format urls into jpg or gif files, and save them in directory with the name: directory name + incremented numbers
	picnum = 0
	for i in imgs:
		urllib.request.urlretrieve(f"{i}", f"{abbrfile}{picnum}.{fformat}")
		picnum += 1


# Run Program

userinput()

dircreation()

browser = driver.get(f"https://www.bing.com/images/search?q={searchparam}")

searchsettings()

scriptrun()

formatimage()

# todo Lock this program from editing into a compiled .pyc
# script = "C:\\temp\\bingimagescraper.py"
# py_compile.compile(script)

print("Done!")