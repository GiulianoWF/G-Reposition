import os
import platform
import numpy

class Modifier:
    def __init__(self, x_translation, y_translation, z_translation, z_rotation):
        #Create rotation matrix.
        theta = numpy.radians(z_rotation)
        c, s = numpy.cos(theta), numpy.sin(theta)
        self.R = numpy.array(((c,-s), (s, c)))
        
        #Store translations.
        self.x_translation = x_translation
        self.y_translation = y_translation
        self.z_translation = z_translation

        #The initial state takes reference to the point (0, 0, 0).
        #This state is allways updated in relation to the last point passed to the object.
        self.point_reference_xy = numpy.array([0.0, 0.0])
        self.z_reference = 0.0

        #The new state is stored here while calculated.
        self.new_point_xy = numpy.array([0.0, 0.0])
        self.new_z = 0.0

    def translate_line(self, line):
        #If the line is a movement line.
        if (('X' in line) or ('Y' in line) or ('Z' in line)) and ('G1' in line):
            #The new point is the reference point, whit the changes needed.
            #First, copy the old point.
            self.new_point_xy = self.point_reference_xy
            self.new_z = self.z_reference

            #Then make the changes.
            for word in line.split():
                if word[0] is 'X':
                    self.new_point_xy[0] = float(word[1:])
                elif word[0] is 'Y':
                    self.new_point_xy[1] = float(word[1:])
                elif word[0] is 'Z':
                    self.new_z = float(word[1:])
            
            #Rotate by the Z axis.
            self.new_point_xy = self.R.dot(self.new_point_xy)

            #Translate.
            self.new_point_xy[0] = self.new_point_xy[0] + self.x_translation
            self.new_point_xy[1] = self.new_point_xy[1] + self.y_translation
            self.new_z           = self.new_z           + self.z_translation
            
            #The new point is calculated, then the line must be translated and returned.
            processed_line = ''
            for word in line.split():
                #Change the words containing the coordinates.
                if 'X' in word:
                    processed_line = processed_line + ' ' + 'X{:.3f}'.format(self.new_point_xy[0])
                elif 'Y' in word:
                    processed_line = processed_line + ' ' + 'Y{:.3f}'.format(self.new_point_xy[1])
                elif 'Z' in word:
                    processed_line = processed_line + ' ' + 'Z{:.3f}'.format(self.new_z)
                else :
                    #Or copy the other words.
                    processed_line = processed_line + ' ' + word

            #Return the line processed.
            return processed_line

        #If the line is not a moviment line.
        else:
            return line

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    my_os = platform.system()
    if my_os is 'Linux':
        path_in  = path + '/' + input('Input file name?')
        path_out = path + '/' + input('Output file name?')
    if my_os is 'Windows':
        path_in  = path + '\\' + input('Input file name?')
        path_out = path + '\\' + input('Output file name?')
    file_in = open(path_in, 'r+')
    file_out = open(path_out, 'w+')

    #get the parameters
    rotation        = float(input("Enter angle to rotate "))
    x_translation   = float(input("Enter X translation "))
    y_translation   = float(input("Enter Y translation "))
    z_translation   = float(input("Enter Z translation "))

    #create object
    transformer = Modifier(x_translation, y_translation, z_translation, rotation)

    i = 0
    for line in file_in:
        i = i+1
        print ('Line number ' + str(i))
        file_out.write(transformer.translate_line(line) + '\n')

    #close the files before ploting, so it is saved when ploting. (witch takes time)
    file_in.close()
    file_out.close()

    print(input('End of conversion.'))

if __name__ == "__main__":
    main()
