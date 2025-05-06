import os.path
from pathlib import Path
import time
from ctypes import *
from sys import platform
from numpy.ctypeslib import ndpointer
import numpy as np

from PIL import Image

import eyeRendererHelperFunctions as eyeTools

home_dir = str(Path.home())

# Load the renderer
eyeRenderer = CDLL(home_dir + "/compound-ray/build/make/lib/libEyeRenderer3.so")
print("Successfully loaded ", eyeRenderer)

# Configure the renderer's function outputs and inputs using the helper functions
eyeTools.configureFunctions(eyeRenderer)

# Load a scene
# eyeRenderer.loadGlTFscene(c_char_p(b"../data/ofstad-arena/ofstad-acceptance-angle.gltf"))
# eyeRenderer.loadGlTFscene(c_char_p(b"../data/natural-standin-sky.gltf"))
# eyeRenderer.loadGlTFscene(c_char_p(b"../data/test-scene/test-scene.gltf"))
eyeRenderer.loadGlTFscene(c_char_p(b"/groups/turaga/home/kimb2/compound-ray/data/ofstad-arena/ofstad-arena-single-compound-eye.gltf"))

renderWidth = 700
renderHeight = 300
eyeTools.setRenderSize(eyeRenderer, renderWidth, renderHeight)

# Choose an eye
# eyeRenderer.gotoCameraByName(c_char_p(b"insect-eye-spherical-projector"))
# eyeRenderer.gotoCameraByName(c_char_p(b"insect-cam-1"))
eyeRenderer.gotoCameraByName(c_char_p(b"split-central-insect-cam-1000"))


Path(home_dir + "/compound-ray/python-examples/alias-demonstration/output/generated-data/alias-demonstration/").mkdir(parents=True, exist_ok=True)

samples = 100
eyeRenderer.setCurrentEyeSamplesPerOmmatidium(samples)
eyeRenderer.renderFrame() # First call to ensure randoms are configured
# renderTime = eyeRenderer.renderFrame() # Second call to actually render the image
#print("Rendered with {:n} in {d:} milliseconds.".format(s, renderTime))

def setPositionNRender(x, y, z, filehead=None):
    eyeRenderer.setCameraPosition(x, y, z)
    renderTime = eyeRenderer.renderFrame()
    if filehead is not None:
        eyeRenderer.saveFrameAs(c_char_p((home_dir+"/compound-ray/python-examples/alias-demonstration/output/generated-data/alias-demonstration/"+filehead+"_test-image-"+str(samples)+"-samples.ppm").encode()))

setPositionNRender(-5, 2, 0, "-1")
setPositionNRender(0, 2, 0, "0")
setPositionNRender(5, 2, 0, "1")
setPositionNRender(10, 2, 0, "2")
setPositionNRender(20, 2, 0, "3")


# eyeRenderer.setCameraPosition(0, 0.1, 0)
# renderTime = eyeRenderer.renderFrame()
# eyeRenderer.saveFrameAs(c_char_p((home_dir+"/compound-ray/python-examples/alias-demonstration/output/generated-data/alias-demonstration/1_test-image-"+str(samples)+"-samples.ppm").encode()))

# eyeRenderer.setCameraPosition(0, 0.2, 0)
# renderTime = eyeRenderer.renderFrame()
# eyeRenderer.saveFrameAs(c_char_p((home_dir+"/compound-ray/python-examples/alias-demonstration/output/generated-data/alias-demonstration/2_test-image-"+str(samples)+"-samples.ppm").encode()))

# eyeRenderer.setCameraPosition(0, 0.3, 0)
# renderTime = eyeRenderer.renderFrame()
# eyeRenderer.saveFrameAs(c_char_p((home_dir+"/compound-ray/python-examples/alias-demonstration/output/generated-data/alias-demonstration/3_test-image-"+str(samples)+"-samples.ppm").encode()))

import pdb; pdb.set_trace()

eyeRenderer.stop() # Stop the renderer