import os
import json
from pprint import pprint

convert = True
check = True

with open('./Sofia/grapes1.json') as grape_file:
    print(type(grape_file))
    grape1 = json.load(grape_file)

with open('./Sabrina/grapes2_1.json') as grape_file:
    grape2_1 = json.load(grape_file)

with open('./Martina/grapes2_2.json') as grape_file:
    grape2_2 = json.load(grape_file)


if convert:
    for p, d, f in os.walk(os.getcwd()):
        for filename in f:
            result = os.popen('identify ' + p + "/" + filename).read()
            if result:
                print(result)
                result = result.split()[2]
                if result != "720x1280": # if the resolution is not the right one
                    width, height = result.split('x')[0], result.split('x')[1]
                    # print(filename, '\t\twidth', width, 'height', height)

                    if int(height) < int(width): # if it's not rotated right
                        os.system('convert -rotate "90" ' + p + "/" + filename + " " + p + "/" + filename + "_rotated.jpg")
                        # print('image', p + "/" + filename, "rotated successfully!")
                        os.system('rm ' + p + "/" + filename)
                        # print('removed', p + "/" + filename)
                        os.system('mv ' + p + "/" + filename + "_rotated.jpg " + p + '/' + filename)
                        # print('removed clones\n\n')

                        # TODO ROTATE JSON TO MATCH
                        """
                        for imagedata in grape1:
                            filename = os.path.basename(imagedata['filename'])
                            annotations = imagedata['annotations']
                        """


                    # rescaling image to fit size
                    os.system('convert ' + p + '/' + filename +' -resize 720x1280! ' + p + '/' + filename + '_resized.jpg')
                    os.system('rm ' + p + "/" + filename)
                    os.system('mv ' + p + "/" + filename + "_resized.jpg " + p + '/' + filename)

                    # TODO SCALE JSON TO MATCH

        if check:
            for filename in f:
                result = os.popen('identify ' + p + "/" + filename).read()
                if result:
                    result = result.split()[2]
                    if result != "720x1280":
                        print(filename, 'has no right resolution!')
                else:
                    print(p + "/" + filename, "doesn't have json file associated!")
