from selenium import webdriver
import requests

def get_links(url):
    """Find all links on page at the given url.
       Return a list of all link addresses, as strings.
    """
    browser = webdriver.Chrome(executable_path='/Users/zexal/Downloads/chromedriver')
    browser.get(url)
    element = browser.find_elements_by_tag_name("a")
    links = [i.get_attribute('href') for i in element]
    browser.close()
    return links

def invalid_urls(urllist):
    invalid = []
    for links in urllist:
        head_request = requests.head(links)
        if head_request.status_code == 404:
            invalid.append(links)
    return invalid

if __name__ == '__main__':
    link = get_links('https://cpske.github.io/ISP/')
    for valid in link:
        print("Valid url: ", valid)
    invalid_list = invalid_urls(link)
    for invalid in invalid_list:
        print("Invalid url: ", invalid)
