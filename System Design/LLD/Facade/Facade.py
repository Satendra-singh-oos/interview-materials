#Faced Desing Pattern 
# Provide a simplified and easy to understant interface to a complex system.
# Facade lets you view or interact with the main features of a complex system.
# Facade is a structural design pattern that provides a simplified interface to the complex logic of one or more services (subsystems).

# Blanicing cm[lexityb and presetauin .usablity

#typical home many subsytem (eletrical sanutuion),comple inter startur(efg.floor kayer),end user is not expised to internal same wuth software many system working to provide flexibility but.. api consumers want it to just work

class Buffer:
  def __init__(self, width=30, height=20):
    self.width = width
    self.height = height
    self.buffer = [' '] * (width*height)

  def __getitem__(self, item):
    return self.buffer.__getitem__(item)

  def write(self, text):
    self.buffer += text

class Viewport:
  def __init__(self, buffer=Buffer()):
    self.buffer = buffer
    self.offset = 0

  def get_char_at(self, index):
    return self.buffer[self.offset+index]

  def append(self, text):
    self.buffer += text

class Console:
  def __init__(self):
    b = Buffer()
    self.current_viewport = Viewport(b)
    self.buffers = [b]
    self.viewports = [self.current_viewport]

  # high-level
  def write(self, text):
    self.current_viewport.buffer.write(text)

  # low-level
  def get_char_at(self, index):
    return self.current_viewport.get_char_at(index)


if __name__ == '__main__':
  c = Console()
  c.write('hello')
  ch = c.get_char_at(0)