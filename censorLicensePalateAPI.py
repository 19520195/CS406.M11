import cv2

class convertImage:
  def __init__(self, image, coords):
    self.image  = image.copy()
    self.coords = coords

  def averageBlur(self, kernelSize):
    for x1, y1, x2, y2 in self.coords:
      LP = self.image[y1:y2, x1:x2]
      LP = cv2.blur(LP, (kernelSize, kernelSize))
      self.image[y1:y2, x1:x2] = LP
    return self.image

  def gaussianBlur(self, kernelSize):
    for x1, y1, x2, y2 in self.coords:
      sub = self.image[y1:y2, x1:x2]
      sub = cv2.GaussianBlur(sub, (kernelSize, kernelSize), 0)
      self.image[y1:y2, x1:x2] = sub
    return self.image

  def medianBlur(self, kernelSize):
    for x1, y1, x2, y2 in self.coords:
      subImage = self.image[y1:y2, x1:x2]
      subImageBlur = cv2.medianBlur(subImage, kernelSize)
      self.image[y1:y2, x1:x2] = subImageBlur
    return self.image

  def eightBitsBlur(self, kernelSize, kernelDepth):
    dst = self.image.copy()
    for x1, y1, x2, y2 in self.coords:
      sub = dst[y1:y2, x1:x2]
      height, width = sub.shape[:2]
      newHeight, newWidth = height // kernelSize, width // kernelSize

      blured = cv2.resize(sub, (newWidth, newHeight))
      blured = cv2.resize(blured, (width, height), interpolation=cv2.INTER_AREA)
      blured = blured // kernelDepth * kernelDepth

      dst[y1:y2, x1:x2] = blured
    return dst
    
  def replaceImage(self, image):
    for x1, y1, x2, y2 in self.coords:
      subImage = self.image[y1:y2, x1:x2]
      height, width = subImage.shape[:2]
      self.image[y1:y2, x1:x2] = cv2.resize(image, (width, height))
    return self.image


