from selenium import webdriver
from selenium.webdriver.support.ui import Select
import lxml.html as lh
import csv,time
import datetime
import pandas as pd
from pyvirtualdisplay import Display	
display = Display(visible=0, size=(800, 600))
display.start()

browser = webdriver.Firefox()
#browser = webdriver.Chrome(executable_path='/home/nv/Downloads/chromedriver_linux64/chromedriver')
browser.get('https://timetables.qmul.ac.uk')
browser.implicitly_wait(30)
python_button = browser.find_element_by_id('LinkBtn_modules') 
python_button.click()
browser.implicitly_wait(30)


select = Select(browser.find_element_by_id('dlObject'))

# select by value 
# select.select_by_value('BDS4004-A19')
# select.select_by_value('BIO227-A19')
# select.select_by_value('BIO723P-A19')
# select.select_by_value('BUS204-A19')
select.select_by_value('ECS7002P-A19')
select.select_by_value('ECS766P-A19')
select.select_by_value('ECS763P-A19')
select.select_by_value('ECS708P-A19')
select.select_by_value('ECS751P-C19')
# dlType
select = Select(browser.find_element_by_id('dlType'))

# select by value 
select.select_by_visible_text('List Timetable')
#bGetTimetable
python_button = browser.find_element_by_id('bGetTimetable') 
python_button.click()

browser.implicitly_wait(30)

time.sleep(30)
doc = lh.fromstring(browser.page_source)
browser.close()
browser.quit()

display.stop()
col=[]
table_val=0


def next_weekday(weekday,d=datetime.datetime.today()):
	weekdayDict = {'Monday' : 0,'Tuesday' : 1,'Wednesday' : 2,'Thursday' : 3,'Friday' : 4,'Saturday' : 5,'Sunday' : 6}
	weekday = weekdayDict[weekday]
	days_ahead = weekday - d.weekday()
	if days_ahead <= 0: # Target day already happened this week
		days_ahead += 7
	dateValue = d + datetime.timedelta(days_ahead)
	return dateValue.strftime("%m/%d/%Y")

for i in range(1,25):	
	day_value = ''.join([i.text_content() for i in doc.xpath('/html/body/p['+str(i)+']')])	
	# /html/body/p[1] /html/body/table[2]
	# /html/body/p[6] /html/body/table[9]
	# /html/body/p[11] /html/body/table[16]
	# /html/body/p[16] /html/body/table[23]
	# /html/body/p[16] /html/body/table[23] 
	# /html/body/p[21] /html/body/table[31] 
	if i == 1:
		table_val = 2
	elif i == 6:
		table_val = 9
	elif i == 11:
		table_val = 16
	elif i == 16:
		table_val = 23
	elif i == 21:
		table_val = 31	
	else:
		pass
	# print(day_value,next_weekday(day_value),str(i),str(table_val)) 
	tr_elements = doc.xpath('/html/body/table['+str(table_val)+']/tbody')	 
	i=0
	# col=[]
	if tr_elements:
		for t in tr_elements[0]:
			i+=1
			name=t.text_content()
			#print(name)
			if 'Module:' in name or 'Weeks:'  in name or 'Description'  in name: 
				pass
			else:
				col.append((name.split('\n')+[next_weekday(day_value)]))
	table_val =table_val+1


print(col)
columns=['X','Activity','Description','Type','Start','End','Week(s)', 'Room', 'Staff','Y','Date']
df = pd.DataFrame.from_records(col,columns=columns)
# Subject,Start Date,Start Time,End Date,End Time,All Day Event,Description,Location,Private
# ECS7002P/A/Lecture,Monday, 	12:00,Monday,  	14:00, FALSE,"Artificial Intelligence in Games,Perez-Liebana, D",Location: Graduate Ctr:GC101,TRUE
columns = ['Subject','Start Date','Start Time','End Date','End Time','All Day Event','Description','Location','Private']
rows = []
for index, row in df.iterrows():
    rows.append([row['Activity'], row['Date'], row['Start'], row['Date'], row['End'], 'FALSE', row['Description'], row['Room'], 'TRUE' ])



df2 = pd.DataFrame(rows,columns=columns)
df2.to_csv('calendar'+str(datetime.datetime.today().strftime("%d-%m-%Y"))+'.csv',index = False)
