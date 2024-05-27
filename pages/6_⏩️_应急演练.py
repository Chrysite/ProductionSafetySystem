# coding=utf8
import base64
import copy
import time
import json
import os

import streamlit as st
from PIL import Image

from conf.path import json_path, video_path, practice_path
from core.set_plans import setPlans
#
# theme = {"火灾","爆炸","毒气排放"}
#
# # with options_titleen(os.path.join(json_path, "plans.json"), "r", encoding="utf-8") as fp:
# #     plans = json.load(fp)
# #
# #
# # 主题
# with st.sidebar:
#     theme_select = st.selectbox(
#         "选择主题",
#         theme
#     )
#
# for i in plan:
#     if i['theme'] == theme_select:
#
#         with st.form("plans"):
#
#
#
#             for options_titles_index, options_title in enumerate(options_titles):
#                 st.multiselect(
#                     options_titles_Ch[options_titles_index],
#                     options_dict[options_title],
#                     default=st.session_state.get(options_title),
#                     key=options_title
#                 )
#             if st.form_submit_button("预览演练步骤", use_container_width=True):
#                 step_index = 1
#                 for options_titles_index, options_title in enumerate(options_titles):
#                     if st.session_state.get(options_title):
#                         st.markdown(f":orange[{options_titles_Ch[options_titles_index]}]")
#                         for step in st.session_state[options_title]:
#                             st.markdown(f":blue[\[{step_index}\]{step}]")
#                             step_index += 1
#                 if step_index == 1:
#                     st.warning("您未选择任何演练步骤！")
#             if st.form_submit_button("提交演练步骤", use_container_width=True):
#                 # 获取用户答案
#                 answers = {}
#                 for options_titles_index, options_title in enumerate(options_titles):
#                     answers[options_title] = st.session_state.get(options_title)
#                 # 获取正确答案
#                 for plan in plan:
#                     if plan["theme"] == st.session_state.get("themes_option"):
#                         if plan["chemical_types"] == st.session_state.get("chemical_types_option"):
#                             correct_answers = plan
#                 # 展示正确答案
#                 step_index = 1
#                 # 评分细则
#                 report = ""
#                 # 总分
#                 grades = 0
#                 # 得分
#                 get_grades = 0
#                 for options_titles_index, options_title in enumerate(options_titles):
#                     report += f":orange[{options_titles_Ch[options_titles_index]}]\n\n"
#                     steps = answers[options_title]
#                     correct_steps = correct_answers[options_title]
#                     for step in correct_steps:
#                         # 交集, 即正确步骤
#                         if step in steps:
#                             report += f"（+10）:green[\[{step_index}\]{step}]\n\n"
#                             get_grades += 10
#                         # 未选择的步骤
#                         else:
#                             report += f"（+0）:violet[\[{step_index}\]{step}]\n\n"
#                         step_index += 1
#                         grades += 10
#                     # 错误或多余的步骤
#                     left_steps = list(set(steps).difference(set(correct_steps)))
#                     for step in left_steps:
#                         report += f"（-5）:red[~~{step}~~]\n\n"
#                         get_grades -= 5
#                 # 百分制得分
#                 get_hundred_grades = round(get_grades * 100 / grades, 2)
#                 st.markdown(f"##### 演练总分：{grades}")
#                 st.markdown(f"##### 实际得分：{get_grades}")
#                 st.markdown(f"##### 百分制得分：{get_hundred_grades}")
#                 st.markdown(report)
#


def resetOptions():
    for options_title_i in options_titles:
        st.session_state[f"expand_{options_title_i}"] = False
        st.session_state[options_title_i] = []


with st.spinner("正在载入应急演练案例数据..."):
    # 加载应急演练案例数据
    themes, options_dict, plans = setPlans()

# 主题列表
themes_list = list(themes.keys())
# 选项题目
options_titles = ["former_periods", "command_centre", "engineering_team", "methods", "alert_team", "medical_team", "after_periods"]
options_titles_Ch = ["应急开始阶段", "指挥中心", "工程抢险组", "特殊情况处置", "警戒治安组", "医疗救护组", "应急结束阶段"]

# 主题对应的危化品
with st.sidebar:
    # 主题选择
    themes_option_index = 0
    if st.session_state.get("themes_option") is not None:
        themes_option_index = themes_list.index(st.session_state.get("themes_option"))
    themes_option = st.selectbox(
        "选择主题",
        themes_list,
        key="themes_option",
        index=themes_option_index,
        on_change=resetOptions
    )
    # 涉及的危化品
    chemical_types_list = themes[st.session_state.get("themes_option")]
    chemical_types_option_index = 0
    if st.session_state.get("chemical_types_option") in chemical_types_list:
        chemical_types_option_index = chemical_types_list.index(st.session_state.get("chemical_types_option"))
    chemical_types_option = st.selectbox(
        "选择涉及的危化品",
        chemical_types_list,
        key="chemical_types_option",
        index=chemical_types_option_index,
        on_change=resetOptions
    )

    video_btn = st.button("播放动画")


with st.form("plans"):
    for options_titles_index, options_title in enumerate(options_titles):
        st.multiselect(
            options_titles_Ch[options_titles_index],
            options_dict[options_title],
            default=st.session_state.get(options_title),
            key=options_title
        )
    if st.form_submit_button("预览演练步骤", use_container_width=True):
        step_index = 1
        for options_titles_index, options_title in enumerate(options_titles):
            if st.session_state.get(options_title):
                st.markdown(f":orange[{options_titles_Ch[options_titles_index]}]")
                for step in st.session_state[options_title]:
                    st.markdown(f":blue[\[{step_index}\]{step}]")
                    step_index += 1
        if step_index == 1:
            st.warning("您未选择任何演练步骤！")
    if st.form_submit_button("提交演练步骤", use_container_width=True):
        # 获取用户答案
        answers = {}
        for options_titles_index, options_title in enumerate(options_titles):
            answers[options_title] = st.session_state.get(options_title)
        # 获取正确答案
        for plan in plans:
            if plan["theme"] == st.session_state.get("themes_option"):
                if plan["chemical_types"] == st.session_state.get("chemical_types_option"):
                    correct_answers = plan
        # 展示正确答案
        step_index = 1
        # 评分细则
        report = ""
        # 总分
        grades = 0
        # 得分
        get_grades = 0
        for options_titles_index, options_title in enumerate(options_titles):
            report += f":orange[{options_titles_Ch[options_titles_index]}]\n\n"
            steps = answers[options_title]
            correct_steps = correct_answers[options_title]
            for step in correct_steps:
                # 交集, 即正确步骤
                if step in steps:
                    report += f"（+10）:green[\[{step_index}\]{step}]\n\n"
                    get_grades += 10
                # 未选择的步骤
                else:
                    report += f"（+0）:violet[\[{step_index}\]{step}]\n\n"
                step_index += 1
                grades += 10
            # 错误或多余的步骤
            left_steps = list(set(steps).difference(set(correct_steps)))
            for step in left_steps:
                report += f"（-5）:red[~~{step}~~]\n\n"
                get_grades -= 5
        # 百分制得分
        get_hundred_grades = round(get_grades * 100 / grades, 2)
        st.markdown(f"##### 演练总分：{grades}")
        st.markdown(f"##### 实际得分：{get_grades}")
        st.markdown(f"##### 百分制得分：{get_hundred_grades}")
        st.markdown(report)


if video_btn:

    st.title('化工厂爆燃事件公共卫生应急处置')
    st.markdown(
        "一、2016年5月20日上午10时10分，某化工厂中控室警报骤响，监控显示屏上显示为工厂西北角原料罐区有可燃气体泄露报警，值班班长迅速安排2名操作工穿戴空气呼吸器前往报警地点检查。15分钟后，值班班长在中控室接到现场情况报告。")


    video_file = open(video_path+'/现场人员向厂长报告.mkv', 'rb')
    video_bytes = video_file.read()
    # 使用st.video函数播放视频
    st.video(video_bytes)

    st.markdown("二、值班班长放下对讲机，立即拿起中控室固定电话向厂长报告着火情况，厂长立即拨打119消防救援电话。")
    st.markdown("三、值班班长向市政府应急办拨打电话")


    # 厂长给市政府应急办打电话
    video_file = open(video_path+'/厂长给市政府应急办打电话.mkv', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

    st.write("")
    st.radio("问：事故上报程序？", ('市政府应急办公室', '市政府办公室', '市卫生局', '市疾控中心'))
    st.write('事故报告应包括下面内容: (多选)')
    st.checkbox('事故发生的时间、地点、类型及事故现场', False)
    st.checkbox('事故的简要过程', False)
    st.checkbox('排放污染物的种类、数量', False)
    st.checkbox('事故已造成或者可能造成的人员伤亡情况和初步估计的直接经济损失', False)
    st.checkbox('已采取的应急措施', False)
    st.checkbox('已污染的范围', False)
    st.checkbox('潜在的危害程度，转化方式趋向，可能受影响区域', False)
    st.checkbox('采取的措施建议', False)


    image = Image.open(practice_path+'/选择装备.png')
    st.image(image, caption='Sunrise by the mountains', use_column_width=True)

    st.write('请选择携带的装备（多选）：')
    st.checkbox('一次性橡皮手套', False)
    st.checkbox('制冷剂', False)
    st.checkbox('胶鞋', False)
    st.checkbox('A级防护服', False)
    st.checkbox('自给式空气呼吸器', False)
    st.checkbox('采样器', False)
    st.checkbox('检气管', False)
    st.checkbox('便携式傅里叶红外气体分析仪', False)