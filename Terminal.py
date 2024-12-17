from time import sleep as wait
import streamlit as st
import pandas as pd
from Functions.Function import sesi_inisilasi, tambah_ke_keranjang, login, katalogfunc, keranjangfunc, historypesanan, downloadlist, historydelete, vouchermaker, voucherdeleter, adminchat, accountbank, accountcreatortool, accountdeletortool, customersupport, deletesupportreport
from Data.Datas import produk, accounts, adminaccounts, superadminaccounts, historypesananlist, vouchers, adminchathistory, supporthistory
sesi_inisilasi()
loggedin = st.session_state.get("loggedin", False)
adminloggedin = st.session_state.get("adminloggedin", False)
superadminlogin = st.session_state.get("superadminlogin", False)
dataaccess = st.session_state.get("databankaccess", False)

if not loggedin and not adminloggedin and not superadminlogin:
    halamanlogin = st.sidebar.radio(
        "Halaman",
        ["Login", "Daftar"]
    )
    
    if halamanlogin == "Login":
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            login(username, password)
    
    if halamanlogin == "Daftar":
        st.title("Daftar")
        st.warning("Fitur ini sedang In Development!")

elif st.session_state.loggedin:
    st.sidebar.title(f"Hello {st.session_state.displayname}!")
    halamanuser = st.sidebar.radio(
        "Halaman User",
        ["Katalog", "Keranjang", "Support"]
    )

    if st.sidebar.button("Logout"):
        st.session_state["loggedin"] = False
        st.rerun()

    if halamanuser == "Katalog":
        st.title("Menu KeleponKita")
        katalogfunc()
    
    if halamanuser == "Keranjang":
        st.title("Keranjang")
        keranjangfunc()

    if halamanuser == "Support":
        st.title("Support Center")
        st.write("Disini, anda bisa meminta bantuan dari admin atau melaporkan Masalah-masalah di web!.")
        customersupport()
        if st.button("Refresh"):
            st.rerun()
        if supporthistory:
            st.dataframe(supporthistory, column_config={"Message": st.column_config.TextColumn(width="large")})

elif st.session_state.adminloggedin:
    st.sidebar.title(f"Selamat Datang Admin {st.session_state.displayname}!")
    halamanadmin = st.sidebar.radio(
        "Halaman Admin",
        ["Pesanan", "Vouchers", "Admin Chat", "Support Center", "Katalog", "Keranjang"]
    )

    if st.sidebar.button("Logout"):
        st.session_state["adminloggedin"] = False
        st.rerun()

    if halamanadmin == "Pesanan":
        st.title("Pesanan")
        pestab = st.tabs(["History Pesanan", "Delete Pesanan"])
        with pestab[0]:
            if historypesananlist:
                st.data_editor(historypesananlist, num_rows="dynamic")
                downloadlist()
            else:
                st.warning("Belum ada pesanan.")
        with pestab[1]:
            historydelete()
    
    if halamanadmin == "Vouchers":
        st.title("Vouchers")
        vtab = st.tabs(["Activate Voucher", "Delete Voucher"])
        with vtab[0]:
            st.write("Active Vouchers")
            vouchermaker()
        with vtab[1]:
            voucherdeleter()

    if halamanadmin == "Admin Chat":
        st.title("Admin Chat")
        adminchat()
        if adminchathistory:
            st.data_editor(adminchathistory, column_config={"Message": st.column_config.TextColumn(width="large")})
        else:
            st.warning("Belum ada chat.")
    
    if halamanadmin == "Support Center":
        st.title("Support Center")
        customersupport()
        if st.button("Refresh"):
            st.rerun()
        if supporthistory:
            st.dataframe(supporthistory, column_config={"Message": st.column_config.TextColumn(width="large")})
        else:
            st.write("Belum ada report.")

    if halamanadmin == "Katalog":
        st.title("Menu KeleponKita")
        katalogfunc()
    
    if halamanadmin == "Keranjang":
        st.title("Keranjang")
        keranjangfunc()

elif st.session_state.superadminlogin:
    st.sidebar.title(f"Selamat Datang Developer {st.session_state.displayname}!")
    halamanspadmin = st.sidebar.radio(
        "Halaman Developer",
        ["Pesanan", "Vouchers", "Admin Chat", "Dev Tools", "Account Bank", "Support Center", "Katalog", "Keranjang"]
    )

    if st.sidebar.button("Logout"):
        st.session_state["superadminlogin"] = False
        st.session_state["databankaccess"] = False
        st.rerun()

    if halamanspadmin == "Pesanan":
        st.title("Pesanan")
        pestab = st.tabs(["History Pesanan", "Delete Pesanan"])
        with pestab[0]:
            if historypesananlist:
                st.data_editor(historypesananlist, num_rows="dynamic")
                downloadlist()
            else:
                st.warning("Belum ada pesanan.")
        with pestab[1]:
            historydelete()
    
    if halamanspadmin == "Vouchers":
        st.title("Vouchers")
        vtab = st.tabs(["Activate Voucher", "Delete Voucher"])
        with vtab[0]:
            vouchermaker()
        with vtab[1]:
            voucherdeleter()

    if halamanspadmin == "Admin Chat":
        st.title("Admin Chat")
        adminchat()
        if adminchathistory:
            st.data_editor(adminchathistory, num_rows="dynamic", column_config={"Message": st.column_config.TextColumn(width="large")})
        else:
            st.warning("Belum ada chat.")
        
        if st.sidebar.button("Clear Chat"):
            adminchathistory.clear()
            st.rerun()

    if halamanspadmin == "Dev Tools":
        tabs = st.tabs(["Account Creator", "Account Deleter"])
        with tabs[0]:
            st.title("Account Creation Tool")
            selectedtype = st.selectbox("Create what Account Type", ["User Account", "Admin Account"])
            userinput = st.text_input("Enter Account Username to Create")
            passinput = st.text_input("Enter the Account Password", type="password")
            if st.button("Create Account"):
                accountcreatortool(userinput, passinput, selectedtype)
            st.warning("NOTICE: Accounts created this way will be DELETED on Website Reboot!")
        with tabs[1]:
            st.title("Account Deletion Tool")
            deluserinput = st.text_input("Enter Account Username to Delete")
            delselectedtype = st.selectbox("What Account Type you trying to delete", ["User Account", "Admin Account"])
            if st.button("Delete Account"):
                accountdeletortool(deluserinput, delselectedtype)

    if halamanspadmin == "Account Bank":
        st.title("Account Databank")
        if "databankaccess" in st.session_state and st.session_state.databankaccess:
            accountbank()
        else:
            st.write("Enter Password to enter")
            sneakypass = st.text_input("Password", type="password")
            if st.button("Enter Databank"):
                if sneakypass == "4202024":
                    st.session_state.databankaccess = True
                    st.rerun()
                else:
                    st.write("Wrong")
        
    if halamanspadmin == "Support Center":
        st.title("Support Center")
        scpage = st.tabs(["Reports", "Delete Reports"])
        with scpage[0]:
            customersupport()
            if st.button("Refresh"):
                st.rerun()
            if supporthistory:
                st.dataframe(supporthistory, column_config={"Message": st.column_config.TextColumn(width="large")})
            else:
                st.write("Belum ada report.")
        with scpage[1]:
            deletesupportreport()

    if halamanspadmin == "Katalog":
        st.title("Menu KeleponKita")
        katalogfunc()
    
    if halamanspadmin == "Keranjang":
        st.title("Keranjang")
        keranjangfunc()
