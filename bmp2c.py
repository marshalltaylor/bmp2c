from struct import *

def read_rows(path):
    #print(pack('hhl', 1, 2, 3))
    #print(unpack('hhl', b'\x00\x01\x00\x02\x00\x00\x00\x03'))
    #print(calcsize('hhl'))
    
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
    dib_width = dib_array[1]
    dib_height = dib_array[2]
    dib_pixels = dib_array[3]
    print(dib_size)
    print("image (" + path + ") is " + str(dib_width) + "x" + str(dib_height) + ", " + str(dib_pixels) + " pixels")
    
    image_file.read(16)
    
    # Blindly skip the BMP header.
    #image_file.seek(54)

    # We need to read pixels in as rows to later swap the order
    # since BMP stores pixels starting at the bottom left.
    rows = []
    row = []
    pixel_index = 0

    while True:
        if pixel_index == dib_width:
            pixel_index = 0
            rows.insert(0, row)
            if len(row) != dib_width * 3:
                raise Exception("Row length is not dib_width*3 but " + str(len(row)) + " / 3.0 = " + str(len(row) / 3.0))
            row = []
        pixel_index += 1

        r_string = image_file.read(1)
        g_string = image_file.read(1)
        b_string = image_file.read(1)

        if len(r_string) == 0:
            # This is expected to happen when we've read everything.
            if len(rows) != dib_height:
                print("Warning!!! Read to the end of the file at the correct sub-pixel (red) but we've not read dib_height rows!")
            break

        if len(g_string) == 0:
            print("Warning!!! Got 0 length string for green. Breaking.")
            break

        if len(b_string) == 0:
            print("Warning!!! Got 0 length string for blue. Breaking.")
            break

        r = ord(r_string)
        g = ord(g_string)
        b = ord(b_string)

        row.append(b)
        row.append(g)
        row.append(r)

    image_file.close()



    print("Repacking pixels...")
    sub_pixels = []
    for row in rows:
        for sub_pixel in row:
            sub_pixels.append(sub_pixel)

    diff = len(sub_pixels) - dib_width * dib_height * 3
    #print "Packed", len(sub_pixels), "sub-pixels."
    if diff != 0:
        print("Error! Number of sub-pixels packed does not match dib_width*dib_height: (" + str(len(sub_pixels)) + " - dib_width * dib_height * 3 = " + str(diff) +").")

    return sub_pixels

# This list is raw sub-pixel values. A red image is for example (255, 0, 0, 255, 0, 0, ...).
sub_pixels = read_rows("test_image_mono.bmp")

print("Done.")
print(sub_pixels)