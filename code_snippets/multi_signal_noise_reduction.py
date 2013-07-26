from __future__ import division
from PIL import Image as PILImage
from Tkinter import *
from tkFileDialog import askopenfilename as openfile
from itertools import product
from random import shuffle

class Image():
    def __init__(self,filename=None,dimensions=None):
        if filename!=None:
            self.pic = PILImage.open(filename)
            self.imgData = self.pic.load()
            self.size = self.pic.size
        else:
            if dimensions!=None:
                self.size = dimensions
            else:
                self.size = [0,0]
            self.pic = None
            self.imgData = {}
            for x,y in product(range(self.size[0]),range(self.size[1])):
                self.setpixel(x,y,0,0,0)
    def setpixel(self,x,y,r,g,b):
        self.imgData[x,y] = tuple(map(max,zip((r,g,b),(0,0,0))))
    def getpixellist(self):
        return product(range(self.size[0]),range(self.size[1]))
    def show(self):
        tempImage = PILImage.new('RGB',self.size)
        for x,y in self.getpixellist():
            tempImage.putpixel((x,y),self.imgData[x,y])
        tempImage.show()

def get_delta(image1,image2):
    if image1.size != image2.size: raise ValueError("Image sizes do not match")
    delta = 0
    for x,y in image1.getpixellist():
        delta += sum(abs_pixel_diff(image1,image2,x,y))
    return delta / (image1.size[0] * image1.size[1])

mode = (lambda l: max([(l.count(i), i) for i in set(l)])[1] if len(set(l)) < len(l) else sum(l)/float(len(l)))

pixel_operation = lambda f: lambda image1,image2,x,y: map(f,zip(image1.imgData[x,y],image2.imgData[x,y]))
abs_pixel_diff = pixel_operation(lambda (x,y): abs(x-y))
pixel_diff = pixel_operation(lambda (x,y): x-y)
pixel_avg = pixel_operation(lambda (x,y): (x+y)/2)
pixel_sum = pixel_operation(lambda (x,y): x+y)

def image_operation(operation,image1,image2):
    if image1.size != image2.size: raise ValueError("Image sizes do not match")
    result = Image(dimensions=image1.size)
    for x,y in result.getpixellist():
        r,g,b = operation(image1,image2,x,y)
        result.setpixel(x,y,r,g,b)
    return result

get_delta_image = lambda image1,image2: image_operation(abs_pixel_diff,image1,image2)
subtract_image = lambda minuend,subtrahend: image_operation(pixel_diff,minuend,subtrahend)
average_image = lambda image1,image2: image_operation(pixel_avg,image1,image2)
add_image = lambda image1,image2: image_operation(pixel_sum,image1,image2)

def average_images_add(image_list): 
    shuffle(image_list)
    set1 = image_list[0::2]
    image1 = Image(dimensions=set1[0].size)
    for x,y in image1.getpixellist():
        r,g,b = reduce(lambda a,b: (a[0]+b[0],a[1]+b[1],a[2]+b[2]),[image.imgData[x,y] for image in set1])
        image1.setpixel(x,y,r/len(set1),g/len(set1),b/len(set1))
    set2 = image_list[1::2]
    image2 = Image(dimensions=set2[0].size)
    for x,y in image2.getpixellist():
        r,g,b = reduce(lambda a,b: (a[0]+b[0],a[1]+b[1],a[2]+b[2]),[image.imgData[x,y] for image in set2])
        image2.setpixel(x,y,r/len(set2),g/len(set2),b/len(set2))
    return add_image(average_image(image1,image2),subtract_image(image1,image2))

def average_images_sub(image_list):
    shuffle(image_list)
    set1 = image_list[0::2]
    image1 = Image(dimensions=set1[0].size)
    for x,y in image1.getpixellist():
        r,g,b = reduce(lambda a,b: (a[0]+b[0],a[1]+b[1],a[2]+b[2]),[image.imgData[x,y] for image in set1])
        image1.setpixel(x,y,r/len(set1),g/len(set1),b/len(set1))
    set2 = image_list[1::2]
    image2 = Image(dimensions=set2[0].size)
    for x,y in image2.getpixellist():
        r,g,b = reduce(lambda a,b: (a[0]+b[0],a[1]+b[1],a[2]+b[2]),[image.imgData[x,y] for image in set2])
        image2.setpixel(x,y,r/len(set2),g/len(set2),b/len(set2))
    return subtract_image(average_image(image1,image2),subtract_image(image1,image2))

def average_images(image_list): 
    shuffle(image_list)
    set1 = image_list[0::2]
    image1 = Image(dimensions=set1[0].size)
    for x,y in image1.getpixellist():
        r,g,b = reduce(lambda a,b: (a[0]+b[0],a[1]+b[1],a[2]+b[2]),[image.imgData[x,y] for image in set1])
        image1.setpixel(x,y,r/len(set1),g/len(set1),b/len(set1))
    set2 = image_list[1::2]
    image2 = Image(dimensions=set2[0].size)
    for x,y in image2.getpixellist():
        r,g,b = reduce(lambda a,b: (a[0]+b[0],a[1]+b[1],a[2]+b[2]),[image.imgData[x,y] for image in set2])
        image2.setpixel(x,y,r/len(set2),g/len(set2),b/len(set2))
    return subtract_image(average_image(image1,image2),get_delta_image(image1,image2))

def average_noisefilter_all_sub(image_list):
    shuffle(image_list)
    set1 = image_list[0::2]
    image1 = Image(dimensions=set1[0].size)
    for x,y in image1.getpixellist():
        r,g,b = reduce(lambda a,b: (a[0]+b[0],a[1]+b[1],a[2]+b[2]),[image.imgData[x,y] for image in set1])
        image1.setpixel(x,y,r/len(set1),g/len(set1),b/len(set1))
    set2 = image_list[1::2]
    image2 = Image(dimensions=set2[0].size)
    for x,y in image2.getpixellist():
        r,g,b = reduce(lambda a,b: (a[0]+b[0],a[1]+b[1],a[2]+b[2]),[image.imgData[x,y] for image in set2])
        image2.setpixel(x,y,r/len(set2),g/len(set2),b/len(set2))
    noise = subtract_image(image1,image2)
    denoise_set = [subtract_image(image,noise) for image in image_list]
    image3 = Image(dimensions=denoise_set[0].size)
    for x,y in image3.getpixellist():
        r,g,b = reduce(lambda a,b: (a[0]+b[0],a[1]+b[1],a[2]+b[2]),[image.imgData[x,y] for image in denoise_set])
        image3.setpixel(x,y,r/len(denoise_set),g/len(denoise_set),b/len(denoise_set))
    return image3

def average_noisefilter_all_delta(image_list):
    shuffle(image_list)
    set1 = image_list[0::2]
    image1 = Image(dimensions=set1[0].size)
    for x,y in image1.getpixellist():
        r,g,b = reduce(lambda a,b: (a[0]+b[0],a[1]+b[1],a[2]+b[2]),[image.imgData[x,y] for image in set1])
        image1.setpixel(x,y,r/len(set1),g/len(set1),b/len(set1))
    set2 = image_list[1::2]
    image2 = Image(dimensions=set2[0].size)
    for x,y in image2.getpixellist():
        r,g,b = reduce(lambda a,b: (a[0]+b[0],a[1]+b[1],a[2]+b[2]),[image.imgData[x,y] for image in set2])
        image2.setpixel(x,y,r/len(set2),g/len(set2),b/len(set2))
    noise = get_delta_image(image1,image2)
    denoise_set = [subtract_image(image,noise) for image in image_list]
    image3 = Image(dimensions=denoise_set[0].size)
    for x,y in image3.getpixellist():
        r,g,b = reduce(lambda a,b: (a[0]+b[0],a[1]+b[1],a[2]+b[2]),[image.imgData[x,y] for image in denoise_set])
        image3.setpixel(x,y,r/len(denoise_set),g/len(denoise_set),b/len(denoise_set))
    return image3

def modal_image(image_list):
    shuffle(image_list)
    result = Image(dimensions=image_list[0].size)
    for x,y in result.getpixellist():
        r = mode([image.imgData[x,y][0] for image in image_list])
        g = mode([image.imgData[x,y][1] for image in image_list])
        b = mode([image.imgData[x,y][2] for image in image_list])
        result.setpixel(x,y,r,g,b)
    return result

def test_func(f,images,original,trials=25):
    results = list()
    for x in range(trials):
        print "Trial #"+str(x+1)
        results.append(get_delta(f(images),original))
    return sum(results)/len(results)


function_list = [average_images_add,average_images_sub,average_images,average_noisefilter_all_sub,average_noisefilter_all_delta,modal_image]

def test_functions(image_list,original,functions=function_list,trials=10):
    out = ''
    for f in functions:
        out += (str(f) + ' ')
        out += (': ')
        out += (str(test_func(f,image_list,original,trials)))
        out += ('\n')
    print out
