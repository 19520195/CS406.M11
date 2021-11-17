import cv2

class convertImage:
  def __init__(self, image, coords):
    self.image  = image.copy()
    self.coords = coords

  def averageBlur(self, kernelSize):
    for x1, y1, x2, y2 in self.coords:
      sub = self.image[y1:y2, x1:x2]
      sub = cv2.blur(sub, (kernelSize, kernelSize))
      self.image[y1:y2, x1:x2] = sub
    return self.image

  def gaussianBlur(self, kernelSize):
    for x1, y1, x2, y2 in self.coords:
      sub = self.image[y1:y2, x1:x2]
      sub = cv2.GaussianBlur(sub, (kernelSize, kernelSize), 0)
      self.image[y1:y2, x1:x2] = sub
    return self.image

  def medianBlur(self, kernelSize):
    for x1, y1, x2, y2 in self.coords:
      sub = self.image[y1:y2, x1:x2]
      sub = cv2.medianBlur(sub, kernelSize)
      self.image[y1:y2, x1:x2] = sub
    return self.image

  def eightBitsBlur(self, kernelSize, kernelDepth=10):
    dst = self.image.copy()
    for x1, y1, x2, y2 in self.coords:
      sub = dst[y1:y2, x1:x2]
      height, width = sub.shape[:2]
      k = min([kernelSize, height, width])
      newHeight, newWidth = height // k, width // k

      blured = cv2.resize(sub, (newWidth, newHeight))
      blured = cv2.resize(blured, (width, height), interpolation=cv2.INTER_AREA)
      blured = blured // kernelDepth * kernelDepth

      dst[y1:y2, x1:x2] = blured
    return dst

  def replaceImage(self, image):
    for x1, y1, x2, y2 in self.coords:
      sub = self.image[y1:y2, x1:x2]
      height, width = sub.shape[:2]
      self.image[y1:y2, x1:x2] = cv2.resize(image, (width, height))
    return self.image

  def getResult(self, typeBlur, kernelSize, kernelDepth, imageReplace):
    if typeBlur == 1:
        return self.averageBlur(kernelSize)
    elif typeBlur == 2:
        return self.gaussianBlur(kernelSize)
    elif typeBlur == 3:
        return self.medianBlur(kernelSize)
    elif typeBlur == 4:
        return self.eightBitsBlur(kernelSize, kernelDepth)
    return self.replaceImage(imageReplace)
