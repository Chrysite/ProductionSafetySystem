import streamlit as st
import time
from streamlit.components.v1 import html

from conf.path import md_path

st.set_page_config(
    page_title="知识学习模块",layout="wide"
)


with st.sidebar:
    # 选择框
    select_box = st.selectbox(
        "请选择要学习的内容",
        ("1.法律法规", "2.危险物质", "3.气象因素", "4.地理环境", "5.人员培训","6.安全规程")
    )
    # 创建一个会话状态来存储计时器的状态
    if 'timer_started' not in st.session_state:
        st.session_state.timer_started = False
    if 'elapsed_time' not in st.session_state:
        st.session_state.elapsed_time = 0

    start_button = st.button("开始")
    stop_button = st.button("停止")
    reset_button = st.button("更新时间")

    if start_button:
        st.session_state.start_time = time.time()
        st.session_state.running = True

    if stop_button:
        st.session_state.running = False

    if reset_button:
        st.session_state.elapsed_time = 0

    if 'running' in st.session_state and st.session_state.running:
        elapsed_time = int(time.time() - st.session_state.start_time)
        minutes, seconds = divmod(elapsed_time, 60)
        st.write(f"学习时间: {minutes:02d}:{seconds:02d}")

def read_markdown_file(markdown_file):
    with open(markdown_file, encoding='utf-8') as fp:
        w = fp.read()
    return w

if select_box == "1.法律法规":
    intro_markdown = read_markdown_file(md_path + "/1.法律法规.md")
    st.markdown(intro_markdown, unsafe_allow_html=True)
if select_box == "2.危险物质":
    intro_markdown = read_markdown_file(md_path + "/2.危险物质.md")
    st.markdown(intro_markdown, unsafe_allow_html=True)
if select_box == "3.气象因素":
    intro_markdown = read_markdown_file(md_path + "/3.气象因素.md")
    st.markdown(intro_markdown, unsafe_allow_html=True)
if select_box == "4.地理环境":
    intro_markdown = read_markdown_file(md_path + "/4.地理环境.md")
    st.markdown(intro_markdown, unsafe_allow_html=True)
if select_box == "5.人员培训":
    intro_markdown = read_markdown_file(md_path + "/5.人员培训.md")
    st.markdown(intro_markdown, unsafe_allow_html=True)
if select_box == "6.安全规程":
    intro_markdown = read_markdown_file(md_path + "/6.安全规程.md")
    st.markdown(intro_markdown, unsafe_allow_html=True)

