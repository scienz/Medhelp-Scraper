import frontier
import post_scraper
import threading
import queue

if __name__ == "__main__":
    lst = frontier.build()
    taskQueue = queue.Queue()
    threads = list()
    for dct in lst:
        for key in dct:
            taskQueue.put((key, dct[key]))
            #post_scraper.run(key, dct[key])
    
    for i in range(4):
        threads.append(threading.Thread(target = post_scraper.run, args = taskQueue.get(), daemon = True))
        threads[i].start()
    
    while taskQueue:
        for t in threads:
            if not t.isAlive():
                threads.pop(threads.index(t))
                nextTask = threading.Thread(target = post_scraper.run, args = taskQueue.get(), daemon = True)
                threads.append(nextTask)
                nextTask.start()

            