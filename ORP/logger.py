import time
import csv

last_reading= 0

def compare_and_record(reading):
    global last_reading
    if reading != last_reading:
       record(reading)
       last_reading=reading
       return
    else:
        print "Nothing written"

def record(reading):
    with open('log2.csv', 'a') as f:
        log = csv.writer(f)
        log.writerow([time.strftime("%c"), reading])
    f.close

if __name__ == "__main__":
    print "\nINput reading\n"
    while True:
        reading = input("Input")
        print("Last reading is " + str(last_reading))
        compare_and_record(reading)
        print("Reading is " + str(reading))
        
