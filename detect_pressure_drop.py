 
class leak_check:

    
    def __init__(self, num_samples=5, num_lists=3):
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
