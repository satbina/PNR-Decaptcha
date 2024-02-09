import requests
import pickle
import cv2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
s = requests.Session()
loaded_model = pickle.load(open("models/model.sav", "rb"))


def download_image(url, save_path):
    try:
        response = s.get(url, stream=True)
        response.raise_for_status()
        with open(save_path + ".png", "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print("Image downloaded successfully.")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return False


def segment(image, st):
    flag = 0
    flag2 = 0
    start = 0
    end = 0
    for i in range(st, 149):
        for j in range(30):
            if image[j, i] != 0:
                flag = 1
                if start == 0:
                    start = i - 2
                flag2 = 1
        if flag == 0 and flag2 == 1:
            end = i + 2
            break
        flag = 0
    finalImage = image[:, start:end]
    return finalImage, end


def predict_number():
    dfX = []
    image_url = "https://www.indianrail.gov.in/enquiry/captchaDraw.png?1690016648505"
    save_location = "predict/" + str(0)
    download_image(image_url, save_location)
    image = cv2.imread("predict/0.png", cv2.IMREAD_UNCHANGED)
    trans_mask = image[:, :, 3] == 0
    image[trans_mask] = [255, 255, 255, 255]
    image = cv2.bitwise_not(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    image = cv2.resize(image, (150, 30))
    end = 0
    for i in range(6):
        finalImage, end = segment(image, end)
        finalImage = cv2.resize(finalImage, (25, 25))
        dummy = []
        finalImage = finalImage.flatten()
        dummy.append(finalImage)
        if loaded_model.predict(dummy) == [12]:
            break
        dfX.append(finalImage)
    y_pred = loaded_model.predict(dfX)
    plus = 0
    dig1 = 0
    dig = 0
    for i in y_pred:
        if i == 10 or i == 11:
            if i == 10:
                plus = 1
            dig1 = dig
            dig = 0

        else:
            dig = dig * 10 + i
    if plus:
        dig1 += dig
    else:
        dig1 -= dig
    return dig1


def get_pnr_status(captcha, pnr_number):
    base_url = f"https://www.indianrail.gov.in/enquiry/CommonCaptcha?inputCaptcha={captcha}&inputPnrNo={pnr_number}&inputPage=PNR&language=en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    response = s.get(base_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        s.close()
        return None


@app.route("/finpredict", methods=["GET"])
def finpredict():
    captcha = predict_number()  # Replace with your desired captcha value
    pnr_number = int(
        request.args.get("pnrnumber")
    )  # Replace with your desired PNR number

    json_data = get_pnr_status(captcha, pnr_number)

    return json_data


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
