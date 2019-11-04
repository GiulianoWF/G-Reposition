import serial
import numpy as np

path_in = '/home/labcim/Downloads/Bistable_Mechanism/files/file.gcode'
path_out = '/home/labcim/Downloads/Bistable_Mechanism/files/file_transfomed.gcode'
file_in = open(path_in, 'r+')
file_out = open(path_out, 'w+')

rotation = float(input("Enter angle to rotate "))
y_translation = float(input("Enter Y translation "))
x_translation = float(input("Enter X translation "))

theta = np.radians(30)
c, s = np.cos(theta), np.sin(theta)
R = np.array(((c,-s), (s, c)))
x = float(0)
y = float(0)

for line in file_in:
    if ('X' in line) or ('Y' in line):
        print(line + "   ---> get transformed into :")
        for word in line.split():
            if word[0] is 'X':
                x = float(word[1:])
                x = x + x_translation
                # print(float(word[1:]))
            elif word[0] is 'Y':
                # print(float(word[1:]))
                y = float(word[1:])
                y = y + y_translation
        point = np.array([x,y])
        point = R.dot(point)
        new_string = ''
        for word in line.split():
            if 'X' in word:
                word2 = 'X{:.3f}'.format(point[0])
                new_string = new_string + ' ' +  word2
            elif 'Y' in word:
                word2 = 'Y{:.3f}'.format(point[1])
                new_string = new_string + ' ' + word2
            else:
                new_string = new_string + ' ' + word
        print( new_string )
        file_out.write( new_string + '\n')
    else:
        file_out.write( line )

file_in.close()
file_out.close()