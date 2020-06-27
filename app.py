from flask import Flask, render_template, request
from selenium import webdriver
from flask_bootstrap import Bootstrap
from scrapper.scrap import *
import os
app = Flask(__name__)

Bootstrap(app)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/showimg', methods=["POST","GET"])
def showiamge():
    # GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google_chrome'
    # CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    chrome_options = webdriver.ChromeOptions()

    chrome_options.binary_location =os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    driver= webdriver.Chrome(executable_path= os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.binary_location = GOOGLE_CHROME_BIN
    # browser = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    # driver  = browser #'./chromedriver'
    if request.method == "POST":
        search_term=request.form['keyword']
        print(search_term)
        if len(search_term) <0:
            return "Please enter something."
        srch_img=search_and_download_image(search_term,driver)
        print(srch_img)
        try:
            if len(srch_img)>0:

                return render_template('showimg.html', srch_img=srch_img,keyword=search_term,srch_img_len=len(srch_img))
            else:
                return "Please try with a different string"
        except Exception as e:
            print('no Images found ', e)
            return "Please try with a different string"


if __name__ == '__main__':
    app.run()
