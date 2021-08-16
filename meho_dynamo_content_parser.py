


# import
import json
import codecs 
import subprocess


# content required fields, defined in https://docs.google.com/document/d/1XLEl4l2EHKD0FcQhVtPEg8PgIuTC71J6cahKTjh0YSU/edit?usp=sharing
content_id = "content_id"
parent_id = "parent_id"
content_type = "content_type"
title_english = "title_english"
subtitle_english = "title_english"
title_localized = "title_localized"
proficiency = "proficiency"
language = "language"
tag = "tag"
sourcer = "sourcer"
curator = "curator"
created_date = "created_date"
status = "status"

# global tag map [id:name]
tag_map = dict({})



def main():


  # parse each content
  all_contents = []

  parseArticle(all_contents)
  parseDialogue(all_contents)
  parseExpression(all_contents)
  parseTrendingPhrase(all_contents)
  parseVocabulary(all_contents)
  parseParagraph(all_contents)
  parseChapter(all_contents)

  # verify
  print("Total content:" + str(len(all_contents)))
  # print whole file 
  # content_to_dump = json.dumps(all_contents, indent = 4, ensure_ascii=False)
  # print(content_to_dump)

  # write to file
  with codecs.open('all_content.json', 'w', encoding='utf-8') as f_w:
    json.dump(all_contents, f_w, indent = 4, ensure_ascii=False)
      

  # clean ups
  f_w.close()



# Not used for now, due to 3 table join for tags
def prepareTagMap():
  with open('tag_dump.json', "w") as outfile:
    subprocess.call(['aws', 'dynamodb', 'scan', '--table-name', 'Tag-v64ixmlkqrey5mftr2fc6ql55a-mehoadmin', '--region', 'us-west-2', '--output', 'json'], stdout=outfile)
  print("Download Tag ready!")
  with codecs.open('./tag_dump.json','r', 'utf-8') as f_r:
    tags_dump = json.load(f_r)

  tags = tags_dump['Items']
  count = 0
  for tagRaw in tags:
    count = count + 1
    tag_id = tagRaw['id']['S']
    tag_name = tagRaw['content']['S']
    tag_map[tag_id] = tag_name

  f_r.close()
  print("Total tags:" + str(count))


def parseArticle(all_contents):
  with open('article_dump.json', "w") as outfile:
    subprocess.call(['aws', 'dynamodb', 'scan', '--table-name', 'Article-v64ixmlkqrey5mftr2fc6ql55a-mehoadmin', '--region', 'us-west-2', '--output', 'json'], stdout=outfile)
  print("Download Article ready!")
  with codecs.open('./article_dump.json','r', 'utf-8') as f_r:
    articles_dump = json.load(f_r)

  articles = articles_dump['Items']
  count = 0
  for articleRaw in articles:
    count = count + 1
    content = dict({})
    content[content_id] = articleRaw['id']['S']
    content[parent_id] = None
    content[content_type] = articleRaw['__typename']['S']
    content[title_english] = articleRaw['titleEn']['S']
    content[subtitle_english] = articleRaw['whyYouShouldReadThisArticle']['S']
    content[title_localized] = articleRaw['titleZh']['S']
    content[proficiency] = None
    content[tag] = None
    content[sourcer] = articleRaw['sourcer']['S']
    content[created_date] = articleRaw['updatedAt']['S']
    content[status] = articleRaw['status']['S']
    all_contents.append(content)

  f_r.close()
  print("Total articles:" + str(count))

def parseDialogue(all_contents):
  with open('dialogue_dump.json', "w") as outfile:
    subprocess.call(['aws', 'dynamodb', 'scan', '--table-name', 'Dialogue-v64ixmlkqrey5mftr2fc6ql55a-mehoadmin', '--region', 'us-west-2', '--output', 'json'], stdout=outfile)
  print("Download Dialogue ready!")

  with codecs.open('./dialogue_dump.json','r', 'utf-8') as f_r:
    dialogues_dump = json.load(f_r)

  dialogues = dialogues_dump['Items']

  count = 0
  for dialogueRaw in dialogues:
    count = count + 1
    content = dict({})
    content[content_id] = dialogueRaw['id']['S']
    content[parent_id] = None
    content[content_type] = dialogueRaw['__typename']['S']
    content[title_english] = dialogueRaw['titleEn']['S']
    content[subtitle_english] = dialogueRaw['whyYouShouldLearnThisDialogue']['S']
    content[title_localized] = dialogueRaw['titleZh']['S']
    content[proficiency] = dialogueRaw['difficultyLevel']['S']
    content[tag] = None
    content[sourcer] = None
    content[created_date] = dialogueRaw['updatedAt']['S']
    content[status] = dialogueRaw['status']['S']
    all_contents.append(content)

  f_r.close()
  print("Total dialogues:" + str(count))

def parseExpression(all_contents):
  with open('expression_dump.json', "w") as outfile:
    subprocess.call(['aws', 'dynamodb', 'scan', '--table-name', 'Expression-v64ixmlkqrey5mftr2fc6ql55a-mehoadmin', '--region', 'us-west-2', '--output', 'json'], stdout=outfile)
  print("Download Expression ready!")

  with codecs.open('./expression_dump.json','r', 'utf-8') as f_r:
    expressions_dump = json.load(f_r)
  

  expressions = expressions_dump['Items']
  count = 0
  for expressionRaw in expressions:
    count = count + 1
    content = dict({})
    content[content_id] = expressionRaw['id']['S']
    content[parent_id] = None
    content[content_type] = expressionRaw['__typename']['S']
    content[title_english] = expressionRaw['contentEn']['S']
    content[subtitle_english] = expressionRaw['label']['S']
    content[title_localized] = expressionRaw['contentZh']['S']
    content[proficiency] = None
    content[tag] = None
    content[sourcer] = None
    content[created_date] = expressionRaw['createdAt']['S']
    content[status] = None
    all_contents.append(content)

  f_r.close()
  print("Total expressions:" + str(count))


def parseTrendingPhrase(all_contents):
  with open('trending_phrase_dump.json', "w") as outfile:
    subprocess.call(['aws', 'dynamodb', 'scan', '--table-name', 'TrendingPhrase-v64ixmlkqrey5mftr2fc6ql55a-mehoadmin', '--region', 'us-west-2', '--output', 'json'], stdout=outfile)
  print("Download Trending Phrase ready!")

  with codecs.open('./trending_phrase_dump.json','r', 'utf-8') as f_r:
    trendings_dump = json.load(f_r)

  trendings = trendings_dump['Items']
  count = 0
  for trendingRaw in trendings:
    count = count + 1
    content = dict({})
    content[content_id] = trendingRaw['id']['S']
    content[parent_id] = None
    content[content_type] = trendingRaw['__typename']['S']
    content[title_english] = None
    content[subtitle_english] = trendingRaw['description']['S']
    content[title_localized] = trendingRaw['contentZh']['S']
    content[proficiency] = None
    content[tag] = None
    content[sourcer] = None
    content[created_date] = trendingRaw['createdAt']['S']
    content[status] = trendingRaw['status']['S']
    all_contents.append(content)

  f_r.close()
  print("Total trending phrases:" + str(count))

def parseVocabulary(all_contents):
  with open('vocabulary_dump.json', "w") as outfile:
    subprocess.call(['aws', 'dynamodb', 'scan', '--table-name', 'Vocabulary-v64ixmlkqrey5mftr2fc6ql55a-mehoadmin', '--region', 'us-west-2', '--output', 'json'], stdout=outfile)
  print("Download Vocabulary ready!")

  with codecs.open('./vocabulary_dump.json','r', 'utf-8') as f_r:
   vocabularies_dump = json.load(f_r)

  vocabularies = vocabularies_dump['Items']
  count = 0
  for vocabularyRaw in vocabularies:
    count = count + 1
    content = dict({})
    content[content_id] = vocabularyRaw['id']['S']
    content[parent_id] = None
    content[content_type] = vocabularyRaw['__typename']['S']
    content[title_english] = vocabularyRaw['contentEn']['S']
    content[subtitle_english] = vocabularyRaw['label']['S']
    content[title_localized] = vocabularyRaw['contentZh']['S']
    content[proficiency] = None
    content[tag] = None
    content[sourcer] = None
    content[created_date] = vocabularyRaw['createdAt']['S']
    content[status] = None
    all_contents.append(content)

  f_r.close()
  print("Total vocabularies:" + str(count))

def parseParagraph(all_contents):
  with open('paragraph_dump.json', "w") as outfile:
    subprocess.call(['aws', 'dynamodb', 'scan', '--table-name', 'Paragraph-v64ixmlkqrey5mftr2fc6ql55a-mehoadmin', '--region', 'us-west-2', '--output', 'json'], stdout=outfile)
  print("Download Paragraph ready!")

  with codecs.open('./paragraph_dump.json','r', 'utf-8') as f_r:
   paragraphs_dump = json.load(f_r)

  paragraphs = paragraphs_dump['Items']
  count = 0
  for paragraphRaw in paragraphs:
    count = count + 1
    content = dict({})
    content[content_id] = paragraphRaw['id']['S']
    content[parent_id] = paragraphRaw['paragraphArticleId']['S']
    content[content_type] = paragraphRaw['__typename']['S']
    content[title_english] = None
    content[subtitle_english] = None
    content[title_localized] = None
    content[proficiency] = None
    content[tag] = None
    content[sourcer] = None
    content[created_date] = paragraphRaw['createdAt']['S']
    content[status] = None

    if paragraphRaw['contentType']['S'] == 'EN':
      content[title_english] = paragraphRaw['content']['S']
    else:
      content[title_localized] = paragraphRaw['content']['S']
    all_contents.append(content)

  f_r.close()  
  print("Total article paragraphs:" + str(count))

def parseChapter(all_contents):
  with open('chapter_dump.json', "w") as outfile:
    subprocess.call(['aws', 'dynamodb', 'scan', '--table-name', 'Chapter-v64ixmlkqrey5mftr2fc6ql55a-mehoadmin', '--region', 'us-west-2', '--output', 'json'], stdout=outfile)
  print("Download Chapter ready!")

  with codecs.open('./chapter_dump.json','r', 'utf-8') as f_r:
   chapters_dump = json.load(f_r)

  chapters = chapters_dump['Items']
  count = 0
  for chapterRaw in chapters:
    count = count + 1
    content = dict({})
    content[content_id] = chapterRaw['id']['S']
    content[parent_id] = chapterRaw['chapterDialogueId']['S']
    content[content_type] = chapterRaw['__typename']['S']
    content[title_english] = chapterRaw['contentEn']['S']
    content[subtitle_english] = None
    content[title_localized] = chapterRaw['contentZh']['S']
    content[proficiency] = None
    content[tag] = None
    content[sourcer] = None
    content[created_date] = chapterRaw['createdAt']['S']
    content[status] = None

    all_contents.append(content)

  f_r.close() 
  print("Total dialog chapters:" + str(count)) 


if __name__ == "__main__":
    main()
