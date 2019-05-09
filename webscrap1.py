# example from Udemy course learn web scraping with python from scratch, coded by me.
from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://boston.craigslist.org/search/sof"
npo_jobs = {}
job_no = 0
while True:
    response = requests.get(url)

    print(response)

    data = response.text

    print(data)

    soup = BeautifulSoup(data, 'html.parser')

    #display all links from webpage url
    #tags = soup.find_all('a')

    #for tag in tags:
    #    print(tag.get('href'))

    #titles = soup.find_all('a', {"class":"result-title"})
    #for title in titles:
    #    print(title.text);

    #addresses = soup.find_all('span', {'class':'result-hood'})

    #for address in addresses:
    #    print(address.text)

    jobs = soup.find_all('p', {'class':"result-info"})

    for job in jobs:
        title = job.find('a', {'class':'result-title'}).text
        location_tag = job.find('span', {'class':'result-hood'})
        location = location_tag.text[2:-1] if location_tag else 'N/A'
        date = job.find('time', {'class':'result-date'}).text
        link = job.find('a', {'class':'result-title'}).get('href')
        job_response = requests.get(link)
        job_data = job_response.text
        job_soup = BeautifulSoup(job_data, 'html.parser')
        job_description = job_soup.find('section', {'id':'postingbody'}).text
        job_attributes_tag = job_soup.find('p',  {'class':'attrgroup'})
        job_attributes = job_attributes_tag.text if  job_attributes_tag else "N/A"
    
        job_no += 1
        npo_jobs[job_no] = [title, location, date, link,  job_attributes, job_description]
    
        print('Job Title: ', title, '\nLocation: ', location, '\nDate: ', date, '\nLink: ', link, '\nJob Description: ', job_description, '\nJob Attributes: ', job_attributes, '\n---\n')
    url_tag = soup.find('a', {'title': 'next page'})
    if url_tag.get('href'):
        url = 'https://boston.craigslist.org' + url_tag.get('href')
        print(url)
    else:
        break
npo_jobs_df = pd.DataFrame.from_dict(npo_jobs, orient = 'index', columns = ['Job Title', 'Location', 'Date', 'Link', 'Job Attributes', 'Job Description'])        
print("Number of jobs found: ", job_no)
npo_jobs_df.to_csv('npo_jobs.csv')