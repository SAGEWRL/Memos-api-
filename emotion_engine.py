import textblob

def detect_emotion(text):
    from textblob import TextBlob
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.4:
        return "positive"
    elif polarity < -0.2:
        return "negative"
    else:
        return "neutral"
