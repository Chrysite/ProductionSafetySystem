import json
import os
import streamlit as st
from fuzzywuzzy import fuzz

from core.chemical_card import chemicalCard
from conf.menu import menu_items
from conf.path import json_path


st.set_page_config(page_title="常见危险化学品", page_icon="🧪", layout="wide", menu_items=menu_items)
st.markdown("### 🧪 常见危险化学品")

def load_chemicals():
    with open(os.path.join(json_path, "chemicals.json"), "r", encoding="utf-8") as fp:
        chemicals_data = json.load(fp)
    return chemicals_data

if "chemicals_data" not in st.session_state:
    st.session_state.chemicals_data = load_chemicals()


st.radio(
    "选择检索方式",
    ("关键词检索", "CAS检索"),
    horizontal=True,
    key="chemicals_query_mode",
    label_visibility="collapsed"
)

if st.session_state.get("chemicals_query_mode") == "关键词检索":
    data = [] # 储存查找的数据
    data_name = [] # 储存查找的数据名称
    sorted_name = [] # 储存排列后的数据名称
    select_data = None # 选择查看的数据
    keywords = st.text_input(label="请输入要检索的化学品：", key="chemical_query_keywords")
    start_query = st.button("搜索", key="start_query_chemical")

    # 若输入关键词
    if keywords != "":
        # 在危化品库中查找
        for i in st.session_state.chemicals_data:
            # 匹配系数
            match_num = fuzz.ratio(i['name'][0], keywords)
            if match_num>50:
                i['match_num'] = match_num
                data_name.append(i['name'][0])
                data.append(i)
        if data != []:
            # 按照匹配系数大小，从大到小排列
            sorted_list = sorted(data, key=lambda x: x['match_num'],reverse=True)
            for i in sorted_list:
                sorted_name.append(i['name'][0])
            select_name = st.selectbox("以下是搜索结果",sorted_name)
            for i in data:
                if select_name == i['name'][0]:
                    select_data = i
            if select_data != None:
                chemicalCard(select_data)
        else:
            st.warning("未查询到结果")


if st.session_state.get("chemicals_query_mode") == "CAS检索":
    data = []
    data_name = []
    select_data = None
    keywords = st.text_input(label="请输入要检索的化学品：", key="chemical_query_keywords")
    start_query = st.button("搜索", key="start_query_chemical")
    if keywords != "":
        for i in st.session_state.chemicals_data:
            if keywords == i['cas_number'][0]:
                data_name = i['name'][0]
                select_data = i

        if select_data != None:
            chemicalCard(select_data)
        else:
            st.warning("未查询到结果")


