import asyncio
import os
import pickle
import sys
import webbrowser
from streamlit_option_menu import option_menu
import extra_streamlit_components as stx
import oneai
import streamlit as st
import streamlit.components.v1 as components
from pytube import YouTube
from design import *
import regex as re
from PIL import Image

def file_list():
    files = [] 
    AudioFiles = [] 
    i = 1
    for (dirpath, dirnames, filenames) in os.walk('./Podcastapp/files/Piclke'):
        files.extend(filenames)
        break
    for (dirpath, dirnames, filenames) in os.walk('./Podcastapp/files/Audio'):
        AudioFiles.extend(filenames)
        break
    for f in AudioFiles:
        os.remove("./Podcastapp/files/Audio/"+f)
    
    return files

def files_display():
    files = file_list()
    clean_files = []
    for i,file in enumerate(files):
        clean_file = str(i+1) +". "+ str(file)[:-18].replace("_"," ")
        clean_files.append(clean_file)
    return clean_files

def get_pickle(option):
    i = int(option.split(". ",1)[0])
    ref = file_list()[i-1][-18:-7]
    name = './Podcastapp/files/Piclke/' + file_list()[i-1].replace(" ","_")
    pick = open(name,'rb')
    try:
        x = pickle.load(pick)
    except EOFError:
        pass
    return [x,ref]
    
def linkable_labels(data:oneai.Output,ref):
    label_str_lst = []
    start_time_list = []
    for i,x in enumerate(data):
        start_time = str(x.timestamp.seconds)
        label_str = x.value + ": "+ x.span_text
        start_time_list.append(int(start_time))
        label_str_lst.append(label_str)
    return [label_str_lst,start_time_list]
    
def linkable_chapters(data:oneai.Output):
    chapters_str_lst = []
    start_time_list = []
    for i,x in enumerate(data):
        start_time = str(x.timestamp.seconds)
        chapter_str = x.data['subheading']
        start_time_list.append(int(start_time))
        chapters_str_lst.append(chapter_str)
    return [chapters_str_lst,start_time_list]

def getMP3File(url):
    try:
        yt = YouTube(url)
        audio = yt.streams.get_audio_only()
        out_file = audio.download(output_path='./Podcastapp/files/Audio')
        base, ext = os.path.splitext(out_file)
        new_file = base + url[len(url)-11:]+'.mp3'
        new_file = new_file.replace(" ","_")
        os.rename(out_file, new_file)
        return(new_file)
    except:
        pass

def create_pickle(url):
    path = getMP3File(url)
    res = oneai_res(path)
    pickle_name = './Podcastapp/files/Piclke'+ path.split("./Podcastapp/files/Audio",1)[1][:-4]+".pickle"
    with open(pickle_name, 'wb') as f:
        pickle.dump(res.transcription, f)
    file_list()
    return [path,res]

def oneai_res(path):
    with open(path, "rb") as f:
        pipeline = oneai.Pipeline(
        steps = [
            oneai.skills.Transcribe(),
            oneai.skills.Proofread(),
            oneai.skills.Topics(),
            oneai.skills.Sentiments(),
            oneai.skills.SplitByTopic(),
            oneai.skills.Summarize(min_length=500),
        ]
        )
        output = asyncio.run(pipeline.run_async(f))
        return(output)
       
def side_bar_and_tabs(option):
    x = get_pickle(option)
    oneai_res = x[0]
    ref = x[1]
    url = "https://www.youtube.com/watch?v="+ref
    tab_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="Transcription", title="Transcribe", description=False),
    stx.TabBarItemData(id="Sentiments", title="Extract Sentiment", description=False),
    stx.TabBarItemData(id="Chapters", title="Split to Chapters", description=False)])
    topic_str = "Topics: " + ''.join(["#"+ x.value for x in oneai_res.proofread.topics])
    summary_str = "Summary: " + oneai_res.proofread.summary.text
    placeholder_side = st.sidebar.container()
    placeholser_topic = st.container()
    placeholder_vid = st.container()
    placeholder_summary = st.container()
    transcription_str = ''.join([x.speaker + ": " + x.utterance + "<br>" for x in oneai_res.proofread.text])
    if tab_id == "Transcription": 
        placeholder_side.markdown(f'<h1 style="font-size: 24px; color: #1C1D29; font-weight: bold;">{tab_id}</h1>', unsafe_allow_html=True)
        placeholder_side.markdown(f'<p style="font-size: 18px; color: #1C1D29; font-weight: normal;">{transcription_str}</p>', unsafe_allow_html=True)
        placeholser_topic.markdown(f'<h1 style="font-size: 24px; color: #FFFFFF; font-weight: bold;">{topic_str}</h1>', unsafe_allow_html=True)
        placeholder_vid.video(url)
        placeholder_summary.markdown(f'<h1 style="font-size: 24px; color: #FFFFFF; font-weight: normal ;">{summary_str}</h1>', unsafe_allow_html=True)
    elif tab_id == "Sentiments": 
        placeholder_side.markdown(f'<h1 style="font-size: 24px; color: #1C1D29; font-weight: bold;">{tab_id}</h1>', unsafe_allow_html=True)
        labels_data = linkable_labels(oneai_res.proofread.sentiments,ref)
        for i,x in enumerate(labels_data[0]):
            col1,col2 = placeholder_side.columns([0.5,4])
            col2.markdown(f'<p style="font-size: 18px; color: #1C1D29; font-weight: normal;">{x}</p>', unsafe_allow_html=True)
            if col1.button(str(i+1)):
                start_time = labels_data[1][i]
                placeholser_topic.markdown(f'<h1 style="font-size: 24px; color: #FFFFFF; font-weight: bold;">{topic_str}</h1>', unsafe_allow_html=True)
                placeholder_vid.video(url,start_time=start_time)
                placeholder_summary.markdown(f'<h1 style="font-size: 24px; color: #FFFFFF; font-weight: normal ;">{summary_str}</h1>', unsafe_allow_html=True)
    elif tab_id == "Chapters":
        placeholder_side.markdown(f'<h1 style="font-size: 24px; color: #1C1D29; font-weight: bold;">{tab_id}</h1>', unsafe_allow_html=True)
        chapters_data = linkable_chapters(oneai_res.proofread.segments)
        for i,x in enumerate(chapters_data[0]):
            col1,col2 = placeholder_side.columns([0.5,4])
            col2.markdown(f'<p style="font-size: 18px; color: #1C1D29; font-weight: normal;">{x}</p>', unsafe_allow_html=True)
            if col1.button(str(i+1)):
                start_time = chapters_data[1][i]
                placeholser_topic.markdown(f'<h1 style="font-size: 24px; color: #FFFFFF; font-weight: bold;">{topic_str}</h1>', unsafe_allow_html=True)
                placeholder_vid.video(url,start_time=start_time)
                placeholder_summary.markdown(f'<h1 style="font-size: 24px; color: #FFFFFF; font-weight: bold;">{summary_str}</h1>', unsafe_allow_html=True)
    else:
        placeholser_topic.markdown(f'<h1 style="font-size: 24px; color: #FFFFFF; font-weight: bold;">{topic_str}</h1>', unsafe_allow_html=True)
        placeholder_vid.video(url)
        placeholder_summary.markdown(f'<h1 style="font-size: 24px; color: #FFFFFF; font-weight: normal ;">{summary_str}</h1>', unsafe_allow_html=True)

def start_loader():
    intro_str = """ \n\n In this example we used podcast episodes from YouTube and ran them through our text analytics pipeline """
    instruction_str = """ \n\n
1. Select an episode from the dropdown menu
2. Press the Transcribe, Extract Sentiment, or Split to Chapters buttons
3. You can also click the buttons next to the sentiment/chapter on the left to get directly to the relevant part of the video
"""
    image = Image.open('Podcastapp/logo.png')
    col1,col2 = st.columns([3,1])
    col2.image(image, caption=None, width=200, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    col1.markdown(f'<h1 style="font-size: 24px; color: #FFFFFF; font-weight: normal ;">One AI Design Reference - Language AI for Podcasts</h1>', unsafe_allow_html=True) 
    st.markdown(f'<p style="font-size: 24px; color: #FFFFFF; font-weight: normal ;">{intro_str}</p>', unsafe_allow_html=True) 
    st.markdown(f'<p style="font-size: 24px; color: #FFFFFF; font-weight: normal ;">{instruction_str}</p>', unsafe_allow_html=True) 
    st.markdown(f'<a href="https://github.com/yaelK1/ReferenceDesign/tree/main/Podcastapp">See code</a>', unsafe_allow_html=True) 
    option = st.selectbox("",files_display())
    
    if not option is None:
        side_bar_and_tabs(option) 
    

