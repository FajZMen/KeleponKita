import streamlit as st
import PIL as Image
import pandas as pd
import openpyxl as xl
import datetime
from io import BytesIO
from random import randint as rng
from time import sleep as wait
from Data.Datas import accounts, adminaccounts, superadminaccounts, bannedaccounts, accountscreated, produk, vouchers, historypesananlist, adminchathistory, supporthistory

def getstates():
    if "loggedin" not in st.session_state:
        st.session_state.loggedin = False
    if "adminloggedin" not in st.session_state:
        st.session_state.adminloggedin = False
    if "superadminlogin" not in st.session_state:
        st.session_state.superadminlogin = False
    if "banned" not in st.session_state:
        st.session_state.banned = False
    if "databankaccess" not in st.session_state:
        st.session_state.databankaccess = False
    if "keranjang" not in st.session_state:
        st.session_state.keranjang = []
    if "total_harga" not in st.session_state:
        st.session_state.total_harga = 0
    if "diskon" not in st.session_state:
        st.session_state.diskon = 0
    if "historypesanan" not in st.session_state:
        st.session_state.historypesanan = []
    if "stok" not in st.session_state:
        st.session_state.stok = {  # Inisialisasi stok produk
            "Kelepon": 50,
            "Mochi": 50,
    }
        
def login(username, password):
    for banacc in bannedaccounts:
        if banacc["username"] == username:
            st.session_state["banned"] = True
            st.session_state["displayname"] = username
            st.session_state["bannedreason"] = banacc["reason"]
            st.rerun()
            return
    for account in accounts:
        if account["username"] == username and account["password"] == password:
            st.session_state["loggedin"] = True
            st.session_state["displayname"] = username
            st.session_state["Role"] = "User"
            st.rerun()
            return
    for adminaccount in adminaccounts:
        if adminaccount["adminusername"] == username and adminaccount["adminpassword"] == password:
            st.session_state["adminloggedin"] = True
            st.session_state["displayname"] = username
            st.session_state["Role"] = "Admin"
            st.rerun()
            return
    for spadminacc in superadminaccounts:
        if spadminacc["superadminusername"] == username and spadminacc["superadminpassword"] == password:
            st.session_state["superadminlogin"] = True
            st.session_state["displayname"] = username
            st.session_state["Role"] = "Developer"
            st.rerun()
            return
    else:
        st.error("Username atau password salah.")

def register():
    st.title("Register")
    regname = st.text_input("Nama akun")
    regpass = st.text_input("Password akun", type="password")
    if st.button("Register"):
        if not regname or not regpass:
            st.error("Username dan password harus diisi!")
        else:
            for exacc in accounts:
                if exacc["username"] == regname:
                    st.error("Username sudah ada, mohon gunakan Username yang lain!")
                    break

                else:
                    accounts.append({"username": regname, "password": regpass})
                    st.success("Akun berhasil dibuat!")
                    wait(1)
                    st.rerun()

def tambah_ke_keranjang(nama, harga, jumlah, stok):
    if jumlah > 0 and jumlah <= stok:
        st.session_state.keranjang.append({"Nama": nama, "Harga": harga, "Jumlah": jumlah, "Subtotal": jumlah * harga})
        st.session_state.stok[nama] -= jumlah  # Kurangi stok sementara
        st.success(f"{nama} berhasil ditambahkan ke keranjang!")
    elif jumlah > stok:
        st.error(f"Jumlah melebihi stok tersedia ({stok}).")
    else:
        st.error("Jumlah harus lebih dari 0.")

def katalogfunc():
    for amount in produk:
        col1, col2, col3 = st.columns([1, 3, 2])
        stok = st.session_state.stok[amount["Nama"]]  # Dapatkan stok terkini
        
        with col1:
            st.image(f"Images/{amount["Gambar"]}", use_container_width=True)
        with col2:
            st.subheader(amount["Nama"])
            st.write(f"Harga: Rp {amount['Harga']:,}")
            st.write(f"Stok: {stok}")
        with col3:
            if stok > 0:
                jumlah = st.number_input(f"Jumlah untuk {amount['Nama']}", min_value=0, max_value=stok, step=1, key=amount["Nama"])
                if st.button(f"Tambah {amount['Nama']}", key=f"btn-{amount['Nama']}"):
                    tambah_ke_keranjang(nama=amount["Nama"], harga=amount["Harga"], jumlah=jumlah, stok=stok)
            else:
                st.error("Stok habis!")

def keranjangfunc():
    if st.session_state.keranjang:
        total_harga = sum(item["Subtotal"] for item in st.session_state.keranjang)
        st.session_state.total_harga = total_harga

        st.write("List Produk")
        for idx, item in enumerate(st.session_state.keranjang):
            st.write(f"{idx+1}. {item['Nama']} - {item['Jumlah']} x Rp {item['Harga']:,} = Rp {item['Subtotal']:,}")
        
        emailuser = st.text_input("Email:", placeholder="Masukan email anda")
        nohp = st.text_input("No. Hp:", placeholder="Masukan nomor HP/Whatsapp anda")
        alamatuser = st.text_input("Alamat:", placeholder="Masukan alamat anda")
        metodepembayaran = st.selectbox("Metode Pembayaran:", ["Transfer Bank", "Dana", "Gopay"], placeholder="Pilih metode pembayaran")
        
        voucher = st.text_input("Masukkan kode voucher (opsional):")
        hargadiskon = total_harga
        if st.button("Gunakan Voucher"):
            for vc in vouchers:
                if voucher == vc["kode"]:
                    st.session_state.diskon = vc["diskon"]
                    diskonvalue = total_harga * (st.session_state.diskon / 100)
                    hargadiskon = total_harga - diskonvalue
                    st.success(vc["Annouce"])
                    break
            else:
                st.error("Voucher tidak valid.")
        
        st.markdown("### Total Harga")
        st.write(f"Rp {hargadiskon:,}")
        st.warning("Pastikan alamat, nomor HP, dan email sudah benar!. Jika terlihat salah satu dari Info tersebut tidak normal, maka pesanan tersebut akan dibatalkan.")

        if st.button("Beli"):
            st.success("Pesanan sudah dibuat!, mohon tunggu info dari Admin")
            historypesanan(emailuser, nohp, alamatuser, namaproduk=[item["Nama"] for item in st.session_state.keranjang], jumlah=[item["Jumlah"] for item in st.session_state.keranjang], totalharga=hargadiskon, metodepembayaran=metodepembayaran)
    
    else:
        st.write("Keranjang kosong.")

def historypesanan(emailuser, nohp, alamatuser, metodepembayaran, namaproduk, jumlah, totalharga):
    historypesananlist.append({
        "ID": rng(100, 999),
        "Tanggal": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Email": emailuser,
        "No. Hp": nohp,
        "Alamat": alamatuser,
        "Nama Produk": namaproduk,
        "Jumlah": jumlah,
        "Total Harga": totalharga,
        "Metode Pembayaran": metodepembayaran
    })

def historydelete():
    if historypesananlist:
        historyid = st.number_input("Masukkan ID Pesanan yang akan dihapus", min_value=100, max_value=999)
        if st.button("Hapus Pesanan"):
            for hist in historypesananlist:
                if hist["ID"] == historyid:
                    historypesananlist.remove(hist)
                    st.success("History pesanan berhasil dihapus!")
                    wait(1)
                    st.rerun()
                    break
            else:
                st.error("ID Pesanan tidak ditemukan.")
    else:
        st.warning("Belum ada Pesanan")

def downloadlist():
    listfile = BytesIO()
    pd.DataFrame(historypesananlist).to_excel(listfile, index=False)
    listfile.seek(0)

    st.download_button(
        label = "Download List Pesanan",
        data = listfile.getvalue(),
        file_name = "ListPesanan.xlsx",
        mime = "application/vnd.ms-excel"
        )

def vouchermaker():
    kode = st.text_input("Kode Voucher:")
    diskon = st.number_input("Diskon (%):", min_value=0, max_value=100, step=1)
    Annouce = st.text_input("Announcement:")

    if st.button("Aktifkan Voucher"):
        vouchers.append({"kode": kode, "diskon": diskon, "Annouce": Annouce})
        st.success("Voucher berhasil dibuat!")
    
    st.write("Active Vouchers")
    if vouchers:
        st.dataframe(vouchers)
    else:
        st.warning("Belum ada voucher yang aktif.")

def voucherdeleter():
    vouchertarget = st.text_input("Kode Voucher yang akan dihapus")
    if st.button("Hapus Voucher"):
        for vcs in vouchers:
            if vouchertarget == vcs["kode"]:
                vouchers.remove(vcs)
                st.success("Voucher berhasil dihapus!")
                break
        else:
            st.error("Voucher tidak ditemukan.")

    st.write("Active Vouchers")
    if vouchers:
        st.dataframe(vouchers)
    else:
        st.write("Belum ada Voucher yg aktif")
    
def adminchat():
    adminmessage = st.chat_input("Chat here")
    if st.button("Refresh Chat"):
        st.rerun()
    if adminmessage:
        adminchathistory.append({f"Tanggal": {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, "Role": {st.session_state["Role"]}, "Admin": {st.session_state.displayname}, "Message": adminmessage})

def accountbank():
    selectedlist = st.selectbox("Account List", ["User Accounts", "Admin Accounts", "Super Admin Accounts"])
    if selectedlist == "User Accounts":
        st.dataframe(accounts)
    elif selectedlist == "Admin Accounts":
        st.dataframe(adminaccounts)
    elif selectedlist == "Super Admin Accounts":
        st.dataframe(superadminaccounts)
    else:
        st.write("Nothing to show")

def accountcreatortool(userinput, passinput, selectedtype):
    if selectedtype == "User Account":
        accounts.append({"username": userinput, "password": passinput})
        st.success("Account created!")
    elif selectedtype == "Admin Account":
        adminaccounts.append({"adminusername": userinput, "adminpassword": passinput})
        st.success("Admin Account created!")
    else:
        st.write("You didnt select the account type bruh")

def accountdeletortool(deluserinput, delselectedtype):
    if delselectedtype == "User Account":
        for user in accounts:
            if deluserinput == user["username"]:
                accounts.remove(user)
                st.success("User Account deleted!")
                break
        else:
            st.error("User Account not found!")
    elif delselectedtype == "Admin Account":
        for auser in adminaccounts:
            if deluserinput == "Radit" or deluserinput == "Tubagus":
                st.error("This Account cannot be Deleted!")
                break

            elif deluserinput == auser["adminusername"]:
                adminaccounts.remove(auser)
                st.success("Admin Account deleted!")
                break
        else:
            st.error("Admin Account not found!")
    else:
        st.write("You didnt select the account type bruh")

def customersupport():
    supportchat = st.chat_input("Report bugs, Ask Help, or anything here")
    if supportchat:
        supporthistory.append({f"ID" : rng(1, 9999), "Tanggal": {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, "Role": {st.session_state["Role"]}, "User": {st.session_state.displayname}, "Message": supportchat})

def deletesupportreport():
    if supporthistory:
        reportid = st.number_input("Masukkan ID Report yang akan dihapus", min_value=1, max_value=9999)
        if st.button("Hapus Report"):
            for rpd in supporthistory:
                if rpd["ID"] == reportid:
                    supporthistory.remove(rpd)
                    st.success("Report berhasil dihapus!")
                    wait(1)
                    st.rerun()
                    break
            else:
                st.error("ID Report tidak ditemukan.")
        if st.button("Clear History Support Center"):
            supporthistory.clear()
            st.rerun()
    else:
        st.warning("Belum ada Report")

def banaccounts(banuserinput, reason):
    for acctoban in accounts:
        if banuserinput == acctoban["username"]:
            bannedaccounts.append({"username": banuserinput, "reason": reason})
            st.success("Account Banned!")
            break
    else:
        st.error("Account not found.")

def unbanaccount(unbanuserinput):
    for unban in bannedaccounts:
        if unbanuserinput == unban["username"]:
            bannedaccounts.remove(unban)
            st.success("Account Unbanned!")
            break
    else:
        st.error("Account not found.")

def stockeditor(nama): #Not Done
    st.title("Stock Editor")
    selecstok = st.selectbox("Pilih Produk", ["Kelepon", "Thing"])
    if selecstok == "Kelepon":
        st.write(f"Stock Left: {st.session_state.stok[nama]}")
    if selecstok == "Thing":
        st.write("bruh")
    
    if selecstok:
        st.number_input(f"Edit Stock untuk {selecstok}", min_value=0, step=1, key=f"stok-{selecstok}")
        if st.button(f"Edit {selecstok}"):
            st.write("Ok")
    
    st.warning("NOTE: This feature is still in BETA, May not work as intended!.") 

def aboutusinfo(): #Not used for now XD
    st.title("About Us")
    abouttabs = st.tabs(["Tentang Kami", "Members"])
    with abouttabs[0]:
        st.write("KeleponKita adalah sebuah platform yang menyediakan berbagai macam kebutuhan sehari-hari. KeleponKita memiliki berbagai macam produk yang")
    with abouttabs[1]:
        st.image("Images/KeleponKita.png")
