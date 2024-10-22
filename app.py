import streamlit as st
from BizCardX import app
from project import test
from YoutubeHarversting import main as yt
from DS_Phonepe.app import main
from SingaporResale import app as sr
st.sidebar.title('My Capstone Project')

selection = st.sidebar.radio("Go to",['BizCardX','YoutubeHarversting','DS_Phonepe','SingaporResale'])


if selection == 'BizCardX':
     app.main()
elif selection == 'YoutubeHarversting':
     yt.youtube_main()
elif selection == 'DS_Phonepe':
     main.phonepe_main()
elif selection == 'SingaporResale':
     sr.main()