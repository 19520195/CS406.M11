import requests
import cv2
import json
import numpy as np


path_save = "temp/"
path_image = "a.jpg" # Thay path ảnh ở đây
path_image_replace = "_.jpg" # Thay path ảnh replace ở đây
server = "http://127.0.0.1:5000" # Thay server ở đây


files = {'image': open(path_image, 'rb'), 'imageReplace': open(path_image_replace, 'rb')}
typeObj = {'typeBlur': 6, 'kernelSize': 51}
result = requests.post(server, data = typeObj, files = files)
print("Status:", result.text.replace("'", '"'))

# image = cv2.imread(path_image)
# image_replace = cv2.imread(path_image_replace)
# kernel_size = 51

# list_coors = json.loads(result.text.replace("'", '"'))['data']

# image_res_1 = cheBienSoXeAPI(image, list_coors).medianBlur(kernel_size)
# image_res_2 = cheBienSoXeAPI(image, list_coors).replaceImage(image_replace)

# cv2.imwrite("res_b_1.jpg", image_res_1)
# cv2.imwrite("res_b_2.jpg", image_res_2)

# image_scale_down = 2
# x = (int)(image.shape[1]/image_scale_down)
# y = (int)(image.shape[0]/image_scale_down)

# cv2.imshow(path_image, cv2.resize(image_res_1, (x, y)))
# cv2.imshow(path_image, cv2.resize(image_res_2, (x, y)))
# cv2.waitKey(0)
# cv2.destroyAllWindows() 