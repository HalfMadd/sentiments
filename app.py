from flask import Flask, request

from sentiment_detector import Sentiment

app = Flask(__name__)

@app.route('/prediction', methods=['POST'])
def prediction():
  sentiment = Sentiment()
  evaluation = sentiment.evaluate_sentiment(request.form['sentiment'])
  return evaluation
  pass

@app.route('/entrainement', methods=['GET'])
def entrainement():
  sentiment = Sentiment()
  sentiment.train_sentiment()
  return 'Entrainement effectué'
  pass

if __name__ == '__main__':
  app.run()
  pass
