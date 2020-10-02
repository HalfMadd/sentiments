from flask import Flask, request
from sentiment_detector import Sentiment

app = Flask(__name__)

@app.route('/prediction', methods=['POST'])
def prediction():
  sentiment = Sentiment()
  sentiment.set_sentiment(request.form['sentiment'])
  evaluation = sentiment.evaluate_sentiment()
  return evaluation
  pass

@app.route('/entrainement', methods=['GET'])
def entrainement():
  return 'entrainement'
  pass

if __name__ == '__main__':
  app.run()
  pass
