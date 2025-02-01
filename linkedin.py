import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd

print("Please sign in to your Chrome profile manually.")
input("Press Enter after you have signed in...")

chromedriver_path = "C:/Users/SURESH PATEL/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:8901")

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get("http://linked.in")

print("Checking if you have already logged in into the linkedin\n")

soup = bs(driver.page_source,"html.parser")
startpage = soup.find('section',class_="section min-h-[560px] flex-nowrap pt-[40px] babybear:flex-col babybear:min-h-[0] babybear:px-mobile-container-padding babybear:pt-[24px]")
if startpage:
    print("you are not logged in into the linkedin")
        
    print("\nLogging you into the system, enter the option...")
    opt = input("1: log in with username and password\n2: log in manually\n")
    if opt == '1':
        if startpage:
            WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"""/html/body/nav/div/a[2]"""))).click()
            time.sleep(2)
            userprofile = soup.find('input',id="username")
            if not userprofile:
                print("you need to just enter the password")
                #password = input("\nEnter your password: ")
                
                passwordbox = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, """/html/body/div/main/div[3]/div[1]/div[3]/form/div[1]/input""")))
                passwordbox.send_keys("***")

                signinbutton = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"""/html/body/div/main/div[3]/div[1]/div[3]/form/div[2]/button"""))).click()
            else:
                print("you need to enter username and password")
                #username = input("\nEnter your phone or email:")
                
                usernamebox = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, """/html/body/div/main/div[2]/div[1]/form/div[1]/input"""))
                )
                usernamebox.send_keys("dhruvi0326@gmail.com")
                #password = input("\nEnter your password: ")
                passwordbox = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, """/html/body/div/main/div[2]/div[1]/form/div[2]/input"""))
                )
                passwordbox.send_keys("duruP@26")
            
                signinbutton = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"""/html/body/div/main/div[2]/div[1]/form/div[3]/button"""))).click()
            
            print("you're in")
        else:
            print("some issue occured while logging you in!")
    elif opt == '2':
        input("press enter after you have logged in")
        print("you're in")
    else:
        print("Some issue occured while logging you in!")

else:
    print("you are already logged in")

print("\n\nsearching...")

#searchquery = input("\nEnter any Designation/Skill/Job: ")
searchinputbox = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, """//html/body/div[4]/header/div/div/div/div[1]/input"""))
)
time.sleep(5)
searchinputbox.send_keys("media")
searchinputbox.send_keys(Keys.ENTER)
print("Searching done !!!")
time.sleep(3)
print(f"\nSearching all the people with the query -----")
people_button = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"""/html/body/div[4]/div[3]/div[2]/section/div/nav/div/ul/li[3]/button""")))
time.sleep(8)
people_button.click()
print("Searched people!")

print("\nExtracting the details...")
names = []
designations = []
locations = []

# Wait until people list is loaded
WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "reusable-search__result-container"))
)
time.sleep(3)  # Add an extra sleep to ensure everything is fully loaded

soup = bs(driver.page_source,"html.parser")

people_list = soup.find_all('li',class_="reusable-search__result-container")

for people in people_list:
    time.sleep(2)
    name = people.find('span',{'aria-hidden': 'true'})
    if name:
        names.append(name.get_text().strip())
    else:
        names.append("null")
    designation = people.find('div',class_="entity-result__primary-subtitle t-14 t-black t-normal")
    if designation:
        designations.append(designation.get_text().strip())
    else:
        designations.append("null")
    location = people.find('div',class_="entity-result__secondary-subtitle t-14 t-normal")
    if location:
        locations.append(location.get_text().strip())
    else:
        locations.append("null")

print("\nDesignations are... ")
for index,x in enumerate(designations):
    print(index,x)
print("\nLocations are... ")
for index,x in enumerate(locations):
    print(index,x)
print("\nNames are... ")
for index,x in enumerate(names):
    print(index,x)

#print(names)   

print("Extracted all!")

print("\nStarting with the companies section\n")
try:
    driver.back()
    print(f"went back to the previous page with the url: {driver.current_url}")
except:
    print("didn't not go to the previous page")

WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, """/html/body/div[4]/div[3]/div[2]/section/div/nav/div/ul"""))
)
time.sleep(3)
soup = bs(driver.page_source,"html.parser")
print("\nsearching all the companies related to your search query")
company_button = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"""/html/body/div[4]/div[3]/div[2]/section/div/nav/div/ul/li[5]/button""")))
#time.sleep(8)
company_button.click()
print("Searched companies!")     


company_titles = []
company_links = []
company_followers = []

# Pagination Handling
for page in range(1, 3):
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul"))
    )
    time.sleep(2)
    print(f"\nScraping page {page}: {driver.current_url}")
    soup = bs(driver.page_source, "html.parser")
    
    # Extract company details
    companies_list = soup.find_all('li', class_="reusable-search__result-container")
    for company in companies_list:
        title_element = company.find('a', class_="app-aware-link")
        if title_element:
            #company_titles.append(title_element.get_text().strip())
            company_links.append(title_element['href'])
        else:
            #company_titles.append("null")
            company_links.append("null")
        
        followers_element = company.find('div', class_="entity-result__secondary-subtitle t-14 t-normal")
        if followers_element:
            company_followers.append(followers_element.get_text().strip())
        else:
            company_followers.append("null")
    
    # Pagination Handling
    try:
        time.sleep(4)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        next_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next']"))
    )
        next_button.click()
        #print("Successfully clicked the 'Next' button")
    
    except Exception as e:
        print(f"No more pages to scrape. Scraped {page} pages. Error: {e}")
        break

company_contacts = []
company_industry_type = []
company_headquaters = []
company_size = []
company_description = []
company_specialties = []


for url in company_links:
    time.sleep(1)
    if url == "null":
        company_contacts = "null"
        company_industry_type = "null"
        company_headquaters = "null"
        company_size = "null"
        company_titles = "null"
    driver.get(url)
    soup = bs(driver.page_source,"html.parser")
    
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"""/html/body/div[4]/div[3]/div/div[2]/div/div[2]/main/div[1]/section/div/div[2]/div[2]/div[1]""")))   #this is the top heading box
    time.sleep(2)
    topheadingbox = soup.find('div',class_="org-top-card__primary-content org-top-card-primary-content--zero-height-logo org-top-card__improved-primary-content--ia")
    if topheadingbox:
        namebox = topheadingbox.find('div',class_="block mt2").find('h1')
        if namebox:
            company_titles.append(namebox.get_text().strip())
        else:
            company_titles.append("null")
        
        descriptionbox = topheadingbox.find('p',class_="org-top-card-summary__tagline")
        if descriptionbox:
            company_description.append(descriptionbox.get_text().strip())
        else:
            company_description.append("null")
        
        detailsbox = topheadingbox.find('div',class_="org-top-card-summary-info-list")
        
        industry_name = detailsbox.find('div',class_="org-top-card-summary-info-list__info-item")
        if industry_name:
            company_industry_type.append(industry_name.get_text().strip())
        else:
            company_industry_type.append("null")
        
        subdetailsbox = detailsbox.find('div',class_="inline-block")
        sub = subdetailsbox.find_all('div',class_="org-top-card-summary-info-list__info-item")
        if sub[0]:
            company_headquaters.append(sub[0].get_text().strip())
        else:
            company_headquaters.append("null")
        size = subdetailsbox.find('a').find('span',class_="t-normal t-black--light link-without-visited-state link-without-hover-state")
        if size:
            company_size.append(size.get_text().strip())
        else:
            company_size.append("null")
            
        showdetails_button = soup.find('a',class_="ember-view full-width text-align-center link-without-hover-visited org-module-card__footer-hoverable pv4")
        if showdetails_button and 'href' in showdetails_button.attrs:
            joburl = showdetails_button['href']
            showdetailsurl = f"https://www.linkedin.com{joburl}"
            #print(showdetailsurl)
        driver.get(showdetailsurl)
        soup = bs(driver.page_source,"html.parser")
        time.sleep(2)
        phone = "null"
        special = "null"  
        dl_elements = soup.find_all('dl',class_="overflow-hidden")
        
        '''dt_elements = dl_elements.find_all('dt')
        for x in dt_elements:
            dt_text = x.get_text().strip()
            if dt_text == 'Phone':
                dd_element = x.find_next_sibling("dd")
                if dd_element:
                    dd_text = dd_element.get_text().strip()
                    phone = dd_text
                else:
                    phone = "null"
            else:
                phone = "null"
            if dt_text == "Specialties":
                dd_element = x.find_next_sibling("dd")
                if dd_element:
                    dd_text = dd_element.get_text().strip()
                    special = dd_text
                else:
                    special = "null"
            else:
                special = "null"
        '''       
        
        '''for dl in dl_elements:
            dt_elements = dl.find_all('dt')
            dd_elements = dl.find_all('dd')
            for dt, dd in zip(dt_elements, dd_elements):
                dt_text = dt.get_text(strip=True)
                dd_text = dd.get_text(strip=True)
                if dt_text == 'Phone':
                    phone = dd_text
                else:
                    phone = "null"
                if dt_text == 'Specialties':
                    special = dd_text
                else:
                    special = "null"
        '''
        
        for dl in dl_elements:
            dt_elements = dl.find_all('dt')
            for dt  in dt_elements:
                dt_text = dt.get_text(strip=True)
                if dt_text == 'Phone':
                    dd_element = dt.find_next_sibling('dd')
                    if dd_element:
                        dd_text = dd_element.get_text().strip()
                        phone = dd_text
                    else:
                        phone = "null"
                else:
                    phone="null"
                if dt_text == 'Specialties':
                    dd_element = dt.find_next_sibling('dd')
                    if dd_element:
                        dd_text = dd_element.get_text().strip()
                        special = dd_text
                    else:
                        special = "null"
                else:
                    special="null"
        
        company_contacts.append(phone)
        company_specialties.append(special)
    else:
        company_industry_type.append("null")
        company_contacts.append("null")
        company_description.append("null")
        company_headquaters.append("null")
        company_size.append("null")
        company_specialties.append("null")
        
        
print("scraped out each job details also")

print("\ncompanies are... ")
for index,x in enumerate(company_titles):
    print(index,x)
print("\ncompany followers are... ")
for index,x in enumerate(company_followers):
    print(index,x)
print("\ncompany description are... ")
for index,x in enumerate(company_description):
    print(index,x)
print("\ncompany urls are... ")
for index,x in enumerate(company_links):
    print(index,x)
print("\ncompany size are... ")
for index,x in enumerate(company_size):
    print(index,x)
print("\ncompany's industry type are... ")
for index,x in enumerate(company_industry_type):
    print(index,x)
print("\ncompany headquaters are... ")
for index,x in enumerate(company_headquaters):
    print(index,x)
print("\ncompany contacts are... ")
for index,x in enumerate(company_contacts):
    print(index,x)
print("\ncompany specialties are... ")
for index,x in enumerate(company_specialties):
    print(index,x)

print("\nExtracted all the details")

print("success") 
