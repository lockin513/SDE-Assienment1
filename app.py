import streamlit as st
import pandas as pd
import llm, json

# 设置页面标题
st.title('FAQ Uploader and Query Generator')

# 创建一个上传组件，允许用户上传 Excel 文件
uploaded_file = st.file_uploader("Upload your FAQ file", type=['xlsx', 'xls'], accept_multiple_files=False)

# 检查是否有文件被上传
if uploaded_file is not None:
    # 读取 Excel 文件到 Pandas 数据框架
    df = pd.read_excel(uploaded_file)
    
    # 显示数据框架
    st.subheader('Uploaded FAQ')
    st.write(df)


def generate_questions(sentence):
    system_prompt = f"You are a very cute secretary.Answer questions in sweet tone with Emoji"
    # read user_prompt from prompt.txt
    with open("prompt.txt", "r") as f:
        user_prompt = f.read()
    
    ## replace the topic in the user_prompt with the topic from the text_input
    user_prompt = user_prompt.replace("{sentence}", str(sentence))

    # display the user prompt
    print("User prompt:")
    print(user_prompt)
    
    results = llm.answer(system_prompt, user_prompt)
    return results


# 用户输入问题
user_question = st.text_input("Enter your question here")

# 检查是否有文件被上传和用户输入了问题
if uploaded_file is not None and user_question:
    # 查找匹配的问题和答案
    matched_rows = df[df['Question'].str.contains(user_question, case=False, na=False)]

    if "author" in user_question:
        response = generate_questions("the author of this app is Zhang Hanchang and his student ID is 24070116g.")
        st.subheader('AI Response')
        st.warning(response)
    elif not matched_rows.empty:
        # 显示回答
        st.subheader('AI Response')
        for index, row in matched_rows.iterrows():
            response = generate_questions(row['Answer'])
            categories = row['Category']
            question_id = row['Question ID']
            
            # 显示回答
            st.warning(f"Response: {response}")
            
            # Categories expander
            with st.expander("Categories"):
                if pd.notna(categories):
                    st.warning(f"Categories: {','.join(categories.split(','))}")
                else:
                    st.warning("Categories: N/A")
            
            # References expander
            with st.expander("References"):
                st.warning(f"References: [{question_id}] Question: {row['Question']}")
    else:
        response = generate_questions("I'm sorry, but I don't have information regarding your question. Please contact our customer representative for assistance.")
        st.subheader('AI Response')
        st.warning(response)
        with st.expander("References"):
            st.write("Categories: N/A")