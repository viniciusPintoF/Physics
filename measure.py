import math
import numpy

def significant_power(number):
    if number == 0: return 0
    return math.floor(math.log10(number))

def significant_digit(number):
    if number == 0: return 0
    main_digit = 0     
    for digit in str(number):
        if digit == '.': continue
        if digit != '0':
            main_digit = float(digit)
            break    
    return main_digit

def majorate(number):
    digit = significant_digit(number)
    power = significant_power(number)
    value = digit*(10**power) + 1*(10**power)
    return round(value, -power)
    
    
class Measure:
    def __init__(self, value=0.0, deviation=0.0):
        self.m = float(value)
        self.d = float(deviation)
        
    def majorated_deviation(self):
        return majorate(self.d)
    
    def aproximated_value(self):
        majorated = majorate(self.d)
        return round(self.m, -significant_power(majorated))
    
    def formatted_strings(self):
        value = self.aproximated_value()
        deviation = self.majorated_deviation()
        if significant_power(deviation) < 0:
            return (str(value), str(deviation))
        else:
            return ('{:.0f}'.format(value), '{:.0f}'.format(deviation))
        
    def __str__(self):        
        return str(self.m) + '(' + str(self.d) + ')'        
        
    def __pos__(self):
        return Measure(self.m, self.d)
        
    def __neg__(self):
        return Measure(-self.m, self.d)
    
    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Measure(self.m + other.m, self.d + other.d)
        else:
            return Measure(self.m + other, self.d)
    
    __radd__=__add__
        
    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Measure(self.m - other.m, self.d + other.d)
        else:
            return Measure(self.m - other, self.d)
    
    def __rsub__(self, other): return -(self - other)        
    
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            deviation = abs(other.m)*self.d + abs(self.m)*other.d
            return Measure(self.m * other.m, deviation)   
        else:
            deviation = abs(other)*self.d
            return Measure(self.m * other, deviation)        
    
    __rmul__=__mul__
    
    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            deviation = abs(1/other.m)*self.d + abs(-self.m/(other.m**2))*other.d
            return Measure(self.m / other.m, deviation)
        else:
            deviation = abs(1/other)*self.d
            return Measure(self.m / other, deviation)
    
    def __rtruediv__(self, other):
        if isinstance(other, self.__class__):
            deviation = abs(-other.m/(self.m**2))*self.d + abs(1/self.m)*other.d
            return Measure(other.m/self.m, deviation)
        else:
            deviation = abs(-other/(self.m**2))*self.d
            return Measure(other/self.m, deviation)
        
    def __pow__(self, other):
        if isinstance(other, self.__class__):
            deviation = abs(other.m*(self.m**(other.m-1)))*self.d + abs((self.m**other.m)*math.log(self.m))*other.d
            return Measure(self.m**other.m, deviation)
        else:
            deviation = abs(other*(self.m**(other-1)))*self.d            
            return Measure(self.m**other, deviation)
    
    def __rpow__(self, other):
        if isinstance(other, self.__class__):
            deviation = abs((other.m**self.m)*math.log(other.m))*self.d + abs(self.m*(other.m**(self.m-1)))*other.d
            return Measure(other.m**self.m, deviation)
        else:
            deviation = abs((other**self.m)*math.log(other))*self.d
            return Measure(other**self.m, deviation)
    
    def log(self, base=math.e):
        deviation = abs(1/(self.m*math.log(base))) * self.d
        return Measure(math.log(self.m), deviation)
    
    def sin(self):
        return Measure(math.sin(self.m), abs(math.cos(self.m))*self.d)
    
    def cos(self):
        return Measure(math.cos(self.m), abs(-math.sin(self.m))*self.d)

class MeasureList:
    def __init__(self, list):
        self.list = list
        self.m = [msr.m for msr in self.list]
        self.d = [msr.d for msr in self.list]
        self.length = len(self.list)
    
    def __getitem__(self, index):
        return self.list[int(index)]
        
    def majorated_deviation(self):
        return [majorate(measure.d) for measure in self.list]
    
    def aproximated_value(self):
        return [round(msr.m, -significant_power(majorate(msr.d))) for msr in self.list]
    
    def formatted_strings(self):
        values = self.aproximated_value()
        deviations = self.majorated_deviation()
        
        value_str = [str(v) for v in values]
        value_fmt = ['{:.0f}'.format(v) for v in values]
        dev_str = [str(d) for d in deviations]
        dev_fmt = ['{:.0f}'.format(d) for d in deviations]   
        
        return (
            [str(value_str[i]) if significant_power(deviations[i]) < 0 else value_fmt[i] for i in range(self.length)],
            [str(dev_str[i]) if significant_power(deviations[i]) < 0 else dev_fmt[i] for i in range(self.length)]
        )
          
    def __len__(self):
        return self.length
    
    def __str__(self):
        result = '['
        for i in range(self.length):
            result += str(self.list[i])
            if i != self.length-1: result += ', '
        result += ']'
        return result
   
    def __neg__(self):
        return MeasureList([ -self.list[i] for i in range(self.length) ])
   
    def __add__(self, other):
        if isinstance(other, self.__class__):
            return MeasureList([ self.list[i] + other.list[i] for i in range(self.length) ])
        elif isinstance(other, list):
            return MeasureList([ self.list[i] + other[i] for i in range(self.length) ])
        else:
            return MeasureList([ self.list[i] + other for i in range(self.length) ])
    __radd__=__add__
    
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return MeasureList([ self.list[i] * other.list[i] for i in range(self.length) ])
        elif isinstance(other, list):
            return MeasureList([ self.list[i] * other[i] for i in range(self.length) ])
        else:
            return MeasureList([ self.list[i] * other for i in range(self.length) ])
    __rmul__=__mul__
    
    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return MeasureList([ self.list[i] - other.list[i] for i in range(self.length) ])
        elif isinstance(other, list):
            return MeasureList([ self.list[i] - other[i] for i in range(self.length) ])
        else:
            return MeasureList([ self.list[i] - other for i in range(self.length) ])    
    def __rsub__(self, other): return -(self - other)
    
    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return MeasureList([ self.list[i] / other.list[i] for i in range(self.length) ])
        elif isinstance(other, list):
            return MeasureList([ self.list[i] / other[i] for i in range(self.length) ])
        else:
            return MeasureList([ self.list[i] / other for i in range(self.length) ])
    def __rtruediv__(self, other):
        if isinstance(other, self.__class__):
            return MeasureList([ other.list[i] / self.list[i] for i in range(self.length) ])
        elif isinstance(other, list):
            return MeasureList([ other[i] / self.list[i] for i in range(self.length) ])
        else:
            return MeasureList([other / self.list[i] for i in range(self.length) ])
        
    def __pow__(self, other):
        if isinstance(other, self.__class__):
            return MeasureList([ self.list[i] ** other.list[i] for i in range(self.length) ])
        elif isinstance(other, list):
            return MeasureList([ self.list[i] ** other[i] for i in range(self.length) ])
        else:
            return MeasureList([ self.list[i] ** other for i in range(self.length) ])
    def __rpow__(self, other):
        if isinstance(other, self.__class__):
            return MeasureList([ other.list[i] ** self.list[i] for i in range(self.length) ])
        elif isinstance(other, list):
            return MeasureList([ other[i] ** self.list[i] for i in range(self.length) ])
        else:
            return MeasureList([other ** self.list[i] for i in range(self.length) ])
        
    def log(self, base=math.e):
        return MeasureList([ self.list[i].log(base) for i in range(self.length) ])
    
    def sin(self):
        return MeasureList([ self.list[i].sin() for i in range(self.length) ])
    
    def cos(self):
        return MeasureList([ self.list[i].cos() for i in range(self.length) ])
    

def numeric_derivative(top, bottom, offset):
    length = len(top)
    derivatives = numpy.empty(length, dtype=Measure)        
    for i in range(length):   
        next = i+offset if i+offset < length else i
        prev = i-offset if i-offset >= 0 else i
        deltaTop = top[next] - top[prev]
        deltaBot = bottom[next] - bottom[prev]
        derivatives[i] = deltaTop/deltaBot
 
    return MeasureList(derivatives)