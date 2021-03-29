#!/usr/bin/env python3

# Import google cloud natural language API.
from google.cloud import language


def classify_text(text):
  client = language.LanguageServiceClient()
  document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

  response = client.classify_text(document=document)

  for category in response.categories:
    print("=" * 80)
    print(f"category  : {category.name}")
    print(f"confidence: {category.confidence:.0%}")
    
if __name__ == "__main__":
  classify_text(text)