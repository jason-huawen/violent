import requests
import sys
import optparse

class RequestMethodsTest:
    def __init__(self) -> None:
        self.url = self.get_params()
        self.methods_list = ['GET', 'POST', 'PUT', 'DELETE','OPTIONS', 'TRACE']

    def get_params(self):
        parser = optparse.OptionParser('Usage: ./%s -u url' % sys.argv[0])
        parser.add_option('-u', '--url', dest='url', type='string', help='Specify url to test')
        options, args = parser.parse_args()
        if options.url is None:
            print(parser.usage)
            sys.exit()

        return options.url
    

    def run(self):
        for req_method in self.methods_list:
            response = requests.request(method=req_method,url=self.url)
            print('Response code: ', response.status_code)
            if response.status_code == 200:
                print(response.text)
            
            print('*'*100)


if __name__ == '__main__':
    req = RequestMethodsTest()
    req.run()