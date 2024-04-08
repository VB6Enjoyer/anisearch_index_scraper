import requests
from bs4 import BeautifulSoup
import xlsxwriter
import re
import os

def scrape_anisearch():
    base_url = input("Enter the base URL (e.g., 'https://www.anisearch.com/anime/index/page-1'): ")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, "titles.xlsx")
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()
    
    i = 1
    page_number = 1
    pattern = r'page-\d+'
    first_anime = "";
    
    while True:
        url = re.sub(pattern, f'page-{page_number}', base_url)
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all <a> elements with class starting with "rbox"
            rbox_links = soup.find_all('a', class_=re.compile(r'^rbox'))
            
            if not rbox_links:
                print(f'No anime titles found on page {page_number}. Stopping scraping.')
                break  # No more <a> elements found, stop scraping
            
            anime_titles = [link.decode_contents() for link in rbox_links]
            if anime_titles[0] == first_anime: # Probably the simplest way to stop the loop from redirecting to page 1 past the last page. Not the most optimized, though.
                print("All done. " + str(i) + " titles saved to titles.xlsx")
                break;
            
            for title in anime_titles:
                worksheet.write("A" + str(i), title)
                if i == 1:
                    first_anime += title
                i += 1
            
            print("Page " + str(page_number) + " scraped successfully.")
            page_number += 1
            
        else:
            print(f'Failed to fetch aniSearch URL: {url}')
            break
    
    workbook.close()
    print(f'Anime titles scraped and saved to: {file_path}')

if __name__ == "__main__":
    scrape_anisearch()