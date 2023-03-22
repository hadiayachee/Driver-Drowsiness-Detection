
import cv2
import numpy as np
import time
import serial
# Load Yolo
#ARDUINO
arduino = serial.Serial(port='COM4', baudrate=57600, timeout=.1)

counter=0



net = cv2.dnn.readNetFromDarknet("custom-yolov4-tiny-detector (5).cfg",r"custom-yolov4-tiny-detector_best (5).weights")

classes = ['Sleeping','Awake']

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loading camera

cap = cv2.VideoCapture(0)
#address= "http://192.168.43.18:8080/video"
#address= "http://192.168.1.104:8080/video"
#address= "http://192.168.1.100:8080/video"
#cap.open(address)
#cap = cv2.VideoCapture(0)

font = cv2.FONT_HERSHEY_PLAIN
starting_time = time.time()
frame_id = 0
while True:
    _, frame = cap.read()

    frame_id += 1

    height, width, channels = frame.shape
	    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])


            def write_read(x):
                arduino.write(bytes(x, 'utf-8'))
                time.sleep(0.05)
                data = arduino.readline()
                return data


            if True:

                # while (port.isOpen()):

                if ((label == "Sleeping")):
                    # temp = '1'
                    # arduino.write(temp.encode())
                    # arduino.write('1')
                    # counter=counter+1
                    arduino.write(str.encode('1'))

                    # print(label)

                else:
                    # temp = '0'
                    # arduino.write(temp.encode())
                    # arduino.write('0')
                    arduino.write(str.encode('0'))

            # print(label)
            # if label == "WITHOUT MASK"

            confidence = confidences[i]
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.rectangle(frame, (x, y), (x + w, y + 20), color, -1)
            if label == "Sleeping":
                counter = counter + 1

                if counter > 8:
                    cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 10), font, 1, (255, 255, 255),
                                1)

                else:

                    cv2.putText(frame, "Awake" + " " + str(round(confidence, 2)), (x, y + 10), font, 1, (255, 255, 255),
                                1)
            else:
                cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 10), font, 1, (255, 255, 255), 1)
                counter = 0

    elapsed_time: float = time.time() - starting_time
    fps = frame_id / elapsed_time
    cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 3, (0, 0, 0), 3)
    print(fps)
    cv2.imshow("Image", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
