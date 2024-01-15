import json
import time
from ChatGPT import ChatGPT
from Create_article import Create_Article_Docx
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import ast

from docx import Document
from docx.shared import Pt, Inches
from docx.oxml.ns import qn
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx2pdf import convert
import json
from ChatGPT import ChatGPT
import os


question_num = 10  # Set the number of questions
article_length = 4500  # Article length
reader_question_num = 3  # Number of questions from the reader

def GenerateQuestion(hot_topics):
    # Generate questions based on hot topics
    prompt = f"""You are a writer who works for a media company.
            Your task is to publish general health-related articles. 
            The recent hot topics in health-related fields are as follows:
            {hot_topics}
            Please automatically generate {question_num} questions that readers aged 30-60 are interested in on these topics, based on recent trends and your task.
            Here are some examples:```How to prevent cardiovascular disease in middle-aged people? How to maintain bone health for people over 40?```
            Provide them in JSON format with the following keys: Question, Category
            Make sure do not add additinal word outside the JSON format."""
    return ChatGPT(prompt, 3600)

def GenerateArticle(question_txt):
    # Generate an article based on topics and questions
    prompt = f"""You are a writer who works for a media company.
            Your task is to generate an article based on hot topics and answers.
            Write a health-related article with a word count of approximately {article_length} words based on the topics and questions.
            Make sure the article has a minimum of {article_length} words and consists of more than 7 paragraphs.
            The questions:```{question_txt}```
            Provide the article in JSON format with the following key: Article"""
    return ChatGPT(prompt, 3600)

def AskQuestion(article):
    # Ask questions as a reader
    prompt = f"""You are a reader aged between 30 and 60 who is interested in health-related topics.
                 Your task is to ask {reader_question_num} questions after reading the text.
                 ```{article}```
                 Provide the questions in JSON format with the following keys: Question, Category
                 Make sure do not add additinal word outside the JSON format."""
    return ChatGPT(prompt, 1000)

def GenerateArticle1(article, question_txt):
    # Generate a new article based on an old article and questions
    prompt = f"""You are a writer who works for a media company.
                You have written an old article.
                Modify the old article, which has a word count of approximately {article_length} words, based on the questions.
                Make sure the new article has a minimum of {article_length} words and consists of more than 7 paragraphs.
                The questions: '''{question_txt}'''
                The old article:'''{article}'''
                Provide the new article in JSON format with the following key: Article"""
    return ChatGPT(prompt, 2600)

# Used for articles with around 22 paragraphs (including subheadings)
def GenerateLongerParagraph(paragraph): #expand one paragragh
    # Enrich the paragraph to ensure it has a word count of approximately article_length words based on an old paragraph
    prompt = f"""
                Enrich the paragraph to ensure it has a word count of approximately {article_length} words based on the old paragraph.
                The old paragraph:'''{paragraph}'''
                Provide the paragraph in JSON format with the following key: Paragraph"""
    return ChatGPT(prompt, 2800)

# Used for articles with around 12 paragraphs (including subheadings)
def GenerateLongerParagraph2(paragraph):  #one paragragh to several(3) paragraghs
    # Write an article to ensure it has a word count of approximately article_length words based on an old paragraph
    prompt = f"""
                Write an article to ensure it has a word count of approximately {article_length} words based on the old paragraph.
                The old paragraph:'''{paragraph}'''
                Provide the article in JSON format with the following key: Paragraph"""
    return ChatGPT(prompt, 2800)

def AnalyzeTypeOfPerson(article):
    # Identify the type of person and relevant hashtags the article should be exposed to
    prompt = f"""
                Identify the type of person (e.g., male, retired, with children) this article should be exposed to and the relevant hashtags.
                Format your answer as a list of no more than 5 lowercase words or phrases separated by commas.
                Article:```{article}```
                
            """
    return ChatGPT(prompt, 1000)


if __name__ == '__main__': 
    # Create Chrome WebDriver instance
    service = Service(executable_path='D:\Berry\py\chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    # Define the URL to access Google Trends
    url = "https://trends.google.com/trends/trendingsearches/realtime?geo=US&hl=en-AU&category=m"

    # Open the webpage
    driver.get(url)

    # Wait for the page to load
    sleep(5)

    # Find all div tags that match the given criteria
    div_tags = driver.find_elements(By.CSS_SELECTOR, 'div.title')

    # Create a dictionary to store the results
    result_dict = {}

    # Iterate over the div tags
    for i, div in enumerate(div_tags):
        # Find all span tags within the div tag
        span_tags = div.find_elements(By.CSS_SELECTOR, 'span')

        # Extract the text content from the span tags and join them with commas
        content_list = [span.text.replace('•', '') for span in span_tags]
        content_str = ', '.join(filter(None, content_list))

        # Create the key for the dictionary
        key = f"hot_topic{i+1}"

        # Store the result in the dictionary
        result_dict[key] = content_str

    # Output the result dictionary
    for key, value in result_dict.items():
        print(f"{key}: {value}")

    # Close the browser
    driver.quit()


    # Automatically generate multiple questions of interest to daily readers (aged 30-60) based on recent search trends, optimized for search engines.
    # Use a for loop to generate an article for each hot topic. Here, we take the top-ranked hot topic as an example.
    # Get the first hot topic from the result dictionary
    first_topic = next(iter(result_dict.values()))

    # Generate questions based on the first hot topic
    response = GenerateQuestion(first_topic)
    print(response)

    # Convert the response to a list of dictionaries
    data_list = ast.literal_eval(response)

    # Extract the questions from the data and store them in a list
    question_list = []
    for data in data_list:
        question_list.append(data["Question"])
    
    # Generate articles based on hot issues
    # Initialize variables
    question_txt = ""  # String to store the formatted questions
    index = 0

    # Loop through the list of questions and format them
    for question in question_list:
        question_txt += str(index) + "." + question_list[index] + "\n"
        index += 1

    # Generate an article based on the questions
    response = GenerateArticle(question_txt)
    data = json.loads(response, strict=False)
    article = data["Article"]

    # Output the generated article
    print(article)
    # time.sleep(20)

    # Ask questions as a reader based on the article content
    response = AskQuestion(article)
    print(response)

    # Parse the response as JSON
    data_list = json.loads(response)

    # Extract the reader questions from the data and store them in a list
    reader_question_list = []
    for data in data_list:
        reader_question_list.append(data["Question"])

    # Format the reader questions
    new_question_txt = ""
    index = 0
    for reader_question in reader_question_list:
        new_question_txt += str(index) + "." + reader_question[index] + "\n"
        index += 1

    # Wait for some time before generating the modified article
    time.sleep(20)

    # Generate an updated article based on the reader's questions
    response = GenerateArticle1(article, new_question_txt)

    # Parse the response as JSON
    article = json.loads(response, strict=False)
    article = article["Article"]

    # Output the modified article
    print(article)

    #Due to the limitation of the longest token of the model, it needs to be expanded segment by segment.
    # Use the initial article to generate the title
    short_article = article

    # Split the article into paragraphs
    article_list = article.split('\n')

    # Initialize variables
    long_article = ""  # String to store the extended article

    # Iterate through each paragraph
    for single_article in article_list:
        if single_article == "":
            continue

        # Wait for some time before generating the longer paragraph
        time.sleep(20)  # Because the ChatGPT API has usage limits

        # Print the current paragraph
        print(single_article)

        # Generate a longer paragraph based on the current paragraph
        response = GenerateLongerParagraph2(single_article)
        print(response)

        # Parse the response as JSON
        data1 = json.loads(response, strict=False)

        # Extract the new paragraph from the data
        new_paragraph = data1["Paragraph"]

        # Append the new paragraph to the extended article
        long_article += new_paragraph + "\n"


    
    Create_Article_Docx(short_article=short_article,long_article=long_article)

    # Determine the target audience of the article
    response = AnalyzeTypeOfPerson(article=short_article)  # Analyze the type of person the article is targeting

    people_type_list = response.split(' |,')  # Split the response into a list of people types
    people_type_txt = ""  # Initialize an empty string to store the people types

    for people_type in people_type_list:
        if people_type == "":
            continue  # Skip empty people types
        people_type_txt += people_type + " "  # Add the people type to the string

    print(people_type_txt)  # Print the resulting people types
    






