from PIL import Image
import numpy
from math import sqrt, pow


class WhiteImageAnalysis:

    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.width = self.image.width
        self.height = self.image.height
        self.pixels = self.image.load()
        self.threshold = (0, 0, 0, 255)
        self.edge_threshold = 200
        print("Loaded image at:", image_path)
        print("Image Width:", self.image.width, "Image Height:", self.image.height)

    def sobel(self, x, y):
        if x == 0 or x >= self.width - 1 or y == 0 or y >= self.height - 1:
            return 0
        gx = self.xSobel(x, y)
        gy = self.ySobel(x, y)
        return sqrt(pow(gx, 2) + pow(gy, 2))

    def xSobel(self, x, y):
        sobelx = numpy.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
        return abs(numpy.sum(self.caculateArray(sobelx, x, y)))

    def ySobel(self, x, y):
        sobely = numpy.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
        return abs(numpy.sum(self.caculateArray(sobely, x, y)))

    def caculateArray(self, m0, x, y):
        a00 = self.pixels[x - 1, y - 1][0]
        a01 = self.pixels[x, y - 1][0]
        a02 = self.pixels[x + 1, y - 1][0]
        a10 = self.pixels[x - 1, y][0]
        a11 = self.pixels[x, y][0]
        a12 = self.pixels[x + 1, y][0]
        a20 = self.pixels[x - 1, y + 1][0]
        a21 = self.pixels[x, y + 1][0]
        a22 = self.pixels[x + 1, y + 1][0]
        array = numpy.array([[a00, a01, a02], [a10, a11, a12], [a20, a21, a22]])
        return numpy.multiply(m0, array)

    def validArrayFactory(self):
        valid_array = [[False for pixely in range(self.height)] for pixelx in range(self.width)]
        count = 0
        for width in range(self.width):
            for height in range(self.height):
                # print("X:", width, "Y:", height, "Value:", self.pixels[width, height], "sobel:", self.sobel(width, height))
                if self.pixels[width, height] > self.threshold and self.sobel(width, height) > self.edge_threshold:
                    valid_array[width][height] = True
                    count += 1
                else:
                    valid_array[width][height] = False
        return valid_array, count


WIA = WhiteImageAnalysis("img/TestImage/TestImage.png")
print(WIA.xSobel(4,6))
#result = WIA.validArrayFactory()
#print(result[1])
