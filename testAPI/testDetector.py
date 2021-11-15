import requests

httpServer = "http://127.0.0.1:5000" 
pathImage = "a.jpg"

result = requests.post(httpServer, files = {'image': open(pathImage, 'rb')})
print("Status:", result)
print("Result:", result.text)