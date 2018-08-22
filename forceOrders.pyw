#!/WinPython/WinPython Interpreter
#Author: Christopher Shibles, started August 1, 2018, finished August 16, 2018
from selenium import webdriver
from getpass import getpass
import time
import re
import datetime
from tkinter import Tk, Text, BOTH, TOP, X, N, LEFT, RIGHT
from tkinter.ttk import Frame, Button, Label, Entry

class Example(Frame):

	def __init__(self):
		super().__init__()   
		
		self.initUI()

		
	def initUI(self):
		
		self.master.title("Force Orders")
		self.pack(fill=BOTH, expand=True)
		
		frame1 = Frame(self)
		frame1.pack(fill=X)
		
		lbl1 = Label(frame1, text="Username", width=10)
		lbl1.pack(side=LEFT, padx=5, pady=5)           
		
		entry1 = Entry(frame1)
		entry1.pack(fill=X, padx=5, pady = 5, expand=True)
		
		frame2 = Frame(self)
		frame2.pack(fill=X)
		
		lbl2 = Label(frame2, text="Password", width=10)
		lbl2.pack(side=LEFT, padx=5, pady=5)
		
		entry2 = Entry(frame2, show="*")
		entry2.pack(fill=X, padx=5, expand=True)
		
		frame3 = Frame(self)
		frame3.pack(fill=BOTH, expand=True)
		
		lbl3 = Label(frame3, text="Day", width=10)
		lbl3.pack(side=LEFT, anchor=N, padx=5, pady=5)
		
		entry3 = Entry(frame3)
		entry3.pack(fill=X, padx=5, expand=True)
		
		frame4 = Frame(self)
		frame4.pack(fill=BOTH, expand=True)
		
		closeButton = Button(frame4, text="Close", command=self.quit)
		closeButton.pack(side=RIGHT, padx=5, pady=5)
		okButton = Button(frame4, text="OK", command=lambda: self.ordersForced(entry1.get(), entry2.get(), entry3.get())) #command to call ordersForced
		okButton.pack(side=RIGHT)
		
	def ordersForced(self, usrEntry, pwdEntry, weekDayEntry):	
	
		now = datetime.datetime.now()
		with open("errorsrecord.txt", "a") as myfile:
				myfile.write("BEGIN: %02d/%02d/%02d  %02d:%02d:%02d Script Launched \n" % (now.day, now.month, now.year, now.hour, now.minute, now.second))
				
				
		daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

		#Gathering information via input from user for logging into the workbench and what day needs to be printed
		usr = usrEntry
		pwd = pwdEntry
		weekDay = weekDayEntry
		
		if weekDay not in daysOfWeek:
			with open("errorsrecord.txt", "a") as myfile:
				myfile.write("Line 75 hit")
			exit()

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

		#checking if correct login information was entered

		if re.findall("Login failed", html_source) == ["Login failed"]:
			now = datetime.datetime.now()
			with open("errorsrecord.txt", "a") as myfile:
				myfile.write("ERROR: %02d/%02d/%02d  %02d:%02d:%02d incorrect login credentials attempted by username %s \n" % (now.day, now.month, now.year, now.hour, now.minute, now.second, usr))
			exit()

		now = datetime.datetime.now()	
		with open("errorsrecord.txt", "a") as myfile:
			myfile.write("SUCCESS: %02d/%02d/%02d  %02d:%02d:%02d successful launch and login by username %s \n" % (now.day, now.month, now.year, now.hour, now.minute, now.second, usr))
		
		
		url = driver.current_url
		while "Home" not in url:
			url = driver.current_url
		
		#navigating to the correct page for forcing orders
		orders_link = driver.find_element_by_xpath("//span[@id='storeMenu']/ul[@class='nav']/li[@class='dropdown']/a")
		orders_link.click()
		time.sleep(0.5)

		#LOOP STARTS HERE
		while 1 == 1:
			
			url = driver.current_url
			while "List" not in url:
				url = driver.current_url
			
			available_soon = driver.find_element_by_xpath("//select[@id='orderStatus']/option[@value='AvailableSoon']")
			available_soon.click()
			
			url = driver.current_url
			while "AvailableSoon" not in url:
				url = driver.current_url

			filter_by = driver.find_element_by_xpath(filterBy) #filterBy is a string with the path
			filter_by.click()
			
			url = driver.current_url
			while weekDay not in url:
				url = driver.current_url
			
			html_source = driver.page_source
			if len(re.findall("There are no orders to display.", html_source)) == 4:
				break

			order_id = driver.find_element_by_xpath("//td[@class='dateTimerow']")
			order_id.click()

			url = driver.current_url
			while "Detail" not in url:
				url = driver.current_url
			
			print_button = driver.find_element_by_id('printOrderSections')
			print_button.click()

			description_radio_button = driver.find_element_by_css_selector("input[type='radio'][name='printProductDescriptions'][value='0']")
			description_radio_button.click()
			print_order = driver.find_element_by_id('printOrderDetail')
			print_order.click()
			
			#Forcing Orders to Pending
			force_button = driver.find_element_by_id('ForceOrderToPendingButton')
			force_button.click()

			confirm_button = driver.find_element_by_id('ConfirmModalMessageOkButton')
			confirm_button.click()
			
			ok_button = driver.find_element_by_id('ModalButton')
			ok_button.click()
			time.sleep(1)
			

			orderCount += 1
		#LOOP ENDS HERE

		now = datetime.datetime.now()
		with open("errorsrecord.txt", "a") as myfile:
				myfile.write("END: %02d/%02d/%02d  %02d:%02d:%02d script finished running - %d orders forced \n" % (now.day, now.month, now.year, now.hour, now.minute, now.second, orderCount))

		exit()

def main():
  
	root = Tk()
	root.geometry("300x130+300+300")
	root.resizable(0,0)
	app = Example()
	root.mainloop()  


if __name__ == '__main__':
    main() 