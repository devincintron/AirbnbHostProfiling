import csv
from langdetect import detect, DetectorFactory, detect_langs
from collections import defaultdict

output_path = "./SampleCleanedEng/"
file_prefix = 'sample_'
my_language = 'en'
dropped_comments_file = 'dropped_commments'

# Lang detect is non-deterministic so this enforces consistent results across runs
DetectorFactory.seed = 0

# Threshold with which we keep comments -- if langdetect detects that
# the probabilitiy of a comment not matching my_language is less than
# language_threshold then we disregard that comment
language_threshold = 0.75
min_comment_char_length = 7 # less than this many characters is disregarded for comments


# Predicate to check if comment consists with specified language at specified likelihood
def matchesLanguage(comment):
	comment_lang_probs = detect_langs(comment)
	highest_likelihood_lang = comment_lang_probs[0]
	return highest_likelihood_lang.lang == my_language and highest_likelihood_lang.prob >= language_threshold

# Given rowreader and end_row index, builds up and returns
# defaultdict(list) in which keys are listing_ids and
# values are lists of comments corresponding to the
# listing_id
# TODO: prevent none-default language breaks, throw exceptions for bad characters, etc.
def buildListingsAndComments(rowreader, end_row, dropped_comments):
	listings_and_comments = defaultdict(list)
	i, curr_listing_id = 0, None
	for row in rowreader:
		if i == 0: # for first row of headings
			i += 1
		elif i > end_row: # finished
			break
		else:
			local_listing_id, comment = row[0], row[1]
			if curr_listing_id is None:
				curr_listing_id = local_listing_id
			elif curr_listing_id != local_listing_id: # if it is a new Id
				curr_listing_id = local_listing_id

			if (len(comment) > min_comment_char_length and matchesLanguage(comment)): # Only include if it matches the language
				listings_and_comments[curr_listing_id].append(comment)				  # and is of reasonable length
			else:
				dropped_comments.append(comment)
				print(comment)
				# Var is not reassigned so reference just changes i.e. lists are mutable
			i += 1
	return listings_and_comments

# Given defaultdict of listing_ids and their corresponding
# comments and a filenaming prefix, writes the ids to .txt files
# of the format:
# filename = prefix + listing_id
# file content = 
# 		comment1
#		
#		comment2
#		
#		  ...
# 
# The files are written to the folder specified by output path

def writeToFiles(defdict, prefix):
	for listing_id in defdict.keys():
		filename = output_path + prefix + listing_id
		file = open(filename, 'w', encoding='utf-8')
		file.writelines(defdict[listing_id])
		file.close()


# Writes all of the comments which were dropped for length and/or language issues 
# to a file for review
def logDroppedComments(dropped_comments):
	filename = output_path + dropped_comments_file
	dropped_file = open(filename, 'w', encoding='utf-8')
	dropped_file.writelines(dropped_comments)
	dropped_file.close()

def main():
	dropped_comments = []
	with open('chicago_sample.csv', encoding="utf8") as csvfile:
		rowreader = csv.reader(csvfile)
		curr_listing_id = None
		listings_and_comments = buildListingsAndComments(rowreader, 1120, dropped_comments)
		for k,v in listings_and_comments.items():               # will become d.items() in py3k
			print ("%s - %d" % (str(k), len(v)))
		writeToFiles(listings_and_comments, file_prefix)
		logDroppedComments(dropped_comments)

if __name__ == '__main__':
		main()




# take csvs and convert into format:
# title of file: id
# file text: 
# entry
# new line
# next entry
# etc. 

# place all of the files into a directory

# remove these: The reservation was canceled 80 days before arrival. This is an automated posting.
