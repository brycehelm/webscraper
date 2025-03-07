
Web Scraper README

----------Overview-----------
This Python script crawls a specified website, extracts page titles and cleaned text content, and generates a formatted Microsoft Word document (.docx) report. It’s designed to:

Start from a given URL and follow links within the same domain.
Save the scraped data into a Word document with a title page and individual page sections.
Log the crawling process for debugging and tracking.
The script is ideal for archiving website content in a readable, professionally formatted document.

---------Requirements--------
To run this script, you’ll need the following:


----------Software-----------
Python 3.6 or higher: The script uses modern Python features and libraries.
pip: Python’s package manager (usually included with Python).
Python Libraries
requests: For fetching web pages.
beautifulsoup4: For parsing HTML and extracting text.
python-docx: For creating and formatting the Word document.
lxml (optional): Recommended parser for BeautifulSoup for better performance.


--------Installation---------
Install Python: Download and install Python from python.org if it’s not already on your system. Verify with:
bash

python --version
or
bash

python3 --version
Install Dependencies: Open a terminal or command prompt and run:
bash

pip install requests beautifulsoup4 python-docx
Optionally, install lxml for faster parsing:
bash

pip install lxml
Save the Script: Copy the script into a file named webscraper.py in your desired directory (e.g., C:\Users\brych\OneDrive\Documents\Python Scripts\WebSraper).


---------Usage---------------
Run the script from the command line by providing a starting URL.

Command
bash

python webscraper.py <url>
Examples
Scrape https://trove.cyberskyline.com/:
bash

python webscraper.py https://trove.cyberskyline.com/
Scrape example.com (assumes HTTPS):
bash

python webscraper.py example.com


------------Notes------------
The URL can be provided with or without http:// or https://. If omitted, the script defaults to https://.
Use Ctrl+C to stop the script early; it will save the collected data to the Word document before exiting.


-----------Output------------
The script generates two files in the same directory as webscraper.py:

Word Document: <domain>_report.docx
File Name: Based on the domain (e.g., trove.cyberskyline.com_report.docx).
Structure:
Title Page: Centered text: "Web Scraping Report for [Domain]" (16pt, bold) and "Generated on [Date]" (12pt).
Page Sections: One per scraped page, with:
Header: Page title (or URL if no title), formatted as Heading 1.
Body: Cleaned text content in 12pt Times New Roman, justified.
Each section separated by a page break.
Content: Saved at the end of the crawl or when interrupted.
Log File: <domain>_crawl.log
File Name: Based on the domain (e.g., trove.cyberskyline.com_crawl.log).
Content: Logs the crawl process with timestamps, including:
Start of crawl.
Each URL fetched and the number of discovered URLs.
Errors (e.g., failed fetches).
Completion or interruption messages.


----------Customization------
Max Pages: Adjust max_pages in the crawl() call (default: 1000) to limit how many pages are scraped.
Initial Batch Size: Change initial_batch_size (default: 5) if you want to tweak when logging becomes more verbose (though this doesn’t affect .docx saving in this version).
Formatting: Edit save_to_docx() to change fonts, sizes, or alignments (e.g., body.style.font.name = 'Arial').
Delay: Modify time.sleep(2) in crawl() to speed up (e.g., 1 or 0.5) or slow down the crawl rate.


-------Troubleshooting-------
No Output Files:
Ensure all dependencies are installed.
Check if the script completed or was interrupted cleanly (look for Crawl completed or KeyboardInterrupt in the log).
Empty Document:
The site might use JavaScript for content. Try a smaller site first (e.g., https://example.com) or consider using Selenium (requires additional setup).
Errors in Log:
Failed to fetch: Check internet connection or if the site blocks scraping (e.g., with a 403 status).
KeyboardInterrupt: Normal if you stopped it; data should still be saved.
Memory Issues: For large sites, lower max_pages to avoid excessive memory use.


----------Limitations--------
Static Content Only: The script uses requests, so it can’t scrape JavaScript-rendered content. Use Selenium for dynamic sites.
Single Save: The Word document is written once at the end or on interrupt, not incrementally during the crawl.
Domain Restriction: Only follows links within the starting domain (e.g., trove.cyberskyline.com/*).


-----------License-----------
This script is provided as-is for personal use. Modify and distribute as needed, but respect the terms of the scraped website.