import requests,csv
import pandas as pd
from bs4 import BeautifulSoup
from rich.console import Console

console = Console()

URL = "https://members.phpmu.com/project"
PAGE = requests.get(URL)
soup = BeautifulSoup(PAGE.content,"html.parser")
result = soup
check_last_page = result.find("a",string='Last ›')['href']
last_page = check_last_page.split('/')[-1]

array = []

def scrapping(lastnumber):
    for x in range(0,int(lastnumber) + 10,10):
        URL = "https://members.phpmu.com/project/index/" + str(x)
        PAGE = requests.get(URL)
        soup = BeautifulSoup(PAGE.content,"html.parser")
        result = soup
        loop = result.find_all("div",class_='col-md-8')
        for i in loop:
            datalink = i.find("h1").a   
            console.print(f"Deskripsi : {i.find('p').text}\n",style="italic bright_white")
            console.print(f"Job : {datalink.text.strip()}",style="bold green")
            console.print(f"\nBudget : ",style="bold yellow")
            console.print(f"\nLink : {datalink['href']}\n",style="bold red")
            console.print(f"{i.find('div',class_='col-md-6').text}\n",style="bold red")
            console.print("===================================================\n",style="italic green")

            file_csv = {
                'job' : datalink.text.strip(),
                'link' : datalink['href'],
                'detail' : i.find('div',class_='col-md-6').text
            }
            array.append(file_csv)
    
scrapping(last_page)
df = pd.DataFrame(array)
df.to_csv("scrapping_memberphpmu.csv")
print("FINISH")
