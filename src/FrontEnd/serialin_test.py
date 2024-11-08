import serial

def main():
    ser = serial.Serial('COM14', 115200)
    ser.timeout = 5
    
    if ser.is_open:
        print('Serial was opened')

    while 1:
        if ser.in_waiting:
            distance = ser.readline().decode('utf-8').strip()
            if ser.in_waiting:
                print(distance)

if __name__ == "__main__":
    main()