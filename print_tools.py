import time
import sys
import os

class ProgressBar:
    def __init__(self, width=50):
        self.percent = 0
        self.start = time.time()
        self.setWidth(width)
        
    def setWidth(self, width: int):
        if not isinstance(width, int) or os.get_terminal_size().columns < width + 25:
            self.width = os.get_terminal_size().columns-25
            return
        self.width = width
        
    def setPercent(self, i: int):
        if not isinstance(i, (int, float)):
            return
        i = max(0, min(100, i))
        self.percent = int(i)

    def getLinearTime(self):
        if self.percent == 0:
            return "N/A"
        
        now = time.time()
        diff = now-self.start
        v = diff/self.percent
        remain = v*(100-self.percent)
        remain = time.gmtime(remain)
        if remain.tm_hour > 0:
            return f"{remain.tm_hour}h {remain.tm_min}min {remain.tm_sec}s"
        elif remain.tm_min > 0:
            return f"{remain.tm_min}min {remain.tm_sec}s"
        else:
            return f"{remain.tm_sec}s"
        
    def display(self):
        remain = self.getLinearTime()
        hashtags = int(self.percent/(100/self.width))
        print(f"[{'#'*hashtags}{'-'*(self.width-hashtags)}] - {self.percent}% ({remain})", end="\r")
        sys.stdout.flush()
        if (self.percent == 100):
            print("\n")

    def fromTime(self, sec):
        self.setPercent(0)
        t = sec/100
        for i in range(0, 101):
            self.setPercent(i)
            self.display()
            time.sleep(t)
