#!/usr/bin/env python3

# Import sys library for args.
import sys

# Import google cloud natural language API.
from google.cloud import language

# entities.
def entities(text):
  client = language.LanguageServiceClient()
  document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

  response = client.analyze_entities(document=document)

  for entity in response.entities:
    print("=" * 80)
    results = dict(
      name=entity.name,
      type=entity.type_.name,
      pertinence=f"{entity.salience:.1%}",
      wiki=entity.metadata.get("wikipedia_url", "-"),
      mid=entity.metadata.get("mid", "-"),
    )
    for k, v in results.items():
      print(f"{k:15}: {v}")
      
# classify    
def classify(text):
  client = language.LanguageServiceClient()
  document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

  response = client.classify_text(document=document)
    
  for category in response.categories:
    print("=" * 80)
    print(f"category  : {category.name}")
    print(f"confidence: {category.confidence:.0%}")
      
# sentiment   
def sentiment(text):
  client = language.LanguageServiceClient()
  document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

  response = client.analyze_sentiment(document=document)

  sentiment = response.document_sentiment
  results = dict(
    sentiment=f"{sentiment.score:.1%}",
    force=f"{sentiment.magnitude:.1%}",
  )
  print("=" * 80)
  for k, v in results.items():
    print(f"{k:10}: {v}")
       
# syntax
def syntax(text):
  
  client = language.LanguageServiceClient()
  document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

  response = client.analyze_syntax(document=document)

  fmts = "{:10}: {}"
  print("=" * 80)
  print(fmts.format("phrase(s)", len(response.sentences)))
  print(fmts.format("mot(s)", len(response.tokens)))
  print("=" * 80)
  for token in response.tokens:
    print(fmts.format(token.part_of_speech.tag.name, token.text.content))
    
# main
if __name__ == "__main__":
  
  # Retrieve argument 1 as text to transform
  text = sys.argv[1]
  
  # Text.
  print(text)
  
  # Entities
  entities(text)
  # Sentiment
  sentiment(text)
  try:
    # Classify
    classify(text)
  except Exception as e:
    #print("=" * 80)
    #print('No classification... '+str(e))
    pass
  # Syntax
  syntax(text)
  