import streamlit as st



def back():
    st.session_state.submit = None
    st.session_state.restore = True

def refresh():
    st.session_state.submit = None
    st.session_state.restore = False

def show_result(amount,single,multiple,text,single_answers,multiple_answers,text_answers):
    st.button("重组试题", on_click=refresh)
    st.button("重做本卷", on_click=back)

    score = 0
    # 记录选择框判断位置
    check_index = 0
    # 收集每道题选择数量
    check_len = []
    # 单选
    for i, question in enumerate(single):
        if single_answers[i] == question['answer']:
            score += 1
        else:
            pass
    # 多选
    # 用户选择的选项
    select_options = []
    for i, question in enumerate(multiple):
        select_option = []
        for j in range(len(multiple_answers[i])):
            if multiple_answers[i][j] == True:
                select_option.append(multiple[i]["option"][j])

        select_options.append(select_option)

    for i in range(5):
        if select_options[i] == multiple[i]["answer"]:
            score += 2

    # 填空
    for i,question in enumerate(text):
        if text_answers[i] == text[i]['answer']:
            score += 2

    st.markdown(f"##### 您的分数为：{score}")
    st.markdown(f"##### 百分制分数为：{str(round(100*int(score)/(1.5*amount),2))}")

    with st.expander("展开原卷"):

        st.markdown("**一、单项选择题（"+str(int(amount/2))+"题，每题1分）**")
        # 从session_state中获取数据
        for i, question in enumerate(single):
            st.write(f"问题 {i + 1}: {question['question']}")
            if question['answer'] == single_answers[i]:
                st.success("您的答案：" + str(single_answers[i]))
            else:
                st.error("您的答案：" + str(single_answers[i]))
                st.info("正确答案：" + str(question['answer']))

        st.markdown("**二、多项选择题（"+str(int(amount/4))+"题，每题2分）**")
        for i,question in enumerate(multiple):
            st.write(f"问题 {i + 1}: {question['question']}")

            if multiple[i]['answer'] == select_options[i]:
                st.success("您的答案：" + str(select_options[i]))
            else:
                st.error("您的答案：" + str(select_options[i]))
                st.info("正确答案：" + str(multiple[i]['answer']))

        st.markdown("**三、填空题（"+str(int(amount/4))+"题，每题2分）**")
        for i, question in enumerate(text):
            st.write(f"问题 {i + 1}: {question['question']}")
            if text_answers[i] == text[i]['answer']:
                st.success("您的答案：" + str(text_answers[i]))
            else:
                st.error("您的答案：" + str(text_answers[i]))
                st.info("正确答案：" + str(text[i]['answer']))
