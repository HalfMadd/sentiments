from flask import Flask, request, render_template

from sentiment_detector import Sentiment

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')
  pass

@app.route('/prediction', methods=['POST'])
def prediction():
  sentiment = Sentiment()
  input_text = request.form['sentiment']
  evaluation = sentiment.evaluate_sentiment(input_text)
  message = ''
  if evaluation == 0:
    message = 'Désolé que notre produit ne vous ai pas plus.'
    pass
  else:
    message = 'Merci, au plaisir de vous revoir.'

  return render_template('reponse.html', sentiment=input_text, evaluation=message)
  pass

@app.route('/entrainement', methods=['GET'])
def entrainement():
  sentiment = Sentiment()
  accuray = sentiment.train_sentiment()
  return f'Entrainement effectué.\nPrécision : {accuray}%\n'
  pass

@app.route('/metrics')
def metrics():
  return render_template('metrics.html')
  pass

if __name__ == '__main__':
  app.run(debug=True)
  pass
