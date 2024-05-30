import json
import os
import random
import streamlit as st

from conf.path import json_path
from core.submit_answer import show_result

st.set_page_config(
    page_title="考试",layout="wide"
)

# 读取json文件,并储存进sesson_state
if 'single_data' not in st.session_state:
    st.session_state.amount = 0
    st.session_state.submit = False
    st.session_state.restore = False
    with open(os.path.join(json_path, "single.json"), "r", encoding="utf-8") as fp:
        st.session_state.single_data = json.load(fp)
    with open(os.path.join(json_path, "multiple.json"), "r", encoding="utf-8") as fp:
        st.session_state.multiple_data = json.load(fp)
    with open(os.path.join(json_path, "text.json"), "r", encoding="utf-8") as fp:
        st.session_state.text_data = json.load(fp)
    # with open(os.path.join(json_path, "text_1.json"), "r", encoding="utf-8") as fp:
    #     st.session_state.text_1_data = json.load(fp)

if 'single_answers' not in st.session_state:
    st.session_state.single_answers = []
    st.session_state.multiple_answers = []
    st.session_state.text_answers = []
    # st.session_state.text_1_answers = []

if not st.session_state.submit:
    st.session_state.single_answers = []
    st.session_state.multiple_answers = []
    st.session_state.text_answers = []

# 侧边栏，试卷form，提交页面

# 提交试卷
def submit():
    st.session_state.submit = True
    st.session_state.restore = True
    # 显示结果，传入试卷内容（单选、多选、填空以及各部分用户选择的答案）


def refresh():
    st.session_state.restore = True
    st.session_state.disabled = False


# 侧边栏添加选择难度
# 难度选择
difficulty_level = ["请选择", "一级（20题）", "二级（40题）", "三级（60题）"]

# 初始化session_state
if 'selected_option' not in st.session_state:
    st.session_state['selected_option'] = difficulty_level[0]

with st.sidebar:
    selected = st.radio(
        "选择考试难度",
        difficulty_level,
        key="questions_amount"
    )

# 题目数量
questions_amount = int(difficulty_level.index(st.session_state.questions_amount) * 20)


# 未选择时，提示选择题量
if questions_amount == 0:
    st.warning("请选择考试难度以生成试卷！")

# 当选项改变时，更新session_state
if selected != st.session_state['selected_option']:
    st.session_state['selected_option'] = selected
    # 执行相关操作
    st.session_state.submit = False
    st.session_state.restore = False

    # if st.session_state['selected_option'] == "二级（40题）":
    #     st.session_state.text_data = st.session_state.text_1_data
    # if questions_amount == 60:
    #     st.session_state.text_data = st.session_state.text_1_data
    # else:
    #     pass

# 选择20题难度
if questions_amount == 20:
    st.session_state.amount = 20
if questions_amount == 40:
    st.session_state.amount = 40
if questions_amount == 60:
    st.session_state.amount = 60

if not questions_amount == 0:
    amount = st.session_state.amount
    # 判断是否已提交试卷，若未提交则显示原卷
    if not st.session_state.submit:
        with st.form("paper"):
            # 获取数据
            single_data = st.session_state.single_data
            multiple_data = st.session_state.multiple_data
            text_data = st.session_state.text_data
            # 单选
            st.markdown("**一、单项选择题（"+str(int(amount/2))+"题，每题1分）**")
            # 判断是否有储存试卷且是否提取
            if st.session_state.restore:
                single = st.session_state.single
                multiple = st.session_state.multiple
                text = st.session_state.text
            else:
                # 随机抽取数据
                single = random.sample(single_data["questions"], int(amount/2))
                # 储存数据，便于提交试卷后获取题目
                st.session_state.single = single
                # 随机抽取5组多选数据
                multiple = random.sample(multiple_data["questions"], int(amount/4))
                st.session_state.multiple = multiple
                text = random.sample(text_data['questions'],int(amount/4))
                st.session_state.text = text
            # 遍历json文件中的每个问题
            for i, question in enumerate(single):
                st.write(f"问题 {i + 1}: {question['question']}")
                # 获取选项
                options = question['option']
                # 使用 radio展示选项，并获取用户的选择
                answer = st.radio("请选择你的答案：", options, key=str(i))
                # 将用户的答案储存到列表中
                st.session_state.single_answers.append(answer)
            # 多选（5）
            st.markdown("**二、多项选择题（"+str(int(amount/4))+"题，每题2分，多选少选都不得分）**")
            st.session_state.multiple_answers = []

            # 遍历json文件中的每个问题
            for i, question in enumerate(multiple):
                st.write(f"问题 {i + 1}: {question['question']}")
                options = question['option']
                # 使用selectbox展示选项，并获取用户的选择
                st.write("请选择你的答案：")
                check_answer = []
                for k,j in enumerate(options):
                    check_answer.append(st.checkbox(j,key=(i+1)*100+k))
                st.session_state.multiple_answers.append(check_answer)

            st.markdown("**三、填空题（"+str(int(amount/4))+"题，每题2分）**")
            text_answers = []
            key_num = 1000
            for i,question in enumerate(text):
                key_num += 1
                st.write(f"问题 {i + 1}: {question['question']}")
                text_answers.append(st.text_input("请输入答案",key=key_num+amount))
            st.session_state.text_answers = text_answers

            st.write("注：提交试卷前请先保存答案！")
            st.form_submit_button('保存答案',on_click=refresh, use_container_width=True)
            st.form_submit_button(label='提交试卷', use_container_width=True, on_click=submit)


if st.session_state.submit:
    show_result(st.session_state.amount,
                st.session_state.single,
                st.session_state.multiple,
                st.session_state.text,
                st.session_state.single_answers,
                st.session_state.multiple_answers,
                st.session_state.text_answers)
