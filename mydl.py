from queue import Queue
from time import sleep
from threading import Thread
from youtube_dl import YoutubeDL
import pickle
import os

class dl:
    class __logger(object):
        def debug(self, msg): pass
        def warning(self, msg): pass
        def error(self, msg): print(msg)

    def __hook(self, d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')
        
    def __init__(self, pf="default"):
        self.q = Queue()
        self.pf = pf+'.pickle'
        self.process_t = Thread(target=self.__process)

    def add(self, data):
        self.q.put(data)
        print('Adding',data)
        print('New Queue Size',self.q.qsize())
        self.__save()
        if not self.process_t.is_alive(): self.process_t.start()          
    
    def __process(self):
        print('Started Processing Queue',self.q.qsize())
        while not self.q.empty():
            self.current_download = self.q.get()
            self.__save()
            self.__download()
            self.q.task_done()
            print('New Queue Size',self.q.qsize())
        try:
            os.remove(self.pf)
        except OSError as e:
            print(e)
        print('Done Processing Queue')

    def __save(self):
        with open(self.pf,'wb') as file:
            pickle.dump(self.q.queue,file)
    
    def resume(self):
        if os.path.exists(self.pf) and os.path.getsize(self.pf):
            with open(self.pf,'rb') as file:
                q = Queue()
                q.queue = pickle.load(file)
                while not q.empty():
                    self.q.put(q.get())
            if self.q.qsize() > 0: self.start()
        
    def __download(self):
        data = self.current_download
        # ydl_opts = {
        #     'outtmpl': data['filename'],
        #     'logger': self.__logger(),
        #     'progress_hooks': [self.__hook]
        # }

        # with YoutubeDL(ydl_opts) as ydl:
        #     ydl.download([data['url']])
        #             print('Downloading...', data)
        sleep(5)
        print('Downloaded ',data)