# -*- coding: utf-8 -*-
from goprocam import GoProCamera
from goprocam import constants
import time
camera = GoProCamera.GoPro()

print(camera.infoCamera())
print(camera.getStatusRaw())
import pdb; pdb.set_trace()

camera.take_photo(1)
time.sleep(10)

camera.shoot_video(10)

print("DONE")