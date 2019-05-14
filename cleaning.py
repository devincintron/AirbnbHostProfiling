import csv
from langdetect import detect
from collections import defaultdict
output_path = "./SampleCleaned/"
# Given rowreader and end_row index, builds up and returns
# defaultdict(list) in which keys are listing_ids and
# values are lists of comments corresponding to the
# listing_id
# TODO: prevent none-default language breaks, throw exceptions for bad characters, etc.
def buildListingsAndComments(rowreader, end_row):
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
			listings_and_comments[curr_listing_id].append(comment)
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

def main():
	with open('chicago_sample.csv', encoding="utf8") as csvfile:
		rowreader = csv.reader(csvfile)
		curr_listing_id = None
		listings_and_comments = buildListingsAndComments(rowreader, 1120)
		for k,v in listings_and_comments.items():               # will become d.items() in py3k
			print ("%s - %d" % (str(k), len(v)))
		writeToFiles(listings_and_comments, 'sample_')

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
