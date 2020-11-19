from bmpTools import BmpFile

import sys, getopt, os

def main(argv):
   inputfile = ''

   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('test.py -i <inputfile>')
      sys.exit(2)
   listHelpAndExit = True
   for opt, arg in opts:
      if opt in ("-i", "--ifile"):
         inputfile = arg
         listHelpAndExit = False
   if listHelpAndExit == True:
         print('test.py -i <inputfile>')
         print('  ex: `python bmp2c.py -i data\\test_image_mono.bmp`')
         sys.exit()
   print('Input file is "', inputfile)
   
   obj = BmpFile()
   obj.load(inputfile)
   
   file='output_' + os.path.split(inputfile)[1] + '.c.txt' 
   with open(file, 'w') as filetowrite:
     filetowrite.write('// Image width: ' + str(hex(obj.width)) + '\n')
     filetowrite.write('// Image height: ' + str(hex(obj.height)) + '\n')
     filetowrite.write('uint8_t test_image_mono[] = {\n')
     for c in range(0, 128 - 32):
        #identify the x of the lines
        xLine = (c * 4) % obj.width
        #print( "c = " + str(c) + ", " + str(xLine) )
        #print(str(obj.width))
        yLine = (int((c * 4) / obj.width) * 5)
        print("start " + str(xLine) + ", " + str (yLine))
        for l in range(5):
           #identify the y for this line
           line = '  '
           for x in range(4):
              px = obj.getPixel(xLine + x, yLine + l)
              print( "   " + str(xLine + x) +", " + str(yLine + l))
              value = px[0]
              line = line + "0x%02X" % value + ', '
           line = line + '\n'
           filetowrite.write(line)
     filetowrite.write('};\n')
     filetowrite.close()


if __name__ == "__main__":
   main(sys.argv[1:])


