import streamlit as st
st.title("แอปพลิเคชันแปลงปี")

bh_year = st.number_input("กรอกปี พ.ศ.", value=2569)
ce_year = bh_year - 543
st.header(f"ปี ค.ศ. คือ : {ce_year}")
