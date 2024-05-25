# coding=utf8
import os

import streamlit as st

from conf.path import root_path, images_common_path
from conf.menu import menu_items

# ---------- Start:每页基础配置 ---------- #
st.set_page_config(page_title="首页", page_icon="🏠", layout="wide")
# initUserConfig()
# st.title("欢迎使用化工类企业生产安全应急预案模拟演练系统")

# 加载 README.md
with st.spinner("正在加载本站信息..."):
    with open(os.path.join(root_path, "README.md"), "r", encoding="utf-8") as fp:
        st.markdown(fp.read())
    with open(os.path.join(images_common_path, "motto.jpg"), "rb") as fp:
        st.image(fp.read())


# name = st.text_input('请输入用户名', max_chars=100, help='最大长度为100字符')
#
# # 根据用户输入进行操作
# st.write('您的用户名是', name)
