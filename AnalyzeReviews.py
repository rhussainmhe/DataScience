import json
import random

#https://www.youtube.com/watch?v=M9Itm95JzL0

class Sentiment:
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"
    POSITIVE = "POSITIVE"

class Review:
    def __init__(self, text, score):
        self.text = text
        self.score = score
        self.sentiment = self.get_sentiment()

    def get_sentiment(self):
        if self.score <= 2:
            return Sentiment.NEGATIVE
        elif self.score == 3:
            return Sentiment.NEUTRAL
        else: #Score of 4 or 5
            return Sentiment.POSITIVE

#Create container class for even distribute method

class ReviewContainer:
    def __init__(self, reviews):
        self.reviews = reviews

    def get_text(self):
        return [x.text for x in self.reviews]

    def get_sentiment(self):
        return [x.sentiment for x in self.reviews]

    def evenly_distribute(self):
        negative = list(filter(lambda x: x.sentiment == Sentiment.NEGATIVE, self.reviews))
        positive = list(filter(lambda x: x.sentiment == Sentiment.POSITIVE, self.reviews))
        positive_shrunk = positive[:len(negative)]
        self.reviews = negative + positive_shrunk
        random.shuffle(self.reviews)


file_name = './output/spiderman.json'

reviews = []

with open(file_name) as f:
    for line in f:
        review = json.loads(line)
        reviews.append(Review(review['Review'], int(review['Rating'])))

from sklearn.model_selection import train_test_split

training, test = train_test_split(reviews, test_size = 0.33, random_state = 42)

train_container = ReviewContainer(training)

test_container = ReviewContainer(test)

train_container.evenly_distribute()
train_x = train_container.get_text()
train_y = train_container.get_sentiment()

test_container.evenly_distribute()
test_x = test_container.get_text()
test_y = test_container.get_sentiment()

print('printing train_y postive')
print(train_y.count(Sentiment.POSITIVE))
print('printing train_y negative')
print(train_y.count(Sentiment.NEGATIVE))

#42 mins Bag of Words vectorization
#tfid = term frequent inverse document frequency (counts important words over less important words)
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

vectorizer = TfidfVectorizer()
train_x_vectors = vectorizer.fit_transform(train_x)

test_x_vectors = vectorizer.transform(test_x)

print(train_x[1])
print(train_x_vectors[1])

#Decide what classifier to now use (CLF SVM)
from sklearn import svm

clf_svm = svm.SVC(kernel='linear')

clf_svm.fit(train_x_vectors, train_y)

print('Testing output test_x and train_x_vectors')
print(test_x[2])
print(train_x_vectors[2].toarray())

print('Printing SVM')
print(clf_svm.predict(test_x_vectors[0]))

# clf_svm.predict()

# Decision Tree
from sklearn.tree import DecisionTreeClassifier

clf_dec = DecisionTreeClassifier()
clf_dec.fit(train_x_vectors, train_y)

print('Decision Tree')
print(clf_dec.predict(test_x_vectors[0]))

# Naive Bayes
# from sklearn.naive_bayes import GaussianNB
#
# clf_gnb = GaussianNB()
# clf_gnb.fit(train_x_vectors, train_y)
#
# print('Gaussian Naive Bayes')
# print(clf_gnb.predict(test_x_vectors[0]))

# Logistic Regression
from sklearn.linear_model import LogisticRegression

clf_log = LogisticRegression()
clf_log.fit(train_x_vectors, train_y)

print('Logistic Regression')
print(clf_log.predict(test_x_vectors[0]))













# Predicting the test set correctly
print('Mean Accuracy')
print('Printing SVM accuracy')
print(clf_svm.score(test_x_vectors, test_y))
print('Printing Decision Tree accuracy')
print(clf_dec.score(test_x_vectors, test_y))
print('Printing Logisitic Regression accuracy')
print(clf_svm.score(test_x_vectors, test_y))


print('F1 Scores')
from sklearn.metrics import f1_score

print('F1 score SVM')
print(f1_score(test_y, clf_svm.predict(test_x_vectors), average=None, labels = [Sentiment.POSITIVE, Sentiment.NEUTRAL, Sentiment.NEGATIVE]))
print('F1 score Decision Tree')
print(f1_score(test_y, clf_dec.predict(test_x_vectors), average=None, labels = [Sentiment.POSITIVE, Sentiment.NEUTRAL, Sentiment.NEGATIVE]))
print('F1 score Logistic Regression')
print(f1_score(test_y, clf_log.predict(test_x_vectors), average=None, labels = [Sentiment.POSITIVE, Sentiment.NEUTRAL, Sentiment.NEGATIVE]))

print(train_y.count(Sentiment.POSITIVE))


#Qualitative analysis

test_set = ['great', 'bad book do not buy', 'horrible waste of time']
new_test = vectorizer.transform(test_set)

print(clf_svm.predict(new_test))

#increasing performance
#use TfidfVectorizer instead of CountVectorizer

#Tuning Model (with Grid Search)

from sklearn.model_selection import GridSearchCV

parameters = {'kernel': ('linear', 'rbf'), 'C': (1,4,8,16,32)}

svc = svm.SVC()
clf = GridSearchCV(svc, parameters, cv=5)
clf.fit(train_x_vectors, train_y)

print('printing Grid Search CV results')

print(clf.score(test_x_vectors, test_y))

# Saving Model
import pickle

with open('./output/sentiment_classifier.pkl', 'wb') as f:
    pickle.dump(clf, f)


with open('./output/sentiment_classifier.pkl', 'rb') as f:
    loaded_clf = pickle.load(f)

print(test_x[0])

print(loaded_clf.predict(test_x_vectors[0]))
