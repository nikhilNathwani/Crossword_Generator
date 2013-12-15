import sys
import requests
import unicodedata
import random
import string
from bs4 import BeautifulSoup

def getPossibleWords(query_string):
  query = {'answer': query_string, 'clue': ''}
  r= requests.get('http://crosswordtracker.com/search/', params=query)
  query_soup= BeautifulSoup(r.text) 
  print r.text
  if not "crossword puzzle answer" in query_soup.title.string:
      words= [str(elem.string) for elem in query_soup.find_all('a', {"class" : "answer highlighted"})]
  else: 
      words= [str(query_soup.title.string.split()[0])]
  print words
  return words


def getClue(word):
  query = {'answer': word, 'clue': ''}
  r= requests.get('http://crosswordtracker.com/search/', params=query)
  clue_soup= BeautifulSoup(r.text)
  clue_list= clue_soup.find('ul', {"class" : "sortable", "id" :"answer-clues-ul"})
  print clue_list
  clue_list= [unicodedata.normalize('NFKD', elem.string).encode('ascii','ignore') for elem in clue_list.find_all('a')]
  a= random.randint(0,len(clue_list)-1)
  print "\n\n\n", word, "\n",clue_list
  return clue_list[a]

def main():
  query_string = raw_input('Enter word pattern, with \'?\' for unknown characters (e.g. r??e?): ')
  query = {'answer': query_string, 'clue': ''}
  r= requests.get('http://crosswordtracker.com/search/', params=query)
  query_soup= BeautifulSoup(r.text)

  #If only 1 word satisfies the query the site goes straight to the clues,
  #with title containing "crossword puzzle answer". Only need to do this when
  #there's multiple words to choose from
  if not "crossword puzzle answer" in query_soup.title.string:
      #print query_soup.prettify()
      #print soup.a
      words= [str(elem.string) for elem in query_soup.find_all('a', {"class" : "answer highlighted"})]
      print words
  
      clue = raw_input('Which would you like to see a clue for?: ')
      url= "http://crosswordtracker.com/answer/" + clue.lower()

      r= requests.get(url)
      
  clue_soup= BeautifulSoup(r.text)
  clue_list= clue_soup.find('ul', {"class" : "sortable", "id" :"answer-clues-ul"})
  clue_list= [unicodedata.normalize('NFKD', elem.string).encode('ascii','ignore') for elem in clue_list.find_all('a')]
  a= random.randint(0,len(clue_list)-1)
  #print clue_list
  print clue_list[a]

if __name__ == '__main__':
    getPossibleWords("?a?")