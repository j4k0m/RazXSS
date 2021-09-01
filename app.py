from flask import Flask, request, render_template
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

app = Flask(__name__)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":f"{open('./flag.txt', 'r').read()}", "platform":"Windows"})

def xss_filter(string):
    string = string.replace('script', "").replace("alert", "").replace("prompt", "").replace("confirm", "").replace('"', '"\\').replace("'", "'\\")
    if "script" not in string and "alert" not in string and "prompt" not in string and "confirm" not in string:
        return string
    return xss_filter(string)

@app.route("/")
def home():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RazinkanXSS</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Ubuntu:wght@300&display=swap" rel="stylesheet">
</head>
<body>
    <h1 style="text-align: center;font-family: 'Ubuntu', sans-serif;">RazinkanXSS</h1>
    <p style="text-align: center;font-family: 'Ubuntu', sans-serif;">Hi {}!, Try to bypass the filter and get your XSS payload to execute. <a style="margin-left: 2px;" href="?name=InsaneHacker">click me</a></p>
    <div class="wrapper" style="text-align: center;">
        <button onclick="window.location.href='/review_admin'">Send to Admin</button>
    </dib>
</body>
</html>""".format(xss_filter("Hacker" if not request.args.get('name') else request.args.get('name')))

@app.route("/review", methods=["POST"])
def review():
    if request.method == "POST":
        if request.form["url"]:
            if request.form["url"].split("/")[2] == request.host_url.split('/')[2]:
                driver.get(request.form["url"])
                return "Sent to Admin."
            else:
                return "Invalid URL."
        else:
            return "No url parameter."

@app.route("/review_admin", methods=["GET"])
def review_admin():
    return render_template("send_review.html")

app.run(host="0.0.0.0", port=5050)