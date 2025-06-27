import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

# ---------- CONFIGURE SSL ----------
SSL_CA_PATH = r"C:\Users\Prem Kumar\Desktop\ca.pem"  # ✅ Make sure this file exists

# ---------- CONNECT TO TiDB ----------
def connect_to_tidb():
    try:
        conn = mysql.connector.connect(
            host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
            port=4000,
            user="2PNbtsH752ymVzG.root",
            password="XHN5P4YZljpIsUrv",
            database="project_7",
            ssl_ca=SSL_CA_PATH,
            ssl_verify_cert=False
        )
        return conn
    except Error as e:
        st.error(f"❌ Connection Error: {e}")
        return None

# ---------- QUERIES ----------
QUERY_OPTIONS = {
    "🚌 Cheapest Bus (Low Cost)": 
        "SELECT * FROM bus_data ORDER BY CAST(REPLACE(amount, '₹', '') AS UNSIGNED) ASC LIMIT 1;",

    "💰 Most Expensive Bus (High Price)": 
        "SELECT * FROM bus_data ORDER BY CAST(REPLACE(amount, '₹', '') AS UNSIGNED) DESC LIMIT 1;",

    "🌟 Top 5 Rated Buses (Premium)": 
        "SELECT * FROM bus_data ORDER BY rating DESC LIMIT 5;",

    "🎯 Buses Below ₹1000 (Budget Friendly)": 
        "SELECT * FROM bus_data WHERE CAST(REPLACE(amount, '₹', '') AS UNSIGNED) < 1000;",

    "👍 Buses Rated Above 4.0 (Highly Rated)": 
        "SELECT * FROM bus_data WHERE rating > 4.0;",

    "❄️ A/C Sleeper Buses (Comfort Focus)": 
        "SELECT * FROM bus_data WHERE about LIKE '%A/C Sleeper%';",

    "🪑 Seater Buses": 
        "SELECT * FROM bus_data WHERE about LIKE '%Seater%';",

    "💸 Exact ₹600 Fare Buses (Ultra Budget)": 
        "SELECT * FROM bus_data WHERE amount = '₹600';",

    "📊 Total Buses Available": 
        "SELECT COUNT(*) AS total_buses FROM bus_data;",

    "📉 Average Bus Fare": 
        "SELECT ROUND(AVG(CAST(REPLACE(amount, '₹', '') AS UNSIGNED)), 2) AS avg_fare FROM bus_data;",

    "📋 Count by Bus Type": 
        "SELECT about, COUNT(*) AS count FROM bus_data GROUP BY about ORDER BY count DESC;",

    "🔀 Buses by Rating & Fare": 
        "SELECT * FROM bus_data ORDER BY rating DESC, CAST(REPLACE(amount, '₹', '') AS UNSIGNED) ASC;",

    "🔎 Distinct Service Types": 
        "SELECT DISTINCT about FROM bus_data;",

    "🚍 Buses with 'Travels' in Name": 
        "SELECT * FROM bus_data WHERE bus_name LIKE '%Travels%';",

    "📈 Rating Distribution": 
        "SELECT rating, COUNT(*) AS count FROM bus_data GROUP BY rating ORDER BY rating DESC;"
}

# ---------- QUERY EXECUTION ----------
def run_query(query):
    conn = connect_to_tidb()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            data = cursor.fetchall()
            return pd.DataFrame(data)
        except Error as e:
            st.error(f"❌ Query Error: {e}")
            return pd.DataFrame()
        finally:
            conn.close()
    return pd.DataFrame()

# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="🚌 Bus Explorer", layout="centered", page_icon="🚌")

st.markdown("""
    <style>
    .big-title {
        font-size:36px !important;
        font-weight:700;
        color:#2C3E50;
        text-align: center;
    }
    .subtle {
        font-size: 15px;
        text-align: center;
        color: gray;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🚌 Bus Insights Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtle">Explore pricing, ratings, and bus types using live data from TiDB Cloud</div>', unsafe_allow_html=True)

st.markdown("### 🔍 Select a Query")
query_choice = st.selectbox("", list(QUERY_OPTIONS.keys()), index=0)

if st.button("🚀 Run Query"):
    query = QUERY_OPTIONS[query_choice]
    df = run_query(query)

    if not df.empty:
        st.success("✅ Query executed successfully!")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ No data found or an error occurred.")
