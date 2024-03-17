"""  CONTEST RANKING GENERATOR - GENERATES LEETCODE RANKINGS  """

import os
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
def extract_first_number(input_string):
    # Use regular expression to find the first occurrence of a number in the string
    match = re.search(r'\d+', input_string)
    
    if match:
        return int(match.group())  # Convert the matched string to an integer
    else:
        return None  
def extract_numbers(input_string):
    if input_string=="NA":
         return input_string
    numbers = re.findall(r'\d+', input_string)
    return ','.join(numbers)

def get_problem_count(profile_link):
     try:
          print(profile_link.strip())
          response=requests.get(profile_link.strip())
          soup=BeautifulSoup(response.content,'html.parser')
          v=soup.find_all('div')
     
          easy,medium,hard,total,rating="NA","NA","NA","NA","NA"
          contest_attended,contest_ranking="NA","NA"

          if 'Contest' and 'Rating' and "Attended" in v[0].text :
               contest_attended=v[0].text.split("Attended")[1].split("Solved")[0]
               contest_attended= extract_first_number(contest_attended)
               contest_ranking=v[0].text.split("Rating")[-1].split("Global")[0]
               
          for i in v:
               print(i)
               if 'Easy' in i.text and 'Medium' in i.text and 'Hard' in i.text:
                    easy=i.text.split('Easy')[-1].split('/')[0]
                    medium=i.text.split('Medium')[-1].split('/')[0]
                    hard=i.text.split('Hard')[-1].split('/')[0]
                    total=int(easy)+int(medium)+int(hard)
                    rating=i.text.split("Community")[0].split("Rank")[-1]
                    for j in range(0,len(rating)):
                         if rating[j]==',':
                              continue
                         if ord(rating[j])-ord('0')>9:
                              rating=rating[:j]
                              break
                         
                    if len(rating)==0:
                         rating=0
                    break

               
          
          return rating,easy,medium,hard,total,contest_attended,contest_ranking
     except:
          return  "NA","NA","NA","NA","NA","NA","NA"
    

# Define the path to the local Excel sheet
local_excel_file = r"NEW TEMPLATES\Batch_21_25 11-03-2024.xlsx"

cnt=0

if __name__ == "__main__":
    # Read the local Excel sheet using pandas
    df = pd.read_excel(local_excel_file)
     #print(df['Leetcode Profile Link'])
    print(len(df))

    for ctr in range(len(df)):
        profile_link = df.at[ctr, 'Leetcode Profile Link']
        if pd.notna(profile_link) and profile_link != '':
            time.sleep(3)
            rating, easy, medium, hard, total, contest_attended, contest_ranking = get_problem_count(profile_link)
            contest_ranking=extract_numbers(contest_ranking)
            print(cnt,"of",len(df),contest_attended,contest_ranking)
            cnt+=1
          #Update the values in the local Excel sheet
            df.at[ctr, 'Global Rating'] = rating
            df.at[ctr, 'Easy'] = easy
            df.at[ctr, 'Medium'] = medium
            df.at[ctr, 'Hard'] = hard
            df.at[ctr, 'Total Solved'] = total
            df.at[ctr, 'Contest Attended'] = contest_attended
            df.at[ctr, 'Contest Rating'] = contest_ranking
            df.to_excel(local_excel_file, index=False)
