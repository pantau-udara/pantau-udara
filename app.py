import streamlit as st
import requests
import pandas as pd

TOKEN = st.secrets["TOKEN"]

st.title("Pemantauan Kualitas Udara")

kota_list = st.multiselect(
    "Pilih kota",
    ["jakarta", "bandung", "surabaya", "medan", "yogyakarta"],
    default=["jakarta", "bandung"],
)

@st.cache_data(ttl=600)
def ambil(kota):
    url = f"https://api.waqi.info/feed/{kota}/?token={TOKEN}"
    r = requests.get(url, timeout=10).json()
    if r["status"] != "ok":
        return None
    d = r["data"]
    return {
        "kota": kota,
        "stasiun": d["city"]["name"],
        "aqi": pd.to_numeric(d["aqi"], errors="coerce"),
        "pm25": d["iaqi"].get("pm25", {}).get("v"),
        "lat": d["city"]["geo"][0],
        "lon": d["city"]["geo"][1],
    }

hasil = [ambil(k) for k in kota_list]
df = pd.DataFrame([h for h in hasil if h])

if df.empty:
    st.info("Pilih minimal satu kota.")
else:
    st.dataframe(df[["kota", "stasiun", "aqi", "pm25"]])
    st.bar_chart(df.set_index("kota")["aqi"])
    st.map(df)
