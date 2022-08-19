from lxml import etree
import sys
import optparse
import os
import requests
import time
import exif
import os


class DownloadExtractImages:
    def __init__(self) -> None:
        self.url = self.get_params()
        self.header = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
        }
        self.image_links = []

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -u url' % sys.argv[0])
        parser.add_option('-u', '--url', dest='url', type='string', help='Specify url to crawl images')
        options, args = parser.parse_args()
        if options.url is None:
            print(parser.usage)
            sys.exit()
        return options.url
    
    def make_store_dir(self):
        if not os.path.exists('images'):
            os.mkdir('images')
            print("[-] Created directory successfully")
    
    def retrieve_page(self, url):
       
        try:
            response = requests.get(url=url, headers=self.header )
        
            if response.status_code == 200:
                return response               

        except Exception as e:
            print(e)
            return False

    def find_image_links(self,response):
        html = etree.HTML(response.text)
        image_links = html.xpath('//img')
        if image_links:
            for each in image_links:
                image_url = each.xpath('./@src')[0]
                # print(image_url)
                if image_url.startswith('/'):
                    image_url = self.url + image_url
                # print(image_url)
                if image_url.endswith('.jpg') or image_url.endswith('.png'):
                    self.image_links.append(image_url)
    
    def store_image(self, filename, response):
        with open('images/'+filename, 'wb') as f:
            f.write(response.content)
            print('[-] Saved image successfully: %s' % filename)
    
    def extract_exif_image(self, filepath):
        with open(filepath, 'rb') as f:
            image_info = exif.Image(f)
            if image_info.has_exif:
                exif_data_list = image_info.list_all()
                for each in exif_data_list:
                    print(each,' : ',image_info.each)
            else:
                print('[-] THe image has not exif data: %s' % filepath)
    
    def run(self):
        self.make_store_dir()
        response = self.retrieve_page(self.url)
        if not response:
            print('[-] Failed to retrieve the web page: %s' % self.url)
        else:
            # print(response.text)
            self.find_image_links(response)
            if len(self.image_links) == 0:
                print('[-] No image found on the page')
            else:
                for link in self.image_links:
                    image_content = self.retrieve_page(link)
                    if image_content:
                        self.store_image(link.split('/')[-1],image_content)
                        print(link.split('/')[-1])
                        self.extract_exif_image('images/'+link.split('/')[-1])
                        time.sleep(2)

if __name__ == '__main__':
    extractor = DownloadExtractImages()
    extractor.run()

    

        

