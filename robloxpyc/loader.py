# LOADING
import sys
if not (os.path.dirname(os.path.abspath(__file__)).startswith(sys.path[-1])):
    import colortext
else:
    from . import colortext
    
from time import sleep
from tqdm import tqdm

class loader:
  self = {}
  def __init__(self, max):
    print("\n\n")
    self.max = max
    self.current = 0
    self.tqdm = tqdm(total=max)
    
  def yielduntil(self):
    global count
    while self.max != self.current:
      sleep(.5)
    self.tqdm.update(self.max-self.current )
    self.tqdm.close()
  def update(self, amount):
    self.tqdm.update(amount)
  def error(self):
    self.tqdm.write(colortext.red("paused!", ["bold"]))
    self.current = self.max
    self.tqdm.close()
  