from flask import Flask, render_template
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import cv2

app = Flask(__name__)
import requests

# product codes that we are getting recommendations for

'''
20309646001_EA - salsa
20131170001_EA - corn
20325274001_KG - butternut squash
20912737_EA - rich & chewy bars
20666167008_EA - apple sauce baby food
'''

'''
code - product code
name - name of product
brand - brand of product
['imageAssets'][0]['mediumUrl'] - url of image
packageSize 
prices[price][value] - current price 
prices[wasPrice]
    if not on sale, then = None,
    if on sale, then prices[wasPrice][value] = old price
    
'''


def getRelatedProductsByProductName(productName):

    nameToCode = {
        'Chocolate': '20912737_EA',
        'Salsa': '20309646001_EA',
        'Corn': '0131170001_EA',
        'Squash': '20325274001_KG',
        'AppleSauce': '20666167008_EA'
    }

    return getRelatedProductsByProductCode(nameToCode[productName])


def getRelatedProductsByProductCode(productCode):
    cookies = {
        'JSESSIONID': '2D3B5883B46C13223FC1A55077EDBF3B.app2',
        'lcl_lang_pref': 'en',
        'customer_state': 'anonymous',
        'timeSlotExpiredRecorded': 'true',
        '_slid': 'b7ede498-1ffe-41e4-a729-c50d6c8d46b0',
        '_sl_session': '^{^%^22firstVisit^%^22:1561236056035^%^2C^%^22lastVisit^%^22:null^%^2C^%^22number^%^22:1^}',
        '_sl_session_beat': 'current',
        '_sl_analytics_visitor': 'true',
        'check': 'true',
        'last_selected_store': '1007',
        'PickupLocation': '1007',
        'PickupDate': '2019-06-25T15:00:00Z^[UTC^]',
        'loblaw-cart': '82258146-09fe-48ca-b2d8-83524139b4a7',
        'mbox': 'session^#1bdcc078bca14bd0b8d758e00e98bc43^#1561240007',
        '_sl_ping_marker': 'initial',
        '_sl_analytics_items': '^[^%^225cc5c699fea3900011f25598^%^22^%^2C^%^225cec4c86fea3900011f25928^%^22^]',
        'tp_mcd': '^[^%^225cec4c86fea3900011f25928^%^22^]',
        'ADRUM_BTa': 'R:45^|g:9b2cb711-092e-4777-b061-8be0d80f245f^|n:lblw_afe7f4d6-4637-4e11-95bb-0a169ff97498',
        'ADRUM_BT1': 'R:45^|i:350336^|e:129',
    }

    headers = {
        'Pickup-Location-Id': '1007',
        'Site-Banner': 'loblaw',
        'Accept-Language': 'en',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Content-Type': 'application/json;charset=utf-8',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.loblaws.ca/Food/Dairy-and-Eggs/Milk-^%^26-Cream/2^%-^%^26-Whole-Milk/2^%-Milk/p/20149754_EA',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    url = 'https://www.loblaws.ca/api/product/' + productCode + '/recommendations'
    response = requests.get(url, headers=headers, cookies=cookies)
    return response.json()['relatedProducts']

getRelatedProductsByProductName('Salsa')[0]['name']

def take_image():
    camera = cv2.VideoCapture(0)
    for i in range(5):
        return_value, image = camera.read()
    cv2.imwrite('test.png', image)    
    return image

def get_result(image):


    # Now there is a trained endpoint that can be used to make a prediction

    ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com"
    predictor = CustomVisionPredictionClient("a9b7310ff55441829878684390c89aae" ,endpoint=ENDPOINT)

    with open("test.png", "rb") as image_contents:
        results = predictor.detect_image("ca2d87c7-9f53-4606-8db7-2cf0f410a075","test", image_contents.read())
        
        return set([item.tag_name for item in results.predictions if item.probability > .5])


# two decorators, same function
@app.route('/')
@app.route('/index.html')
def index():
    image = take_image()
    results = get_result(image)
    alternates = getRelatedProductsByProductName("Salsa")
    return render_template('index.html', the_title=results, recommendations=alternates)

@app.route('/symbol.html')
def symbol():
    return render_template('symbol.html', the_title='Tiger As Symbol')

@app.route('/myth.html')
def myth():
    return render_template('myth.html', the_title='Tiger in Myth and Legend')

if __name__ == '__main__':
    app.run(debug=True)
