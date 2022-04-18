import threading

x = 0

def increment():
    global x
    for i in range(500000):
        x += 1

def main():
   global x
   x = 0
   
   t1 = threading.Thread(target=increment)
   t2 = threading.Thread(target=increment)

   t1.start()
   t2.start()

   t1.join()
   t2.join()
   print(x)

main()