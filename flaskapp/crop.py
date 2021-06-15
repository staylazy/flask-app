import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import matplotlib.image
from PIL import Image
import random
import os
import io
import numpy


def get_croped_images(filename):
    
    original_img = Image.open(filename)

    img = matplotlib.image.imread(filename)

    width, height = original_img.size

    wid = width // 2
    hei = height // 2
    
    parts = []

    parts.append(original_img)
    parts.append(original_img.crop((0, 0, wid, hei)))
    parts.append(original_img.crop((wid, 0, width, hei)))
    parts.append(original_img.crop((0, hei, wid, height)))
    parts.append(original_img.crop((wid, hei, width, height)))

    for i in range(len(parts)):
        parts[i].save("./static/" + str(i) + '.png')
        parts[i] = "./static/" + str(i) + '.png'
    
    graphs = []

    print("0")
    x = img[:,:,0]
    plt.xlabel("value")
    plt.ylabel("pixels frequency")     
    plt.hist(x)
    plt.savefig('./static/charts/0.png')
    plt.clf()
    graphs.append('./static/charts/0.png')

    print("1")
    img = matplotlib.image.imread('./static/1.png')
    x = img[:,:,0]
    plt.xlabel("value")
    plt.ylabel("pixels frequency")     
    plt.hist(x)
    plt.savefig('./static/charts/1.png')
    plt.clf()
    graphs.append('./static/charts/1.png')

    print("2")
    img = matplotlib.image.imread('./static/2.png')
    x = img[:,:,0]
    plt.xlabel("value")
    plt.ylabel("pixels frequency")     
    plt.hist(x)
    plt.savefig('./static/charts/2.png')
    plt.clf()
    graphs.append('./static/charts/2.png')

    print("3")
    img = matplotlib.image.imread('./static/3.png')
    x = img[:,:,0]
    plt.xlabel("value")
    plt.ylabel("pixels frequency")     
    plt.hist(x)
    plt.savefig('./static/charts/3.png')
    plt.clf()
    graphs.append('./static/charts/3.png')

    print("4")
    img = matplotlib.image.imread('./static/4.png')
    x = img[:,:,0]
    plt.xlabel("value")
    plt.ylabel("pixels frequency")     
    plt.hist(x)
    plt.savefig('./static/charts/4.png')
    graphs.append('./static/charts/4.png')

    return parts, graphs

