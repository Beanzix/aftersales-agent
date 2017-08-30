#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "shipping.cost":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("shipping-zone")

    cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}

    speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."

    # wx add below
    if req.get("result").get("action") != "return.policy-choice": #intent
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("return-choice")

    choice-policy = {
                    'online returns':'please label your online ID and order number in the package you are returning. ',
                    'gift returns':'gift refunds will be issued as an eGift Card within 24 hours of us receiving your returned item(s).',
                    'returns in-store':'please bring your original receipt and return the product in any Orange retail store.'
                    }

    speech = "The policy to " + zone + " is " + str(choice-policy[zone])
#wx add above
    
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print (f"Starting app on port {port}")

    app.run(debug=True, port=port, host='0.0.0.0')
