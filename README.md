# Homework - LineBot

## Setup
### How to run
* **Step 1: Install Python Packages**
    * > pip install -r requirements.txt
* **Step 2: Modifiy `.env.sample` and save as `.env`**
    ```
    LINE_TOKEN = Your Line Token
    LINE_SECRET = Your Line Secret
    LINE_UID = Your Line UID
    ```
* **Step 3: Run `main.py`**
    * The port used in calculator_main.py is '8787'
    * > python3 main.py

* **Step 4: Run ngrok**
    * > ngrok http 8787
    

## How to use in LineBot
*  a + b
    * Add two numbers a+b
*  a - b
    * Subtract two numbers a-b
*  a * b
    * Multiply two numbers a*b
*  a / b
    * Divide two numbers a/b
    * If Division of zero, will get error
*  #help
    * View hint
*  Input any sticker
    * Return random sticker
