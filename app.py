import streamlit as st
import pandas as pd
from io import StringIO
import seaborn as sns
from scipy.stats import ttest_ind

age = st.number_input("Age", value=35, placeholder="Type a number...")
work_days = st.number_input("Work days", value=2, placeholder="Type a number...")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    data = pd.read_csv(uploaded_file)
    data = data[data["Количество больничных дней"] > work_days]
    st.write(data)
    data['IsOld'] = data['Возраст'] > age
    data["IsOld"] = data["IsOld"].map({True: 1, False: 0})
    gender_plot = sns.displot(x="Количество больничных дней", data=data, kind="kde", hue="Пол")
    st.pyplot(gender_plot)
    age_plot = sns.displot(x="Количество больничных дней", data=data, kind="kde", hue="IsOld")
    st.pyplot(age_plot)
    st.write("H_0: Количество больничных дней у мужчин и женщин имеет одинаковое распределение")
    st.write("H_1: Количество больничных дней у мужчин и женщин имеет разное распределение")
    st.write("Определим уровень значимости 0.05")
    women = data[data["Пол"] == "Ж"]
    men = data[data["Пол"] == "М"]
    gender_result = ttest_ind(women['Количество больничных дней'], men['Количество больничных дней'])
    st.write("P-value: ", gender_result.pvalue)
    if gender_result.pvalue < 0.05:
        st.write("Количество больничных дней у мужчин и женщин имеет разное распределение")
    else:
        st.write("Количество больничных дней у мужчин и женщин имеет одинаковое распределение")
    st.write("H_0: Количество больничных дней у взрослых и молодых сотрудников имеет одинаковое распределение")
    st.write("H_1: Количество больничных дней у взрослых и молодых сотрудников имеет разное распределение")
    st.write("Определим уровень значимости 0.05")
    old = data[data['IsOld'] == 1]
    young = data[data['IsOld'] == 0]
    age_result = ttest_ind(old["Количество больничных дней"], young["Количество больничных дней"])
    st.write("P-value: ", age_result.pvalue)
    if age_result.pvalue < 0.05:
        st.write("Количество больничных дней у взрослых и молодых сотрудников имеет разное распределение")
    else:
        st.write("Количество больничных дней у взрослых и молодых сотрудников имеет одинаковое распределение")