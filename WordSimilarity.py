#!~/data/anaconda3/bin/python

'''
Author: Abhishek Sharma

Program: Word Similarity by Context, Sequency and Synonym. 

Last Modified: Jan 31, 2018
'''

from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag
import difflib
import spacy
import sys

class WordSimilarity(object):

	def __init__(self):
		self.nlp = spacy.load('en')
		print(self.issimilar(sys.argv[1],sys.argv[2]))

	def difflib_similarity(self,keyword_1,keyword_2):
		seq=difflib.SequenceMatcher(None, keyword_1,keyword_2)
		percentage = seq.ratio()*100
		return percentage

	def spacy_similarity(self,keyword_1,keyword_2,nlp):
		keyword1 = nlp(keyword_1)
		keyword2 = nlp(keyword_2)
		percentage = float((keyword1.similarity(keyword2)) * 100)
		return percentage

	def penn_to_wn(self,tag):

		if tag.startswith('N'):
			return 'n'
		if tag.startswith('V'):
			return 'v'
		if tag.startswith('J'):
			return 'a'
		if tag.startswith('R'):
			return 'r'
		return None

	def tagged_to_synset(self,word, tag):

		wn_tag = self.penn_to_wn(tag)
		if wn_tag is None:
			return None
		try:
			return wn.synsets(word, wn_tag)[0]
		except:
			return None

	def wordnet_similarity(self,sentence1, sentence2):

		sentence1 = pos_tag(word_tokenize(sentence1))
		sentence2 = pos_tag(word_tokenize(sentence2))

		synsets1 = [self.tagged_to_synset(*tagged_word) for tagged_word in sentence1]
		synsets2 = [self.tagged_to_synset(*tagged_word) for tagged_word in sentence2]

		synsets1 = [ss for ss in synsets1 if ss]
		synsets2 = [ss for ss in synsets2 if ss]

		score, count = 0.0, 0
		for synset in synsets1:
			arr_simi_score = []
			for ss in synsets2:
				score_ = synset.path_similarity(ss)
				if score_ is not None:
					arr_simi_score.append(score_)

			if (len(arr_simi_score) > 0):
				best_score = max(arr_simi_score)
				if best_score is not None:
					score += best_score
					count += 1
		try:
			score /= count
		except Exception as error:
			score = 0.0
		return float(score * 100)
	
	def issimilar(self,keyword1,keyword2):
		
		difflib_score = round(self.difflib_similarity(keyword1.strip(),keyword2.strip()),2)
		wordnet_score_a = self.wordnet_similarity(keyword1.strip(),keyword2.strip())
		wordnet_score_b = self.wordnet_similarity(keyword2.strip(),keyword1.strip())
		wordnet_score = round(min(wordnet_score_a,wordnet_score_b),2)
		spacy_score = round(self.spacy_similarity(keyword1,keyword2,self.nlp),2)
		spacy_percentage = float((5 * spacy_score)/100)
		wordnet_percentage = float((20 * wordnet_score)/100)
		difflib_percentage = float((75 * difflib_score)/100)
		percentage = round(float(spacy_percentage + wordnet_percentage + difflib_percentage),2)
		
		return {"Sequence Score" : difflib_score, "Synonym Score" : wordnet_score, "Context score" : spacy_score, "Total Score" : percentage}
					
if __name__ == '__main__':
	WordSimilarity()
