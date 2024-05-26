from openai import OpenAI
import pandas as pd
import re
from neo4j import GraphDatabase
from src.neo4j_connector import neo4j_connector

API_KEY = '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'
# openai.api_key = API_KEY
client = OpenAI(api_key=API_KEY)

# ft:gpt-3.5-turbo-1106:personal::94KbmS0e
# gpt-3.5-turbo
def get_completion(prompt, model="gpt-4-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
    model=model,
    messages = messages,
    temperature=0
    )
    return response.choices[0].message.content

def normalize_entity(entity):
    return [element.strip().lower() for element in entity]

def get_entity_from_nl(nl):
    prompt = f"""
    As a smart AI assistant specialized in natural language
    processing and knowledge graph analysis, I am given the following question: '{nl}'.\
    Perform Mention Detection on this question to identify the geographic entities.\
    your answer should be in this format without any words.\
    Entity: answer, answer (if more than one).
    """
    
    
    f"""
    Passage: As a smart AI assistant specialized in natural language processing and knowledge graph analysis, I am given the following question: '{nl}'. 
    Here are some example question-entity pairs:
    - "세화여자중학교에 배정받을 수 있는 아파트 알려줘" identifies "세화여자중학교"
    - "동고아파트의 평균 관리비는?" identifies "동고아파트"
    - "서초포레스타7단지아파트의 가구당 주차대수는 몇 대야?" identifies "서초포레스타7단지아파트"
    - "서초래미안아파트의 인구는 몇명이야?" identifies "서초래미안아파트"
    - "서초네이처힐1단지아파트에는 지하주차장이 있어?" identifies "서초네이처힐1단지아파트"
    - "한강 음식점 근처 카페가 어디있어?" identifies "한강"
    - "서울에 있는 논현동을 지나치는 지하철 노선은 뭐야?" identifies "서울, 논현동"
    - "인천에 있는 가좌동에서 시세가 가장 저렴한 아파트 알려줘" identifies "인천, 가좌동"
    - "두만강은 북한의 어디에 위치에 있어?" identifies "두만강, 북한"
    Perform Mention Detection on this question to identify the geographic entities.
    Question: From this passage, can one identify the geographic entities mentioned in the question?
    Answer must be in this format
    Answer: [Entity: answer, answer (if more than one)]
    """


    response = get_completion(prompt)
    answer = re.split(',|:', response)
    return normalize_entity(answer[1:])


def entity_disambiguation_bootalk(nl, entity, json):
    prompt = f"""
    As a smart AI assistant specialized in natural language\
    processing and knowledge graph analysis, I am given the following question: '{nl}'.\
    The recognized entity in this question is {entity}\
    By doing entity disambiguation with the question given :'{nl}'\
    Find the coressponding information in this json: {json}.\
    Answer must be from the json not from your own knowledge and should be in Korean.  
    Answer format must be like this:\
    Name:\
    Identity: \
    Description: \
    Addr: \
    If json is empty or you can't find the right one, Answer is None.

    """
    response = get_completion(prompt)
    return response


def main(text):   
    results = []
    entities = get_entity_from_nl(text)
    for entity in entities:
        bootalk_json = neo4j_connector.get_apartment_by_name(entity)
        # print(bootalk_json)
        disambiguated_itemID = entity_disambiguation_bootalk(text, str(entity), bootalk_json)
        results.append({
            "Question": text,
            "Entity": str(entity),
            "Disambiguated ID": disambiguated_itemID
        })
    

    return results

if __name__ == "__main__":
    main()


