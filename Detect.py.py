import cv2



def faceBox(faceNet,frame):
    frameHeight =frame.shape[0]
    frameWidth=frame.shape[1]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (227,227), [104,177,123], swapRB=False)
    faceNet.setInput(blob)
    detection = faceNet.forward()
    bboxs=[]
    for i in range(detection.shape[2]):
       confidence = detection[0,0,i,2]
       if confidence>0.7:
           x1=int(detection[0,0,i,3]*frameWidth)
           y1=int(detection[0,0,i,4]*frameHeight)
           x2=int(detection[0,0,i,5]*frameWidth)
           y2=int(detection[0,0,i,6]*frameHeight)
           bboxs.append([x1,y1,x2,y2])
           cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 1)

    return frame, bboxs

faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"

ageProto = "age_deploy.prototxt"
ageModel = "age_net.caffemodel"

genderProto = "gender_deploy.prototxt"
genderModel = "gender_net.caffemodel"



faceNet=cv2.dnn.readNet(faceModel, faceProto)
ageNet=cv2.dnn.readNet(ageModel,ageProto)
genderNet=cv2.dnn.readNet(genderModel,genderProto)

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2 years)', '(4-6 years)', '(8-12 years)', '(15-20 years)', '(25-32 years)', '(38-43 years)', '(48-53 years)', '(60-100 years)']
genderList = ['MALE', 'FEMALE']


video = cv2.VideoCapture(0)

while(True):
    ret, frame = video.read()
    frame, bboxs = faceBox(faceNet, frame)
    for bbox in bboxs:
        face = frame[bbox[1]:bbox[3],bbox[0]:bbox[2]]
        blob = cv2.dnn.blobFromImage(face,1.0,(227, 227),MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderpred=genderNet.forward()
        gender=genderList[genderpred[0].argmax()]


        ageNet.setInput(blob)
        agepred=ageNet.forward()
        age=ageList[agepred[0].argmax()]

        label = "{},{}".format(gender, age)
        cv2.putText(frame, label,(bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_PLAIN, 1.0, (255,255,255), 2)
    cv2.imshow('PROJECT   BY   AWULU VICTOR    FPI/HND/COM/20/047 ', frame)
    k=cv2.waitKey(1)
    if k==ord('q'):
         break
video.release()
cv2.destroyAllWindows()