try:
    import requests
    import os
    from random import choice
    from concurrent.futures import ThreadPoolExecutor as Pool
    from concurrent.futures import wait
    from threading import Lock
    from sys import exit
    from colorama import init, Fore
except ImportError:
    import os
    os.system('pip3 install requests')
    os.system('pip3 install colorama')
    import requests
    from random import choice
    from concurrent.futures import ThreadPoolExecutor as Pool
    from concurrent.futures import wait
    from threading import Lock
    from sys import exit
    from colorama import init, Fore

class Scan:
    def __init__(self, help, root):
        init(autoreset = True)
        self.help = help
        self.root = root
        self.lock = Lock()
        self.code = {
            '200' : Fore.GREEN,
            '403' : Fore.RED,
            '429' : Fore.YELLOW,
            '500' : Fore.RED
            }

        with open(self.root + '/file/User-Agent.txt') as headers:
            self.headers = headers.read().split('\n')
            if '' in self.headers:
                self.headers.remove('')

    def test_proxy(self, proxies):
        try:
            requests.get('https://www.baidu.com', proxies = proxies, timeout = 5)
            return True
        except:
            return False

    def check_options(self, url, thread, file, timeout, proxy, status):
        #check url
        if url == None:
            print(Fore.RED + '[-]ERROR: URL can\'t be none.')
            print(Fore.YELLOW + self.help)
            exit()
        else:
            self.url = url.strip('/')
        
        #check thread
        
        if thread == None:
            self.thread = 600
        elif thread > 1000:
            print(Fore.RED + '[-]ERROR: Too many threads.')
            self.thread = 600
        elif thread <= 0:
            print(Fore.RED + '[-]ERROR: Threads is below 0.')
            self.thread = 600
        else:
            self.thread = thread

        #check dictionary file

        if file == None:
            self.file = self.root + '/file/dicc.txt'
        else:
            try:
                f = open(file)
                f.close()
                self.file = file
            except FileNotFoundError:
                print(Fore.RED + '[-]ERROR: Can\'t find the file.')
                print(Fore.YELLOW + '[?]Continue with local file?(y/n)')
                if input() == 'y':
                    self.file = self.root + '/file/dicc.txt'
                else:
                    exit()

        #check timeout

        if timeout == None:
            self.timeout = 2
        elif timeout <= 0:
            print(Fore.RED + '[-]ERROR:Timeout is below 0.')
            self.timeout = 2
        else:
            self.timeout = timeout

        #check proxy

        if proxy == None:
            self.proxies = [None]
        else:
            self.proxies = proxy.split(',')
            if '' in self.proxies:
                self.proxies.remove('')

            for p in self.proxies:
                proxies = {
                    'http' : 'http://' + p,
                    'https' : 'https://' + p
                    }
                if self.test_proxy(proxies) == False:
                    self.proxies.remove(p)

        if len(self.proxies) == 0:
            print(Fore.RED + '[-]ERROR: The proxies is not useful.')
            self.proxies = [None]

        #check status code

        if status == None:
            self.status = None
        else:
            self.status = status.split(',')

            for s in self.status:
                if s  not in self.code:
                    self.code[s] = 'green'


    def get(self, url):
        headers = {
            'User-Agent' : choice(self.headers)
            }
        
        try:
            if choice(self.proxies) != None:
                proxies = {
                    'http' : 'http://' + choice(self.proxies),
                    'https' : 'https://' + choice(self.proxies)
                    }
            else:
                proxies = None
            
            s = requests.get(url, timeout = self.timeout, proxies = proxies, headers = headers)
            self.lock.acquire()
            try:
                if self.status == None:
                    if s.status_code != 404:
                        if str(s.status_code) in self.code:
                            print(self.code[str(s.status_code)] + '[*]' + str(s.status_code) + ' ' + url)
                        else:
                            print(Fore.RED + '[*]' + str(s.status_code) + ' ' + url)
                else:
                    if str(s.status_code) in self.status:
                        print(self.code[str(s.status_code)] + '[*]' + str(s.status_code) + ' ' + url)
                self.lock.release()
                return 0
            except KeyboardInterrupt:
                self.lock.release()
                exit()
        except KeyboardInterrupt:
            self.lock.release()
            exit()
        except:
            return 1



    def scan(self):
        print(Fore.BLUE + '--<start>--')

        with open(self.file) as urls:
            e = Pool(max_workers = self.thread)
            t = [e.submit(self.get, (self.url + '/' + d.strip('\n'))) for d in urls]

            if wait(t, return_when = 'ALL_COMPLETED'):
                print(Fore.BLUE + '--<end>--')
                exit()



        

        
        
