#!/WinPython/WinPython Interpreter
#Author: Christopher Shibles,
#Progress of script, code used as function ordersForced in forceOrders.pyw

from selenium import webdriver
from getpass import getpass
import time
import re
import datetime

now = datetime.datetime.now()
with open("errorsrecord.txt", "a") as myfile:
		myfile.write("BEGIN: %02d/%02d/%02d  %02d:%02d:%02d Script Launched \n" % (now.day, now.month, now.year, now.hour, now.minute, now.second))
		
		
daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

#Gathering information via input from user for logging into the workbench and what day needs to be printed
print("Please enter the requested information in the following prompts to login to the Manager's Workbench.")
print("Please enter your username for the Workbench: ")
usr = input()
#TODO: Install Chrome and Selenium on Flash Drive
print("Please enter your password for the Workbench (you will not see the text as you input): ")
pwd = getpass()

weekDay = "empty"

while weekDay not in daysOfWeek:
	print("Please enter the day of the week you wish to print for (format Sunday): ")
	weekDay = input()

filterBy = "//select[@name='filterBy']/option[text()='"+ weekDay + "']" #uses the weekDay input from user to create path string for later use


orderCount = 0 #to count number of orders forced over and printed to confirm at the end

#Kiosk printing allows for printing without having a print dialog open
chrome_options = webdriver.ChromeOptions() 
chrome_options.add_argument('--kiosk-printing')

driver = webdriver.Chrome(chrome_options=chrome_options) 
driver.get('https://workbench.shoprite.com/')
main_window = driver.window_handles[0]
driver.implicitly_wait(5)

usr_box = driver.find_element_by_id('username')
usr_box.send_keys(usr)

pwd_box = driver.find_element_by_id('password')
pwd_box.send_keys(pwd)

login_button = driver.find_element_by_name('submit')
login_button.submit()

html_source = driver.page_source
print("re.findall:")
print(re.findall("Login failed", html_source))

#checking if correct login information was entered

if re.findall("Login failed", html_source) == ["Login failed"]:
	print("Login credential incorrect. Please close this window, re-launch the shortcut, and try again.")
	now = datetime.datetime.now()
	with open("errorsrecord.txt", "a") as myfile:
		myfile.write("ERROR: %02d/%02d/%02d  %02d:%02d:%02d incorrect login credentials attempted by username %s \n" % (now.day, now.month, now.year, now.hour, now.minute, now.second, usr))
	exit()

now = datetime.datetime.now()	
with open("errorsrecord.txt", "a") as myfile:
	myfile.write("SUCCESS: %02d/%02d/%02d  %02d:%02d:%02d successful launch and login by username %s \n" % (now.day, now.month, now.year, now.hour, now.minute, now.second, usr))

#navigating to the correct page for forcing orders
orders_link = driver.find_element_by_xpath("//span[@id='storeMenu']/ul[@class='nav']/li[@class='dropdown']/a")
orders_link.click()
time.sleep(0.5)

#LOOP STARTS HERE
while 1 == 1:

	available_soon = driver.find_element_by_xpath("//select[@id='orderStatus']/option[@value='AvailableSoon']")
	available_soon.click()
	time.sleep(0.5)

	filter_by = driver.find_element_by_xpath(filterBy) #filterBy is a string with the path
	filter_by.click()
	time.sleep(0.5)



	html_source = driver.page_source
	if len(re.findall("There are no orders to display.", html_source)) == 4:
		print("There are no more orders")
		break

	order_id = driver.find_element_by_xpath("//td[@class='dateTimerow']")
	order_id.click()

	time.sleep(1)

	print_button = driver.find_element_by_id('printOrderSections')
	print_button.click()

	description_radio_button = driver.find_element_by_css_selector("input[type='radio'][name='printProductDescriptions'][value='0']")
	description_radio_button.click()
	print_order = driver.find_element_by_id('printOrderDetail')
	print_order.click()
	time.sleep(1)

	#Forcing Orders to Pending
	force_button = driver.find_element_by_id('ForceOrderToPendingButton')
	force_button.click()

	confirm_button = driver.find_element_by_id('ConfirmModalMessageOkButton')
	confirm_button.click()
	
	ok_button = driver.find_element_by_id('ModalButton')
	ok_button.click()

	orderCount =+ 1
#LOOP ENDS HERE

print("Printed and forced over " + str(orderCount) + " orders.")
now = datetime.datetime.now()
with open("errorsrecord.txt", "a") as myfile:
		myfile.write("END: %02d/%02d/%02d  %02d:%02d:%02d script finished running - %d orders forced \n" % (now.day, now.month, now.year, now.hour, now.minute, now.second, orderCount))

exit()