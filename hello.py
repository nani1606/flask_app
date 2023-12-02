from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load tweets data globally at application startup
try:
    with open('100tweets.json', 'r', encoding='utf-8') as file:
        tweets_data = json.load(file)
except FileNotFoundError as error:
    tweets_data = []  # Empty list if file not found
    print(f"Error: {error}")

@app.route("/", methods=["GET"])
def hello_world():
    name = request.args.get('name', 'Guest')  
    return f"<p>Hello, {name}</p>"

@app.route("/tweets", methods=['GET'])
def get_tweets():
    return jsonify(tweets_data)

@app.route('/tweets/filter', methods=['GET'])
def get_filtered_tweets():
    user_name = request.args.get('user_name')
    try:
        if user_name:
            filtered_tweets = [tweet for tweet in tweets_data if tweet.get('user_name') == user_name]
            return jsonify(filtered_tweets)
        else:
            return jsonify(tweets_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Other errors

@app.route('/tweets/<int:tweet_id>', methods=['GET'])
def get_specific_tweet(tweet_id):
    try:
        tweet = next((tweet for tweet in tweets_data if tweet.get('id_str') == str(tweet_id)), None)
        print(tweet)
        if tweet:
            return jsonify(tweet)
        else:
            return jsonify({"error": "Tweet not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
