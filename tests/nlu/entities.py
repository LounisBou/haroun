#!/usr/bin/env python3

# Import google cloud natural language API.
from google.cloud import language

def analyze_text_entities(text):
  client = language.LanguageServiceClient()
  document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

  response = client.analyze_entities(document=document)

  for entity in response.entities:
    print("=" * 80)
    results = dict(
      name=entity.name,
      type=entity.type_.name,
      salience=f"{entity.salience:.1%}",
      wikipedia_url=entity.metadata.get("wikipedia_url", "-"),
      mid=entity.metadata.get("mid", "-"),
    )
    for k, v in results.items():
      print(f"{k:15}: {v}")
      
if __name__ == "__main__":
  analyze_text_entities(text)