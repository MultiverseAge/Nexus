import datetime
import requests
import json
from googlesearch import search
from googletrans import Translator
import platform
import streamlit as st
from io import BytesIO
from gtts import gTTS, gTTSError
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet
from streamlit_option_menu import option_menu

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Function to speak the response
selected = option_menu(
            menu_title=None,
            options=["Nexus", "Help"],
            icons=["alexa","info circle"],
            orientation = "horizontal",
            styles={
                "container":{"border-radius":"0px",}
            }
        )

if selected == "Nexus":
 def speak_response(response):
     sound_file = BytesIO()
     try:
         tts = gTTS(text=response, lang="en", tld="us")
         tts.write_to_fp(sound_file)
         st.audio(sound_file)
     except gTTSError as err:
         st.error(err)
 
 
 page_bg_img = '''
 <style>
 [data-testid="stAppViewContainer"]{
 background-image: url("https://wallpaperaccess.com/full/99836.jpg");
 background-size: cover;
 }
 [data-testid="stHeader"] {
 background: rgba(0,0,0,0);
 }
 </style>
 '''
 st.markdown(page_bg_img, unsafe_allow_html=True)
 
 def get_weather():
     city = st.text_input("Which city's weather do you want?")
     if st.button("Get Weather"):
         url = f"https://api.weatherapi.com/v1/current.json?key=c4edb1b163464a9fab291441232707&q={city}"
         get = requests.get(url)
         dic = json.loads(get.text)
         weather = {
             "Temperature": dic["current"]["temp_c"],
             "Humidity": dic["current"]["humidity"],
             "Clouds": dic["current"]["cloud"]
         }
 
         weather_info = f"The weather of {city} is: Temperature - {weather['Temperature']}°C, Humidity - {weather['Humidity']}%, Clouds - {weather['Clouds']}%"
         st.write(weather_info)
         speak_response(weather_info)
 
 def web_search():
     query = st.text_input("Enter your query:")
     if st.button("Search"):
         search_results = search(query)
         for index, result in enumerate(search_results, 1):
             st.write(f"{index}. {result}")
             speak_response(result)
 
 def calculate():
     operation = st.text_input("Tell the operation:")
     one = st.number_input("Tell the first digit:", step=1, value=0, format="%d")
     two = st.number_input("Tell the second digit:", step=1, value=0, format="%d")
     if st.button("Calculate"):
         if operation == "+":
             result = f"{one} + {two}: {one + two}"
         elif operation == "-":
             result = f"{one} - {two}: {one - two}"
         elif operation == "*":
             result = f"{one} × {two}: {one * two}"
         elif operation == "/":
             if two != 0:  # Avoid division by zero
                 result = f"{one} / {two}: {one // two}"  # Use integer division
             else:
                 result = "Division by zero is not allowed."
         elif operation == "**":
             result = f"{one} ^ {two}: {one ** two}"
         else:
             result = "Invalid operation."
         st.write(result)
         speak_response(result)
 
 
 def get_word_meaning():
     word = st.text_input("Tell the word:")
     if st.button("Search Meaning"):
         meaning = None
 
         # Fetching word meaning from WordNet
         synsets = wordnet.synsets(word)
         if synsets:
             meaning = synsets[0].definition()
         if meaning:
             st.markdown(f"**Meaning:** {meaning}", unsafe_allow_html=True)
             speak_response(meaning)
         else:
             st.write("Sorry, the word meaning couldn't be found.")
 
 
 def get_latest_news():
     if st.button("Get Latest News"):
         nurl = "https://newsapi.org/v2/top-headlines?country=in&apiKey=ae364ee645b741b3aef7dae2e6ff59a5"
         nget = requests.get(nurl)
         nresponse = nget.json()
 
         if "articles" in nresponse and nresponse["articles"]:
             articles = nresponse["articles"][:5]
             for index, article in enumerate(articles, start=1):
                 news_title = article["title"]
                 st.write(f"{index}. {news_title}")
                 speak_response(news_title)
         else:
             st.write("No articles found in the API response.")
 
 def translate_sentence():
     translator = Translator()
     sentence = st.text_input("Tell me the sentence:")
     target_language = st.text_input("Tell me the language in which I have to translate the sentence:")
     if st.button("Translate"):
         translated_text = translator.translate(sentence, dest=target_language)
         st.write(f"Original: {sentence}")
         st.write(f"Translated ({target_language}): {translated_text.text}")
         speak_response(translated_text.text)
 
 def get_system_specifications():
     if st.button("Get System Specs"):
         architecture = platform.architecture()
         st.write("System Architecture:", architecture)
         os_name = platform.system()
         st.write("Operating System:", os_name)
         release = platform.release()
         st.write("Release Version:", release)
         processor = platform.processor()
         st.write("Processor:", processor)
         speak_response(f"System Architecture: {architecture}. Operating System: {os_name}. Release Version: {release}. Processor: {processor}.")
 
 def greet_user():
     st.title("Virtual Assistant")
     name = st.text_input("Hello, Can I know your name:")
     if name:
         now = datetime.datetime.now()
         hour = now.hour
         greet = ""
 
         if hour > 5 and hour < 12:
             greet = "Good Morning"
         elif hour >= 12 and hour <= 17:
             greet = "Good Afternoon"
         elif hour > 17 and hour <= 20:
             greet = "Good Evening"
         else:
             greet = "Good Night"
 
         greet = f"{greet} {name}"
         st.write(greet)
         speak_response(greet)
         main(name)
 
 def main(name):
     assist = st.selectbox("Choose an option:", [
         "What's the weather today?",
         "What's the time and date?",
         "I want to do a web search",
         "I want to calculate something.",
         "I want to know the meaning of a word",
         "What's the latest news?",
         "I want to translate a sentence.",
         "Tell me the system specifications of my computer.",
         "Who are you",
     ])
 
     if assist == "What's the weather today?":
         get_weather()
     elif assist == "What's the time and date?":
         now = datetime.datetime.now()
         date = now.date()
         time = now.time()
         st.write(f"Today's date is: {date}")
         st.write(f"Currently time is: {time.hour}:{time.minute}")
         speak_response(f"Today's date is {date} and currently time is {time.hour}:{time.minute}.")
     elif assist == "I want to do a web search":
         web_search()
     elif assist == "I want to calculate something.":
         calculate()
     elif assist == "I want to know the meaning of a word":
         get_word_meaning()
     elif assist == "What's the latest news?":
         get_latest_news()
     elif assist == "I want to translate a sentence.":
         translate_sentence()
     elif assist == "Tell me the system specifications of my computer.":
         get_system_specifications()
     elif assist == "Who are you":
         st.write("I am your virtual assistant, an AI-powered program designed to help you with a variety of basic tasks and answer your questions. I can assist you with tasks such as setting reminders, providing weather updates, searching the web for information, scheduling events, sending messages, and more. Just let me know what you need help with, and I'll do my best to assist you efficiently and accurately.")
         speak_response("I am your virtual assistant, an AI-powered program designed to help you with a variety of basic tasks and answer your questions.")
     else:
         st.write("Command not recognized. Try Again....")
         speak_response("Command not recognized. Please try again.")
 
 if __name__ == "__main__":
     greet_user()

else:
  page_bg_img = '''
  <style>
  [data-testid="stAppViewContainer"]{
  background-image: url("https://images.hdqwalls.com/wallpapers/mountains-minimal-landscape-4k-5b.jpg");
  background-size: cover;
  }
  [data-testid="stHeader"] {
  background: rgba(0,0,0,0);
  }
  </style>
  '''
  st.markdown(page_bg_img, unsafe_allow_html=True)

  st.write("Sure, here's an explanation on how to use the virtual assistant you've created:\n\n"
  "**Step 1: Greeting and Personalization**\n"
  "When you start the virtual assistant, it will greet you based on the time of day. You can make the greeting more personal by entering your name. The assistant will then determine whether it's morning, afternoon, evening, or night and greet you accordingly.\n\n"
  "**Step 2: Weather Information**\n"
  "To get the current weather information for a specific city, type the city's name in the provided text input and click the 'Get Weather' button. The assistant will fetch the temperature, humidity, and cloud conditions for that city and display them on the screen. Additionally, it will read the weather information aloud.\n\n"
  "**Step 3: Web Search**\n"
  "You can use the virtual assistant to search the web for information. Enter your query in the text input provided and click the 'Search' button. The assistant will display a list of search results on the screen, and it will also read the search results aloud.\n\n"
  "**Step 4: Calculator**\n"
  "Perform calculations using the virtual assistant. Type in the mathematical operation you want to perform (+, -, *, /, **) and two numbers. Click the 'Calculate' button to get the result of the calculation. The assistant will display the result on the screen and read it aloud.\n\n"
  "**Step 5: Word Meaning**\n"
  "If you're curious about the meaning of a word, enter the word in the text input and click the 'Search Meaning' button. The virtual assistant will use WordNet to find the definition of the word and display it on the screen. It will also read the meaning aloud.\n\n"
  "**Step 6: Latest News**\n"
  "Stay up to date with the latest news. By clicking the 'Get Latest News' button, the virtual assistant will retrieve the top headlines from a news API and display them on the screen. It will also read the headlines aloud.\n\n"
  "**Step 7: Translation**\n"
  "Translate sentences to different languages using the virtual assistant. Enter the sentence you want to translate in the text input, and specify the target language. Click the 'Translate' button to see the translated sentence and hear it spoken aloud.\n\n"
  "**Step 8: System Specifications**\n"
  "If you're curious about your computer's system specifications, click the 'Get System Specs' button. The virtual assistant will provide information about your system's architecture, operating system, release version, and processor. This information will be displayed on the screen and read aloud.\n\n"
  "**Step 9: About the Assistant**\n"
  "To learn more about the virtual assistant itself, select the 'Who are you' option. The assistant will introduce itself and provide an overview of its capabilities and functions.\n\n"
  "**Step 10: Invalid Command**\n"
  "If you enter a command that the virtual assistant doesn't understand, it will let you know that the command is not recognized. It will suggest trying again or selecting a different option from the menu.\n\n"
  "Feel free to explore the various options offered by the virtual assistant and let it assist you with different tasks, from weather updates to calculations, translations, and more. This AI-powered assistant is designed to make your life easier and provide you with quick and helpful information.")
 
  
 