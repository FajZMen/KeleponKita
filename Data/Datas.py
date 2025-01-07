import streamlit as st
from PIL import Image

accountscreated = 0
historypesananlist = []
vouchers = []
adminchathistory = []
supporthistory = []

produk = [
    {"Nama": "Kelepon", "Harga": 5000, "Gambar": "Kelepon.png"},
    {"Nama": "Mochi", "Harga": 8000, "Gambar": "Mochi.png"},
]

bannedaccounts = [
    {"username": "bannedperson", "reason": "bruh"},
]

accounts = [
    {"username": "pembeli", "password": "pembeli1"},
    {"username": "bannedperson", "password": "yessir"},
]

adminaccounts = [
    {"adminusername": "Radit", "adminpassword": "raditiya15240565"},
    {"adminusername": "Tubagus", "adminpassword": "tubagusgus15240157"},
]

superadminaccounts = [
    {"superadminusername": "FajZ", "superadminpassword": "zstleader222"},
    {"superadminusername": "Fauzan", "superadminpassword": "ozan15240092"},
]

def updatehistory(): #Dont ask why its here, it's just there.
    updvers = st.selectbox("Pilih Versi", ["1.0.0", "1.1.0", "1.2.0"])
    if updvers == "1.0.0":
        st.write("Full Release!, nothing else to expect")
    elif updvers == "1.1.0":
        st.write("""- Fitur Daftar/Register! """)
    elif updvers ==  "1.2.0":
        st.write("""- Fitur Support Center! """)
