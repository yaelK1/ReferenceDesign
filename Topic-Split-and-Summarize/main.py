import streamlit as st
import pickle
import oneai
from pytube import YouTube
import os
import sys
import webbrowser
import asyncio
import streamlit.components.v1 as components
from design import *

global files

oneai.api_key = "bd883760-daa9-4bfe-8702-bd4fc90cdea0"


def chapters_to_summaries(chapters):
    pipeline_summaries = oneai.Pipeline(steps=[oneai.skills.Summarize(),])
    summaries = []
    for chapter in chapters:
        output_summary = asyncio.run(pipeline_summaries.run_async(chapter))
        summaries.append(output_summary.summary.text)
    return summaries


def oneai_seg_text(text: oneai.Input, selected_option_topics: str) -> oneai.Output:
    pipeline_text = oneai.Pipeline(
        steps=[oneai.skills.SplitByTopic(amount=selected_option_topics),]
    )
    output_chapters = asyncio.run(pipeline_text.run_async(text))
    chapters = [x.output_spans[0].text for x in output_chapters.segments]
    summaries = chapters_to_summaries(chapters)
    return summaries


def oneai_seg_url(url: oneai.Input, selected_option_topics: str) -> oneai.Output:
    pipeline_url = oneai.Pipeline(
        steps=[
            oneai.skills.HtmlToArticle(),
            oneai.skills.SplitByTopic(amount=selected_option_topics),
        ]
    )
    output_chapters = asyncio.run(pipeline_url.run_async(url))
    chapters = [x.output_spans[0].text for x in output_chapters.html_article.segments]
    summaries = chapters_to_summaries(chapters)
    return summaries


def start_loader():
    selected_option_topics = st.selectbox("Topic Split:", ["normal", "more", "less"],)
    break_str = "<br> *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* <br>"
    url = st.text_input("Enter html link")
    if url:
        output = oneai_seg_url(url, selected_option_topics)
        segments_str = break_str.join(output)
        st.markdown(segments_str, unsafe_allow_html=True)
    text = st.text_area("Enter text")
    if text:
        output = oneai_seg_text(text, selected_option_topics)
        segments_str = break_str.join(output)
        st.markdown(segments_str, unsafe_allow_html=True)

