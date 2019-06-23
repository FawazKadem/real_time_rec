from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

import cv2


camera = cv2.VideoCapture(0)
for i in range(10):
    return_value, image = camera.read()
    cv2.imwrite('opencv'+str(i)+'.png', image)
del(camera)




# Now there is a trained endpoint that can be used to make a prediction

ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com"
predictor = CustomVisionPredictionClient("a9b7310ff55441829878684390c89aae" ,endpoint=ENDPOINT)

with open("test.jpg", "rb") as image_contents:
    results = predictor.detect_image("ca2d87c7-9f53-4606-8db7-2cf0f410a075","test", image_contents.read())

    # Display the results.
    for prediction in results.predictions:
        print ("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100))
