# output.py
# Usage 1: python output.py --typeinput image --input testcases/input/image_1.jpg --output testcases/output/image_1.jpg \
#                [--typeblur 6 --kernesize 15 --kerneldepth 10 --imagereplace static/images/_.jpg]
# Usage 2: python output.py --typeinput video --input testcases/input/video_1.mp4 --output testcases/output/video_1.avi \
#                [--typeblur 6 --kernesize 15 --kerneldepth 10 --imagereplace static/images/_.jpg]
# Authors: Nguyen Ngoc Lan Phuong <19520227@gm.uit.edu.vn>
#          Cao Hung Phu           <19520214@gm.uit.edu.vn>
#          Le Quang Nha           <19520195@gm.uit.edu.vn>

# %% Import library

import argparse
import os
from tqdm import tqdm
from config import *
from censorLicensePalate import *

# %% Main
if __name__ == '__main__':
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--typeinput', type=str, default='image')
    parser.add_argument('--input', type=str, default='testcases/input/image_1.jpg')
    parser.add_argument('--output', type=str, default='testcases/output/image_1.jpg')
    parser.add_argument('--typeblur', type=int, default='5')
    parser.add_argument('--kernesize', type=int, default='15')
    parser.add_argument('--kerneldepth', type=int, default='10')
    parser.add_argument('--imagereplace', type=str, default='static/images/_.jpg')
    
    # Get arguments
    args = parser.parse_args()
    detectType = args.typeinput.lower()
    inputFile = args.input
    outputFile = args.output
    typeBlur = args.typeblur
    kerneSize = args.kernesize
    kernelDepth = args.kerneldepth
    inputFileReplace = args.imagereplace


    # Check arguments
    if detectType not in ['image', 'video']:
        print("Error type!!!")
        print("Type: image, video")
        print("Example 1: python output.py --typeinput image --input testcases/input/image_1.jpg --output testcases/output/image_1.jpg \
                [--typeblur 5 --kernesize 15 --kerneldepth 10 --imagereplace static/images/_.jpg]")
        print("Example 2: python output.py --typeinput video --input testcases/input/video_1.mp4 --output testcases/output/video_1.avi \
                [--typeblur 5 --kernesize 15 --kerneldepth 10 --imagereplace static/images/_.jpg]")
        exit()
        
    if not os.path.exists(inputFile):
        print("Error input: Input not found!!!")
        exit()
        
    if not os.path.exists(inputFileReplace):    
        print("Error input replace: Input replace not found!!!")
        exit()
    imageReplace = cv2.imread(inputFileReplace)

    # Load detector
    detector = None
    if CFG_MODEL == 'yolo':
        from modelYOLO import *
        detector = modelYOLO()
    else:
        from modelFasterRCNN import *
        detector = modelFasterRCNN()

    if detectType == 'video':
        # Read input video
        imReader = cv2.VideoCapture(inputFile)
        frWidth  = int(imReader.get(cv2.CAP_PROP_FRAME_WIDTH))
        frHeight = int(imReader.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frNumber = int(imReader.get(cv2.CAP_PROP_FRAME_COUNT))  # Number of frames
        frPS     = imReader.get(cv2.CAP_PROP_FPS)               # Frame per second

        # Print information
        print('=== CAPTURE INFORMATION ===')
        print('Input path      : {}'.format(inputFile))
        print('Output path     : {}'.format(outputFile))
        print('Frame size      : {} x {}'.format(frWidth, frHeight))
        print('Number of frame : {}'.format(frNumber))
        print('Frame per second: {}'.format(frPS))

        # Write output
        imWriter = cv2.VideoWriter(outputFile, cv2.VideoWriter_fourcc(*'XVID'), frPS, (frWidth, frHeight))
        for frIndex in tqdm(range(frNumber)):
            _, image = imReader.read()
            if _:
                listCoors = detector.predict(image)
                imageResult = convertImage(image, listCoors).getResult(typeBlur, kerneSize, kernelDepth, imageReplace)
                imWriter.write(imageResult)

    else:
        # Read input image
        print('Input path: {}'.format(inputFile))
        image = cv2.imread(inputFile)
        listCoors = detector.predict(image)
        imageResult = convertImage(image, listCoors).getResult(typeBlur, kerneSize, kernelDepth, imageReplace)
        # Write output image
        cv2.imwrite(outputFile, imageResult)
        print('Output path: {}'.format(outputFile))