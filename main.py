import os
from multiprocessing.dummy import Pool

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

from WhiteImageAnalysis import WhiteImageAnalysis

class DisplayValidatedImage(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        pool = Pool(4)
        level = 0
        img_array = []
        lvl_array = []

        for img in os.listdir("C:/Users/db217620/Documents/Python/Panda3d/WhiteImageAnalysis/img/"):
            if img.endswith(".jpg"):
                self.process_image(img, level)
                level += 1

    def process_image(self, img, level):
        print("Processing", img)
        wia = WhiteImageAnalysis(os.path.join("img", img))
        wia.threshold = (250, 250, 250, 255)
        array = wia.validArrayFactory()

        x_var = 1
        y_var = 1
        z_var = 1

        array_p = GeomVertexArrayFormat()
        array_p.addColumn('vertex', 3, Geom.NTFloat32, Geom.CPoint)

        format_a = GeomVertexFormat()
        format_a.addArray(array_p)
        format_a = GeomVertexFormat.registerFormat(format_a)

        vdata = GeomVertexData('name', format_a, Geom.UHStatic)

        vertex = GeomVertexWriter(vdata, 'vertex')

        vertex_count = 0
        prim = GeomPoints(Geom.UHStatic)

        for width in range(wia.width):
            for height in range(wia.height):
                if array[0][width][height]:
                    vertex.addData3f(width * x_var, height * y_var, level * z_var)
                    prim.addVertex(vertex_count)
                    vertex_count += 1

        prim.closePrimitive()

        geom = Geom(vdata)
        geom.addPrimitive(prim)

        node = GeomNode('gnode')
        node.addGeom(geom)

        nodePath = self.render.attachNewNode(node)
        nodePath.setRenderModeThickness(5)
        nodePath.reparentTo(self.render)

app = DisplayValidatedImage()
app.run()
