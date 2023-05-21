# Example of Python Flask app with /webhook endpoint
# for processing events sent by Blockfrost Secure Webhooks
from flask import Flask, request, json
from blockfrost import verify_webhook_signature, SignatureVerificationError

SECRET_AUTH_TOKEN = "SECRET-WEBHOOK-AUTH-TOKEN"

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Validate webhook signature
        request_bytes = request.get_data()
        # try:
        #     verify_webhook_signature(
        #         request_bytes, request.headers['Blockfrost-Signature'], SECRET_AUTH_TOKEN)
        # except SignatureVerificationError as e:
        #     # for easier debugging you can access passed header and request_body values (e.header, e.request_body)
        #     print('Webhook signature is invalid.', e)
        #     return 'Invalid signature', 403

        # Get the payload as JSON
        event = request.json

        print('Received request id {}, webhook_id: {}'.format(
            event['id'], event['webhook_id']))

        if event['type'] == "block":
            # process Block event
            print('Received block hash {}'.format(event['payload']['hash']))
        elif event['type'] == "...":
            # truncated
            print('Unexpected event type {}'.format(event['type']))
        else:
            # Unexpected event type
            print('Unexpected event type {}'.format(event['type']))

        return 'Webhook received', 200
    else:
        return 'POST Method not supported', 405


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=6666, debug=True)