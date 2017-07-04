import os
import json
from pprint import pprint


convert = True
check = False


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
                # print(result)
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

                        for element in grape1:
                            if element['annotations'] != [] and os.path.basename(element['filename']) == filename:
                                for annotation in element['annotations']:
                                    print('CHANGED', annotation, end='')
                                    try:
                                        annotation['x'], annotation['y'] = float(height) - annotation['y'] - annotation['width'], annotation['x']
                                    except:
                                        annotation['x'], annotation['y'] = annotation['y'], annotation['x']
                                    try:
                                        annotation['width'], annotation['height'] = annotation['height'], annotation['width']
                                    except: pass
                                    print(' WITH ', annotation)

                        for element in grape2_1:
                            if element['annotations'] != [] and os.path.basename(element['filename']) == filename:
                                for annotation in element['annotations']:
                                    print('CHANGED', annotation, end='')
                                    try:
                                        annotation['x'], annotation['y'] = float(height) - annotation['y'] - annotation['width'], annotation['x']
                                    except:
                                        annotation['x'], annotation['y'] = annotation['y'], annotation['x']
                                    try:
                                        annotation['width'], annotation['height'] = annotation['height'], annotation['width']
                                    except: pass
                                    print(' WITH ', annotation)

                        for element in grape2_2:
                            if element['annotations'] != [] and os.path.basename(element['filename']) == filename:
                                for annotation in element['annotations']:
                                    print('CHANGED', annotation, end='')
                                    try:
                                        annotation['x'], annotation['y'] = float(height) - annotation['y'] - annotation['width'], annotation['x']
                                    except:
                                        annotation['x'], annotation['y'] = annotation['y'], annotation['x']
                                    try:
                                        annotation['width'], annotation['height'] = annotation['height'], annotation['width']
                                    except: pass
                                    print(' WITH ', annotation)

                        height, width = width, height

                    # rescaling image to fit size
                    os.system('convert ' + p + '/' + filename +' -resize 720x1280! ' + p + '/' + filename + '_resized.jpg')
                    os.system('rm ' + p + "/" + filename)
                    os.system('mv ' + p + "/" + filename + "_resized.jpg " + p + '/' + filename)

                    # Scaling json to match
                    for element in grape1:
                        if element['annotations'] != [] and os.path.basename(element['filename']) == filename:
                            for annotation in element['annotations']:
                                annotation['x'] *= 720.0 / float(width)
                                annotation['y'] *= 1280.0 / float(height)
                                try:
                                    annotation['width'] *= 720.0 / float(width)
                                    annotation['height'] *= 1280.0 / float(height)
                                except: pass

                    for element in grape2_1:
                        if element['annotations'] != [] and os.path.basename(element['filename']) == filename:
                            for annotation in element['annotations']:
                                annotation['x'] *= 720.0 / float(width)
                                annotation['y'] *= 1280.0 / float(height)
                                try:
                                    annotation['width'] *= 720.0 / float(width)
                                    annotation['height'] *= 1280.0 / float(height)
                                except: pass

                    for element in grape2_2:
                        if element['annotations'] != [] and os.path.basename(element['filename']) == filename:
                            for annotation in element['annotations']:
                                annotation['x'] *= 720.0 / float(width)
                                annotation['y'] *= 1280.0 / float(height)
                                try:
                                    annotation['width'] *= 720.0 / float(width)
                                    annotation['height'] *= 1280.0 / float(height)
                                except: pass

                    print(filename, 'CONVERSION COMPLETED!')

        if check:
            for filename in f:
                result = os.popen('identify ' + p + "/" + filename).read()
                if result:
                    result = result.split()[2]
                    if result != "720x1280":
                        print(filename, 'has no right resolution!')
                else:
                    print(p + "/" + filename, "doesn't have json file associated!")
