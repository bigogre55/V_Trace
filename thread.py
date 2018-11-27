from threading import Thread
import geoIP

class TraceThread(Thread):

  def __init__(self, target):
    self.return_data = None
    self.TARGET = target
    super(TraceThread, self).__init__()
    
  def run(self):
    target = self.TARGET
    self.return_data = geoIP.main_trace(target)
    
if __name__ == '__main__':
  t = TraceThread(input("Target: "))
  t.start()
  t.join()
  print(t.return_data)