from struct import *


class BmpFile:
  def __init__(self):
    self.width = 0
    self.height = 0
    self.data_length = 0
    self.data = 0

  def load(self, path):
    print('Loading ' + path + ' into object')
    
    image_file = open(path, "rb")
    header_data = image_file.read(14)
    #Read header
    header_array = unpack('=2sLHHL', header_data)
    
    header_field = header_array[0]
    header_size = header_array[1]
    header_offset = header_array[4]

    print(header_field)
    print(header_size)
    print(header_offset)
    
    if(header_field != b'BM'):
        print('ERROR: Not a windows bitmap. Try mspaint')
    
    header_data = image_file.read(24)
    print(header_data)
    dib_array = unpack('=LLL8xL', header_data)
    print(dib_array)
    dib_size = dib_array[0]
    self.width = dib_array[1]
    self.height = dib_array[2]
    self.data_length = dib_array[3]
    print(dib_size)
    
    image_file.read(16)
    
    self.data = image_file.read(self.data_length)

    self.printDebug()
    image_file.close()
    
  def getPixel(self, x, y):
    bmp_y = self.height - y - 1
    r = self.data[(bmp_y * self.width * 3) + (x * 3)]
    g = self.data[(bmp_y * self.width * 3) + (x * 3) + 1]
    b = self.data[(bmp_y * self.width * 3) + (x * 3) + 2]
    return (r, g, b)

  def printDebug(self):
    print('BmpFile Params')
    print(' width: ' + str(self.width))
    print(' height: ' + str(self.height))
    print(' data length: ' + str(self.data_length))
    print(' data: ' + str(self.data[1000:1200]))
    
    for y in range(0, self.height, 3):
      line = ''
      for x in range(0, self.width, 3):
        px = self.getPixel(x, y)
        num = px[0] * 9 / 256
        line = line + str(int(num))
      print(line)
      

