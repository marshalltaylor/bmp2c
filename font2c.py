from bmpTools import BmpFile

import sys, getopt, os

#TODO: add ascii range input options
#TODO: generate metadata to describe output font
#TODO: generate usable file pairs into folder for all font2c.py, bmp2c.py, etc

def main(argv):
   inputfile = ''

   try:
      opts, args = getopt.getopt(argv,"i:x:y:",["ifile="])
   except getopt.GetoptError:
      print('test.py -i <inputfile> -x <char width> -y <char height>')
      sys.exit(2)
   listHelpAndExit = True
   for opt, arg in opts:
      if opt in ("-i", "--ifile"):
         inputfile = arg
         listHelpAndExit = False
      if opt in ("-x"):
         charWidth = int(arg)
         listHelpAndExit = False
      if opt in ("-y"):
         charHeight = int(arg)
         listHelpAndExit = False
   if listHelpAndExit == True:
         print('test.py -i <inputfile>')
         print('  ex: `python font2c.py -i data\8x11_font.bmp -x 8 -y 11`')
         sys.exit()
   print('Input file is ', inputfile, charWidth, charHeight)
   obj = BmpFile()
   obj.load(inputfile)
   
   file='output_' + os.path.split(inputfile)[1] + '.c.txt' 
   ASCII_BLACK_LEVEL = 98
   with open(file, 'w') as filetowrite:
     filetowrite.write('// Image width: ' + str(hex(obj.width)) + '\n')
     filetowrite.write('// Image height: ' + str(hex(obj.height)) + '\n')
     filetowrite.write('uint8_t test_image_mono[] = {\n')
     for c in range(0, 128 - 32):
        #identify the x of the lines
        xLine = (c * charWidth) % obj.width
        #print( "c = " + str(c) + ", " + str(xLine) )
        #print(str(obj.width))
        yLine = (int((c * charWidth) / obj.width) * charHeight)
        print("start " + str(xLine) + ", " + str (yLine))
        for l in range(charHeight):
           #identify the y for this line
           line = '  '
           for x in range(charWidth):
              px = obj.getPixel(xLine + x, yLine + l)
              print( "   " + str(xLine + x) +", " + str(yLine + l))
              #Scale to video ready range
              value = int(((px[0] * (255 - ASCII_BLACK_LEVEL))/256) + ASCII_BLACK_LEVEL)
              line = line + "0x%02X" % value + ', '
           line = line + '\n'
           filetowrite.write(line)
     filetowrite.write('};\n')
     filetowrite.close()


if __name__ == "__main__":
   main(sys.argv[1:])


