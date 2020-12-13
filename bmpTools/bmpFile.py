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

    print('Main Header Data')
    print(' field: ' + str(header_field))
    print(' size: ' + str(header_size))
    print(' offset: ' + str(header_offset))
    
    if(header_field != b'BM'):
        print('ERROR: Not a windows bitmap. Try mspaint')
    
    header_data = image_file.read(24)
    #print('Sub Header Data')
    print('DATA: ' + str(header_data))
    dib_array = unpack('=LLLHHxxxxL', header_data)
    #print(dib_array)
    dib_size = dib_array[0]
    self.width = dib_array[1]
    self.height = dib_array[2]
    self.bytesPerPixel = int(dib_array[4] / 8)
    self.data_length = dib_array[5]
    #print(dib_size)
    image_file.seek(header_offset)
    bytesPerRow = self.width * self.bytesPerPixel
    print(" per row", bytesPerRow)
    bytePaddingRequired = 0
    if((bytesPerRow % 4) != 0):
      bytePaddingRequired = 4 - (bytesPerRow % 4)
    print(" pad per row", bytePaddingRequired)
    self.data = b""
    for y in range(0, self.height):
      self.data = self.data + image_file.read(bytesPerRow)
      image_file.read(bytePaddingRequired)

    self.printDebug()
    image_file.close()
    
  def getPixel(self, x, y):
    bmp_y = self.height - y - 1
    #print('get ', x, y)
    #print('get ', (bmp_y * self.width * self.bytesPerPixel) + (x * self.bytesPerPixel))
    if self.bytesPerPixel == 1:
      r = self.data[(bmp_y * self.width * self.bytesPerPixel) + (x * self.bytesPerPixel)]
      g = r
      b = r
    if self.bytesPerPixel == 3:
      r = self.data[(bmp_y * self.width * self.bytesPerPixel) + (x * self.bytesPerPixel)]
      g = self.data[(bmp_y * self.width * self.bytesPerPixel) + (x * self.bytesPerPixel) + 1]
      b = self.data[(bmp_y * self.width * self.bytesPerPixel) + (x * self.bytesPerPixel) + 2]
    #print(str(int(x)) + ", " + str(int(y)) + ", " + hex(r))
    return (r, g, b)

  def printDebug(self):
    print('BmpFile Params')
    print(' width: ' + str(self.width))
    print(' height: ' + str(self.height))
    print(' bytes per pixel: ' + str(self.bytesPerPixel))
    print(' data length: ' + str(self.data_length))
    print(' measured length: ' + str(len(self.data)))
    #For debugging exact data:
    #print(' data: ' + str(self.data[0:1000]))
    
    print()
    print(' Ascii thumb:')
    print()
    for y in range(0, self.height, 3):
      line = ''
      for x in range(0, self.width, 3):
        px = self.getPixel(x, y)
        num = px[0] * 9 / 256
        line = line + str(int(num))
      print(line)
      

