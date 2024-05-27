import os
import pandas as pd
import streamlit as st
import json

from conf.menu import menu_items
from conf.path import case_path

st.set_page_config(page_title="国内外生产安全事故案例检索", page_icon="🌐", layout="wide", menu_items=menu_items)
st.markdown("### 🌐 国内外生产安全事故案例")


# 初始页面
if 'select' not in st.session_state:
    # 收集已筛选的数据
    st.session_state.item = []
    st.session_state.select = False
    st.session_state.name = ""
    st.session_state.disabled = False
    st.session_state.show = False
    st.session_state.pd = None
    st.session_state.event = None


# 返回按钮
def back():
    st.session_state.select = False
    st.session_state.show = True

# 选择按钮
def submit():
    st.session_state.show = False
    st.session_state.select = True


    for i in st.session_state.item:
        if st.session_state.event == i['name']:

            st.button("返回", on_click=back,use_container_width=True)
            st.markdown(" **事件：** " + i['name'], unsafe_allow_html=True)
            st.markdown(" **发生时间：** " + i['when'], unsafe_allow_html=True)
            st.markdown(" **发生地区：** " + i['where'], unsafe_allow_html=True)
            st.markdown(" **公司名称：** " + i['who'], unsafe_allow_html=True)
            st.markdown(" **事故摘要：** " + i['event'], unsafe_allow_html=True)
            st.markdown(" **事故发生主要原因：** " + i['cause'], unsafe_allow_html=True)
            st.markdown(" **应急措施：** " + i['emergency_response'], unsafe_allow_html=True)
            st.markdown(" **应急措施评价：** " + i['emergency_response_assessment'], unsafe_allow_html=True)


# “select为 False“，未选择
if not st.session_state.select:
    with st.form(key='select_form'):

        style = st.multiselect(
            '请选择事故类型',
            ('火灾','泄露','中毒')
        )
        area = st.multiselect(
            '请选择事故发生地区',
            ('全部','广东','河北','山西','辽宁','吉林','黑龙江','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','海南','四川','贵州','云南','陕西','甘肃','青海','台湾','内蒙古')
        )

        select_button = st.form_submit_button(label='检索',use_container_width=True)

        # 按下检索按钮
        # 先判断类型，包括火灾、泄露、中毒，单选多选
        # 再判断地区，全部单选多选
        if select_button:
            # 初始化
            st.session_state.show = False

            # 火灾事件
            with open(os.path.join(case_path, "fire.json"), "r", encoding="utf-8") as fp:
                content = fp.read()
            fire_item = json.loads(content)

            # 泄露事件
            with open(os.path.join(case_path, "divulge.json"), "r", encoding="utf-8") as fp:
                content = fp.read()
            divulge_item = json.loads(content)

            # 中毒事件
            with open(os.path.join(case_path, "poisoning.json"), "r", encoding="utf-8") as fp:
                content = fp.read()
            poisoning_item = json.loads(content)

            style_len = len(style)
            # 判断是否选择事故类型检索条件，不等于0说明有检索条件
            if style_len != 0:

                style_item = []
                # 若包含火灾，先将火灾的数据储存进列表
                if "火灾" in style:
                    style_item = fire_item
                if "泄露" in style:
                    for i in divulge_item:
                        style_item.append(i)
                if "中毒" in style:
                    for i in poisoning_item:
                        style_item.append(i)

                # 接下来判断地区，没选、全部、单个地区、多个地区
                area_len = len(area)
                # 有选择
                if area_len != 0:
                    area_item = style_item
                    # 全部，直接显示
                    if '全部' in area:
                        all_show = [{k: d[k] for k in ('name', 'keywords','when', 'where', 'who') if k in d} for d in area_item if
                                                      'name' in d and 'keywords' in d and 'when' in d and 'where' in d and 'who' in d]
                        all_pd = pd.DataFrame(all_show)
                        st.write(all_pd)
                        all_name = ([i['name'] for i in area_item])
                        st.session_state.item = area_item
                        st.session_state.pd = all_pd
                        st.session_state.name = all_name

                    # 不包含全部的话就看具体选了什么地区
                    else:
                        area_list = []
                        area_name = []
                        area_show = []
                        for i in area_item:
                            if i['province'] in area:
                                area_list.append(i)
                                area_name.append(i['name'])
                        area_show = [{k: d[k] for k in ('name','keywords', 'when','where','who') if k in d} for d in area_list if
                                     'name' in d and 'when' in d and 'where' in d and 'who' in d]
                        area_pd = pd.DataFrame(area_show)
                        st.write(area_pd)
                        st.session_state.name = area_name
                        st.session_state.item = area_list
                        st.session_state.pd = area_pd

                # 无选择
                else:
                    st.warning("请选择地区")

            else:
                st.warning("请选择事故类型")


# 若”st.session_state.show“为True，呈现事故案例具体信息
if st.session_state.show:
    st.write(st.session_state.pd)
    # st.write(st.session_state.event)

st.session_state.event = st.selectbox("请选择要查看具体信息的事故：", st.session_state.name)
if st.button(label='选择', use_container_width=True):
    if st.session_state.event == None:
        st.warning("没有数据")
    else:
        st.session_state.select = True
        submit()


