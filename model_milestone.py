
# For cs230 project -- Citation: adapted from https://medium.com/jatana/unsupervised-text-summarization-using-sentence-embeddings-adb15ce83db1

import numpy as np
import skipthoughts
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from nltk.tokenize import sent_tokenize

def preprocessSkip(text):
	print(text)
	text = skipthoughts.preprocess(text)
	print(text)
	return text

def gatherReviewAsList(filepath):
	text = []
	file = open(filepath, 'r')
	for line in file:
		text.append(line)
	file.close()
	return text

def gatherReviews(filepath):
	reviews = []
	file = open(filepath, 'r')
	for line in file:
		if not line == '\n':
			reviews.append(line)

	n_reviews = len(reviews)
	for i in range(n_reviews):
		review = reviews[i]
		lines = review.split('\n')
		for j in reversed(range(len(lines))):
			lines[j] = lines[j].strip()
			if lines[j] == '':
				lines.pop(j)
				reviews[i] = ' '.join(lines)
	return reviews

def encodeSentences(reviews):
	enc_reviews = [None]*len(reviews)
	cum_sum_sentences = [0]
	sent_count = 0
	for review in reviews:
		sent_count += len(review)
		cum_sum_sentences.append(sent_count)

	print('Loading pretrained model...')
	model = skipthoughts.load_model()
	encoder = skipthoughts.Encoder(model)
	print('Encoding sentences...')
	enc_sentences = encoder.encode(reviews, verbose=False)
	return enc_sentences 

def kmeans(enc_sentences, review):
	print('Starting clustering...')
	n_clusters = int(np.ceil(len(enc_sentences)**0.5))
	kmeans = KMeans(n_clusters=n_clusters, random_state=0)
	kmeans = kmeans.fit(enc_sentences)
	avg = []
	closest = []
	for j in range(n_clusters):
		idx = np.where(kmeans.labels_ == j)[0]
		avg.append(np.mean(idx))
	closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, \
													enc_sentences)
	ordering = sorted(range(n_clusters), key=lambda k: avg[k])
	summary_volume = []
	for idx in ordering:
		summary_volume.append(review[idx])
	return summary_volume

def main():
	#print('Gathering reviews...')
	#reviews = gatherReviews('listing_sample.txt')
	processed_review = gatherReviewAsList('expanded_sample.txt')
	enc_sentences = encodeSentences(processed_review)
	print('This is the processed_review: (size = ' + str(len(processed_review)))
	for i in range(len(processed_review)):
		print(i)
		print(processed_review[i]) # this is a sentence
	print('This is the corresponding encodings (size = ' + str(len(enc_sentences)))
	for i in range(len(enc_sentences)):
		print(i)
		print(enc_sentences[i])	# this is a sentence encoding
	
	summary = kmeans(enc_sentences, processed_review)
	print('Here is the original: ' + str(processed_review))
	print('Here are the chosen sentences: ')
	print(summary)




if __name__ == '__main__':
	main()
