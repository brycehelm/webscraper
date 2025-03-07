import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from collections import deque
import logging
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

# Configure logging
def setup_logging(base_domain):
    log_file = f"{base_domain}_crawl.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return log_file

def crawl(start_url, base_domain, max_pages=1000, initial_batch_size=5):
    def is_valid_url(url, visited_set):
        parsed = urlparse(url)
        return parsed.netloc == base_domain and url not in visited_set

    queue = deque([start_url])
    visited = set()
    discovered_urls = set([start_url])
    content_list = []  # To store scraped data

    logging.info(f"Starting crawl from {start_url} with max_pages={max_pages}")

    try:
        while queue and len(discovered_urls) < max_pages:
            url = queue.popleft()
            if url in visited:
                logging.debug(f"Skipping already visited URL: {url}")
                continue
            visited.add(url)

            logging.info(f"Fetching URL: {url} (Discovered: {len(discovered_urls)})")
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()

                if 'text/html' not in response.headers.get('Content-Type', ''):
                    logging.warning(f"Skipping non-HTML content at {url}")
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string if soup.title else url
                title = title.strip()

                # Extract and clean text
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text(separator=" ").strip()
                lines = (line.strip() for line in text.splitlines())
                text = " ".join(line for line in lines if line)

                # Store the data
                content_list.append({
                    'url': url,
                    'title': title,
                    'text': text
                })

                links_found = 0
                for link in soup.find_all('a', href=True):
                    absolute_url = urljoin(url, link['href'])
                    if is_valid_url(absolute_url, visited):
                        if absolute_url not in discovered_urls:
                            links_found += 1
                        discovered_urls.add(absolute_url)
                        if absolute_url not in visited:
                            queue.append(absolute_url)
                logging.debug(f"Found {links_found} new links on {url}")

            except requests.RequestException as e:
                logging.error(f"Failed to fetch {url}: {e}")
                content_list.append({
                    'url': url,
                    'title': 'Error',
                    'text': f"Failed to fetch content - {str(e)}"
                })

            time.sleep(2)

    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt detected. Saving collected content...")
        raise

    logging.info(f"Crawl completed. Processed {len(content_list)} pages.")
    return content_list

def save_to_docx(content_list, base_domain):
    doc = Document()

    # Title page
    title = doc.add_paragraph(f"Web Scraping Report for {base_domain}")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.runs[0].font.size = Pt(16)
    title.runs[0].font.bold = True

    subtitle = doc.add_paragraph(f"Generated on {time.strftime('%B %d, %Y')}")
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.runs[0].font.size = Pt(12)

    doc.add_page_break()

    # Content
    for entry in content_list:
        # Add header (page title or URL)
        header_text = entry['title'] if entry['title'] != 'Error' else entry['url']
        doc.add_heading(header_text, level=1)

        # Add body text
        body = doc.add_paragraph(entry['text'])
        body.style.font.size = Pt(12)
        body.style.font.name = 'Times New Roman'
        body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        doc.add_page_break()

    output_file = f"{base_domain}_report.docx"
    doc.save(output_file)
    logging.info(f"Saved report to {output_file}")
    return output_file

def main():
    if len(sys.argv) != 2:
        print("Usage: python webscraper.py <url>")
        print("Example: python webscraper.py example.com")
        sys.exit(1)

    input_url = sys.argv[1]
    if not input_url.startswith(('http://', 'https://')):
        start_url = f"https://{input_url}"
    else:
        start_url = input_url

    base_domain = urlparse(start_url).netloc
    log_file = setup_logging(base_domain)

    try:
        content_list = crawl(
            start_url=start_url,
            base_domain=base_domain,
            max_pages=1000,
            initial_batch_size=5
        )
    except KeyboardInterrupt:
        print("\nStopped by user.")
    else:
        print(f"\nCrawling complete. Processed {len(content_list)} pages.")

    # Save to Word document
    output_file = save_to_docx(content_list, base_domain)
    print(f"Report saved to {output_file}")
    print(f"Log saved to {log_file}")

if __name__ == "__main__":
    main()