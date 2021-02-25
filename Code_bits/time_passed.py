import time

oldtime = time.time()
# check
while True:
    if time.time() - oldtime > 10:
        print ("it's been 10 seconds")
        break