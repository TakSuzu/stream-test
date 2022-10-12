import streamlit as st
import pandas as pd
import time
import altair as alt

st.title("hello")

st.write("おためしです")


check = st.checkbox("チェックすると表示される") #引数に入れることでboolを返す

if check:
   st.button("ボタン") #引数に入れるとboolで返す
   st.selectbox("メニューリスト", ("選択肢1", "選択肢2", "選択肢3")) #第一引数：リスト名、第二引数：選択肢
   st.multiselect("メニューリスト（複数選択可）", ("選択肢1", "選択肢2", "選択肢3")) #第一引数：リスト名、第二引数：選択肢、複数選択可
   st.radio("ラジオボタン", ("選択肢1", "選択肢2", "選択肢3")) #第一引数：リスト名（選択肢群の上に表示）、第二引数：選択肢
   st.text_input("文字入力欄") #引数に入力内容を渡せる
   st.text_area("テキストエリア")


# 以下をサイドバーに表示
st.sidebar.text_input("サイドバー文字入力欄") #引数に入力内容を渡せる
#st.sidebar.text_area("テキストエリア２")


@st.cache
def get_UN_data():
    df = pd.read_csv("Covid_infection.csv")
    return df.set_index("date")


df = get_UN_data()


data = df.loc[:,"num"]

df.index = pd.to_datetime(df.index)

st.markdown("# 感染者数の推移グラフ")

data = data.T.reset_index()

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = data.loc[0:1,"num"]
#chart = st.line_chart(last_rows)
chart = st.line_chart(df.loc[:,"num"][0:10])

for i in range(1, len(df)):
    #status_text.text("%i%% Complete" % i)
    #chart.add_rows(data.loc[i:i+1,"num"])
    chart.add_rows(df.loc[:,"num"][i:i+1])
    #progress_bar.progress(i)
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")


st.markdown("## パターン2")


chart = (
    alt.Chart(data)
    .mark_circle()#area(opacity=0.7)
    .encode(
        x="date:T",
        y=alt.Y("感染者数:Q", stack=None),
        color="Region:N",
    )
)
st.altair_chart(chart, use_container_width=True)
