import requests

httpServer = "http://127.0.0.1:5000" 
pathImage = "a.jpg"
pathImageReplace = "_.jpg"

data = {'typeBlur': 6, 'kernelSize': 51, 'kernelDepth': 10}
files = {'image': open(pathImage, 'rb'), 'imageReplace': open(pathImageReplace, 'rb')}

result = requests.post(httpServer, data = data, files = files)

print("Status:", result)
print("Result:", result.text)