import sys
import serial
from time import sleep

peak_pressure = 0
num_samples = 5
num_lists = 3
data_list = list()

class leak_check:

    
    def __init__(self, num_samples, num_lists):
        self.num_samples = num_samples
        self.num_lists = num_lists
        self.data_list = list()
        self.leak = False
        
    def check_leak(self, cur_reading):
        self.leak = False
        sensitivity = -0.04
        # warning will be emailed if it drops a certain amount from averages
        if len(self.data_list) < self.num_samples*self.num_lists:
            self.data_list.append(cur_reading)
            leak = False
        else:
            self.data_list.append(cur_reading)
            del self.data_list[0]
            temp_lists = [list(t) for t in zip(*[iter(self.data_list)]*(self.num_samples))]
            average_list = list()
            for pressure_section in temp_lists:
                average_list.append(sum(pressure_section)/self.num_samples)
            prev_pressure = average_list[0]
            print(average_list)
            for pressure in average_list[1:]:
                if pressure-prev_pressure > sensitivity:
                    self.leak = False
                    break
                prev_pressure = pressure
                self.leak = True
        print(self.leak)    
        return self.leak
        
    def test_list(self, input_list):
        for item in input_list:
            print(item)
            self.leak = self.check_leak(item)
            if self.leak == True:
                return self.leak
        return self.leak


def main():
    if len(sys.argv) > 1:
        port = sys.argv[1]
        
        file_index = 0
        filename = 'file{}.txt'.format(file_index)
        try:
            f = open(filename, "w")
        except:
            print("Could not open file:", filename)
            return
# open file
        try:
            ser = serial.Serial(port, 115200)
            sleep(3)
            ser.reset_input_buffer()
        except Exception as err:
            print("Could not connect: {!r}".format(err))
            return
        print("Data connection at:", port)
        line_count = 0
        while True:
            try:
                line = ser.readline().decode().rstrip("\r\n")
                if line != '': # Still alive?
                    print(line)
                    line_count += 1
                    print('writing')
                    f.write(line + "\r\n")
                    if line_count >= 5:
                        line_count = 0
                        f.close()
                        file_index+= 1
                        
                        filename = 'file{}.txt'.format(file_index)
                        if file_index == 8:
                            break
                        f = open(filename, "w")
                        
                else: # EOF
                    print('is none')
                    break
            except Exception as err:
                print("{!r}".format(err))
                break
            except KeyboardInterrupt:
                print("Interrupted!")
                break
        if f is not None:
            f.close()
    else:
        print("Usage: usbrecv port [filename]")

if __name__ == "__main__":
    main()
