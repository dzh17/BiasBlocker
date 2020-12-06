import re
import nltk
import json

from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from SortedSet.sorted_set import SortedSet
from collections import Counter
import moment
from datetime import datetime

import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')


def exclude(excluded_words, words):
    return list(filter(lambda word: word not in excluded_words, words))


def get_base(verb):
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(verb, 'v')


def get_class(types, words):
    filtered_words = filter(lambda word: word[1] in types, words)
    mapped_words = map(lambda word_tuple: word_tuple[0], filtered_words)
    return list(mapped_words)


def get_weight(label):
    weights = {
        'DATE': 10,
        'PERSON': 9,
        'ORGANIZATION': 8,
        'FORP': 7,
        'GPE': 7,
        'GSP': 7,
        'FACILITY': 5,
        'NOUN': 2,
        'VERB': 1
    }

    return weights[label] if label in weights else 0.5


def retrieve_base_verbs(sentence_text, title):
    tokenized_words = nltk.word_tokenize(sentence_text)
    tagged_words = pos_tag(tokenized_words)
    verbs = get_class(["VB", "VBD", "VBG", "VBN", "VBZ"], tagged_words)
    verbs_base = list(exclude(['have', 'be', 'say', 'tell', 'become', 'get'], list(
        map(lambda verb: get_base(verb), verbs))))

    verbs = []
    for verb in verbs_base:
        if(len(verb) > 2):
            normalized_item = {}
            normalized_item['label'] = 'VERB'
            normalized_item['value'] = verb
            normalized_item['label_weight'] = get_weight(
                normalized_item['label'])
            normalized_item['occurencies'] = verbs_base.count(verb)
            normalized_item['words_count'] = len(verbs_base)
            normalized_item['weight'] = normalized_item['label_weight'] * \
                normalized_item['occurencies'] / normalized_item['words_count']
            normalized_item['synonyms'] = get_synonyms(
                normalized_item['value'])
            if normalized_item['value'] in title:
                normalized_item['weight'] = normalized_item['weight'] * 3
                normalized_item['enhanced'] = True
            verbs.append(normalized_item)
    sorted_x = list(sorted(verbs, key=lambda kv: kv['weight'], reverse=True))
    unique = list({v['value']: v for v in sorted_x}.values())
    return unique


def retrieve_generic_nouns(sentence_text, title):
    tokenized_words = nltk.word_tokenize(sentence_text)
    tagged_words = pos_tag(tokenized_words)
    generic_nouns = list(get_class(['NN'], tagged_words))
    nouns = []

    for noun in generic_nouns:
        normalized_item = {}
        normalized_item['label'] = 'NOUN'
        normalized_item['value'] = noun
        normalized_item['label_weight'] = get_weight(normalized_item['label'])
        normalized_item['occurencies'] = generic_nouns.count(noun)
        normalized_item['words_count'] = len(generic_nouns)
        normalized_item['weight'] = normalized_item['label_weight'] * \
            normalized_item['occurencies'] / normalized_item['words_count']
        normalized_item['synonyms'] = get_synonyms(normalized_item['value'])
        if normalized_item['value'] in title:
            normalized_item['weight'] = normalized_item['weight'] * 3
            normalized_item['enhanced'] = True
        nouns.append(normalized_item)
    sorted_x = list(sorted(nouns, key=lambda kv: kv['weight'], reverse=True))
    unique = list({v['value']: v for v in sorted_x}.values())
    return unique


def retrieve_proper_nouns(sentence_text, title):
    tokenized_words = nltk.word_tokenize(sentence_text)
    tagged_words = pos_tag(tokenized_words)
    ner = nltk.ne_chunk(tagged_words, binary=False)
    lemmatizer = WordNetLemmatizer()
    excluded_nouns = ['Twitter', 'Facebook', 'Covid']
    ner_found = []
    for item in ner:
        if hasattr(item, 'label'):
            value = ' '.join(i[0] for i in item.leaves())
            ner_found.append({'label': item.label(), 'value': value})

    nouns = []
    for item in ner_found:
        normalized_item = item.copy()
        normalized_item['value'] = lemmatizer.lemmatize(item['value'], 'n')
        normalized_item['label_weight'] = get_weight(normalized_item['label'])
        normalized_item['occurencies'] = ner_found.count(item)
        normalized_item['words_count'] = len(ner_found)
        normalized_item['weight'] = normalized_item['label_weight'] * \
            normalized_item['occurencies'] / normalized_item['words_count']
        normalized_item['synonyms'] = []
        if normalized_item['value'] not in excluded_nouns:
            if normalized_item['value'] in title:
                normalized_item['weight'] = normalized_item['weight'] * 3
                normalized_item['enhanced'] = True
            nouns.append(normalized_item)

    sorted_x = list(sorted(nouns, key=lambda kv: kv['weight'], reverse=True))
    unique = list({v['value']: v for v in sorted_x}.values())
    return unique


def retrieve_dates(text):
    monthRegexOne = r'((January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,4})'
    monthRegexTwo = r'(\d{1,4}\s(January|February|March|April|May|June|July|August|September|October|November|December))'
    matchesOne = re.findall(monthRegexOne, text)
    matchesTwo = re.findall(monthRegexTwo, text)
    dates = []

    for match in matchesOne:
        if len(match) > 0:
            normalized_item = {}
            normalized_item['label'] = 'DATE'
            normalized_item['value'] = match[0]
            normalized_item['label_weight'] = get_weight(
                normalized_item['label'])
            normalized_item['occurencies'] = text.count(match[0])
            normalized_item['words_count'] = len(matchesOne) + len(matchesTwo)
            normalized_item['weight'] = normalized_item['label_weight'] * \
                normalized_item['occurencies'] / normalized_item['words_count']
            normalized_item['enhanced'] = True
            normalized_item['synonyms'] = []
            dates.append(normalized_item)

    for match in matchesTwo:
        if len(match) > 0:
            normalized_item = {}
            normalized_item['label'] = 'DATE'
            normalized_item['value'] = match[0]
            normalized_item['label_weight'] = get_weight(
                normalized_item['label'])
            normalized_item['occurencies'] = text.count(match[0])
            normalized_item['words_count'] = len(matchesOne) + len(matchesTwo)
            normalized_item['weight'] = normalized_item['label_weight'] * \
                normalized_item['occurencies'] / normalized_item['words_count']
            normalized_item['enhanced'] = True
            normalized_item['synonyms'] = []
            dates.append(normalized_item)

    sorted_x = list(sorted(dates, key=lambda kv: kv['weight'], reverse=True))
    unique = list({v['value']: v for v in sorted_x}.values())
    return unique


def rename_geo_data(sentence_text):
    names = {
        'Stepanakert': 'Khankendi',
        'Shusha': 'Shushi',
        'Mardakert': 'Aghdara',
        'Karvachar': 'Kalbajar',
        'Martuni': 'Khodjavend',
        'Berdzor': 'Lachin',
        'Artsakh': 'NagornoKarabakh'
    }

    for name in names:
        value = names[name]
        sentence_text = sentence_text.replace(name, name + ',' + value + '. ')

    for name in names:
        if name not in sentence_text:
            value = names[name]
            sentence_text = sentence_text.replace(
                value, value + ',' + name + '. ')

    return sentence_text


def format_text(text):
    formatted_text = re.sub(r'-Karabakh', 'karabakh', text)
    formatted_text = rename_geo_data(text)
    formatted_text = formatted_text.replace('“', '')
    formatted_text = formatted_text.replace('”', '')
    return formatted_text


def get_all_keywords(sentence_text, title):
    dates = retrieve_dates(sentence_text)
    proper_nouns = retrieve_proper_nouns(sentence_text, title)
    generic_nouns = retrieve_generic_nouns(sentence_text, title)
    base_verbs = retrieve_base_verbs(sentence_text, title)

    all_keywords = []
    all_keywords.extend(dates)
    all_keywords.extend(proper_nouns)
    all_keywords.extend(generic_nouns)
    all_keywords.extend(base_verbs)
    sorted_x = sorted(all_keywords, key=lambda kv: kv['weight'], reverse=True)
    return sorted_x


def get_synonyms(word):
    synonyms = set({})
    for words in wordnet.synsets(word):
        for lemma in words.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)


def is_similar(word1, word2):
    synonyms = set({})
    for words in wordnet.synsets(word1):
        for lemma in words.lemmas():
            synonyms.add(lemma.name())
    return word2 in synonyms


def compare_articles(keywords_1, article):
    keywords_2 = get_all_keywords(article['content'], article['title'])
    comparisons = []

    total_score = 0
    for keyword_1 in keywords_1:
        host_label = keyword_1['label']
        keyword_1_value = keyword_1['value']
        keyword_1_weight = keyword_1['weight']

        comparison = {}
        comparison['keyword_1_value'] = keyword_1_value
        comparison['keyword_1_weight'] = keyword_1_weight

        for keyword_2 in keywords_2:
            keyword_2_label = keyword_2['label']
            keyword_2_value = keyword_2['value']
            keyword_2_weight = keyword_2['weight']
            keyword_2_synonyms =  keyword_2['synonyms']

            comparison['keyword_2_value'] = keyword_2_value
            comparison['keyword_2_weight'] = keyword_2_weight

            local_comparison_score = 0
            if host_label in ['NOUN', 'VERB', 'DATE']:
                if keyword_2_label in ['NOUN', 'VERB', 'DATE']:
                    if keyword_1_value in keyword_2_synonyms:
                        local_comparison_score = keyword_1_weight * keyword_2_weight
                    else:
                        local_comparison_score = 0
                else:
                    local_comparison_score = 0
            else:
                if keyword_2_label not in ['NOUN', 'VERB', 'DATE']:
                    if keyword_1_value.lower() in keyword_2_value.lower() or keyword_2_value.lower() in keyword_1_value.lower():
                        local_comparison_score = keyword_1_weight * keyword_2_weight
                    else:
                        local_comparison_score = 0

            comparison['score'] = local_comparison_score
            comparisons.append(comparison)
            total_score += local_comparison_score

    return total_score


def get_articles(country, article_text, article_title, article_date):
    scores = []
    with open(f'{country}_weight.json', encoding="utf8") as json_file:
        articles = json.load(json_file)
        sentence_text = article_text
        sentence_text = re.sub(r'-Karabakh', 'karabakh', sentence_text)
        sentence_text = re.sub(r'Armenian', 'Armenia', sentence_text)
        sentence_text = re.sub(r'Azerbaijani', 'Azerbaijan', sentence_text)

        keywords_1 = get_all_keywords(sentence_text, article_title)
        start_date = str(moment.date(article_date).add(hours=-36))
        end_date = str(moment.date(article_date).add(hours=36))
        for article in articles:
            p_date = str(moment.date(article['pubDate'][0:19]))
            print('Pub date: ', p_date)
            if start_date < p_date < end_date:
                print(start_date, p_date, end_date)
                score = compare_articles(keywords_1, article)
                score_obj = {}
                score_obj['url'] = article['link']
                score_obj['title'] = article['title']
                score_obj['score'] = score
                score_obj['article'] = article
                scores.append(score_obj)

    sorted_scores = sorted(scores, key=lambda kv: kv['score'], reverse=True)

    return sorted_scores[0:10]


def parse_article(article_text, article_title):
    article_text_temp = article_text
    article_text_temp = re.sub(r'-Karabakh', 'karabakh', article_text_temp)
    article_text_temp = re.sub(r'Armenian', 'Armenia', article_text_temp)
    article_text_temp = re.sub(r'Azerbaijani', 'Azerbaijan', article_text_temp)
    article_text_temp = format_text(article_text_temp)
    article_dict = {
        'title': article_title,
        'content': article_text,
        'keywords': get_all_keywords(article_text_temp, article_title)
    }

    return article_dict


def update_weights(country):
    with open(f'{country}_summary.json', encoding="utf8") as json_file:
        articles = json.load(json_file)
        articles_with_keywords = []
        for article in articles:
            article_with_keywords = article.copy()
            sentence_text = format_text(article_with_keywords['content'])
            title = format_text(article_with_keywords['title'])
            keywords = get_all_keywords(sentence_text, title)
            article_with_keywords['keywords'] = keywords
            articles_with_keywords.append(article_with_keywords)
            article_with_keywords['pubDate'] = format_date(article)
            progress = str(articles.index(article)) + '/' + str(len(articles))
            message = article_with_keywords['pubDate'] + ' Wrote : ' + progress + ' : ' + \
                article['title'] + str(len(keywords)) + '\n' 
            yield str(message)
        with open(f'{country}_weight.json', 'w', encoding='utf-8') as f:
            json.dump(articles_with_keywords, f, ensure_ascii=False, indent=4)

def format_date(article): 
    formatted_date = str(moment.date(article['pubDate'])) 
    if 'arka.am' in article['link']:
        formatted_date = str(moment.date(article['pubDate'], ' HH:mm DD.MM.YYYY').format('YYYY-DD-MMTHH:mm:ss%z'))
    
    return formatted_date

# article_text = """Russia has moved to stop the worst escalation of fighting in the separatist region of Nagorno-Karabakh in more than a quarter of a century by hosting ceasefire talks on Friday. Vladimir Putin called on Armenian and Azerbaijani forces to suspend the fighting that has raged in the disputed south Caucasus region for almost two weeks. The Kremlin said Putin’s initiative followed a series of calls with the Armenian prime minister, Nikol Pashinyan, and the Azerbaijani president, Ilham Aliyev. The latest clashes between the two sides began on 27 September and marked an escalation of the decades-old conflict over Nagorno-Karabakh. The region lies in Azerbaijan but has been under the control of ethnic Armenian forces backed by Armenia since the end of a separatist war in 1994. The Kremlin said Putin proposed calling a ceasefire to exchange prisoners and collect the bodies of dead soldiers. On Friday afternoon Russia’s foreign minister, Sergei Lavrov, greeted his Armenian and Azerbaijani counterparts in Moscow. Armenia said it was open to a ceasefire, while Azerbaijan has made a potential truce conditional on the Armenian forces’ withdrawal from Nagorno-Karabakh, arguing that the failure of international efforts to negotiate a settlement left it with no other choice but to try to reclaim its lands by force. In a TV address to his nation, Aliyev said nearly three decades of international talks “haven’t yielded an inch of progress. We haven’t been given back an inch of the occupied lands.” He said: “Mediators and leaders of some international organisations have stated that there is no military solution to the conflict. I have disagreed with the thesis, and I have been right. The conflict is now being settled by military means and political means will come next.” Q&A Why are Armenia and Azerbaijan fighting over the Nagorno-Karabakh region? Show Azerbaijani officials and Nagorno-Karabakh separatist authorities said heavy shelling continued. Fighting with heavy artillery, warplanes and drones has engulfed Nagorno-Karabakh despite numerous international calls for a truce. Both sides have accused each other of targeting residential areas and civilian infrastructure. On Friday a historic cathedral in the town of Shusha came under shelling for a third time, locals said. It was previously hit on Thursday, with one shell piercing its dome and damaging the interior. Further shelling wounded two Russian journalists inspecting the damage. The Azerbaijani military denied targeting the cathedral. The Nagorno-Karabakh military says 350 of its people have been killed since 27 September. Azerbaijan has not provided details on its military losses. Scores of civilians on both sides have been killed. Nagorno-Karabakh conflict: both sides accused of using cluster bombs Read more Stepanakert, the capital of Nagorno-Karabakh, has been under intense shelling. Residents are staying in shelters, some of which are in the basements of apartment buildings. Armenian officials allege that Turkey is involved in the conflict and is sending Syrian mercenaries to fight on Azerbaijan’s side. Turkey has publicly backed Azerbaijan in the conflict but has denied sending fighters to the region. Turkey said on Friday that efforts by France, the US and Russia to end violence between Azeri and Armenian forces over Nagorno-Karabakh were bound to fail unless they ensured a withdrawal of Armenian forces from the enclave."""
# article_title = """Russia hosts talks proposing Nagorno-Karabakh ceasefire"""
# get_articles('am', article_text, article_title, '2020-10-07')
#update_weights('am')
