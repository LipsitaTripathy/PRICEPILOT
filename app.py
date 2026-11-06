import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from datetime import date, datetime
import pandas as pd
import plotly.express as px
import requests
import os

# ============================================================
# PRICEPILOT 3.0 | Retail Intelligence Workspace
# ============================================================
st.set_page_config(
    page_title="PRICEPILOT | Retail Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "retail_inventory.csv"
CSS_PATH = BASE_DIR / "assets" / "style.css"
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
BG, TEAL, TEXT = "#080D18", "#35D6C0", "#F4F7FC"
VERSION = "3.0"

# The sound is intentionally user-triggered. Browsers block autoplay audio.
INTRO_HTML = r"""
<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 50% 35%,#172c43 0%,#0b1424 48%,#080d18 100%);font-family:Arial,sans-serif;color:#f4f7fc}
.wrap{height:430px;display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden;position:relative}
.grid{position:absolute;inset:0;background-image:linear-gradient(#8ca8c015 1px,transparent 1px),linear-gradient(90deg,#8ca8c015 1px,transparent 1px);background-size:42px 42px;mask-image:linear-gradient(transparent,#000,transparent)}
.robot{position:relative;width:124px;height:108px;border-radius:34px;background:linear-gradient(145deg,#e5f7f7,#9ebcc9);box-shadow:0 0 55px #35d6c055,inset -8px -10px 20px #7895a8;animation:bob 2.5s ease-in-out infinite;z-index:2}
.robot:before{content:"";position:absolute;width:74px;height:48px;left:25px;top:24px;border-radius:19px;background:#10243a;box-shadow:inset 0 0 14px #071321}
.eye{position:absolute;top:41px;width:11px;height:14px;border-radius:50%;background:#56f5dc;box-shadow:0 0 14px #35d6c0;z-index:3;animation:blink 4s infinite}
.e1{left:45px}.e2{right:45px}.mouth{position:absolute;z-index:3;top:67px;left:53px;width:18px;height:4px;border-radius:8px;background:#7196a9}
.antenna{position:absolute;top:-20px;left:59px;width:6px;height:22px;background:#9ebcc9;border-radius:6px}.antenna:after{content:"";position:absolute;top:-7px;left:-4px;width:14px;height:14px;background:#35d6c0;border-radius:50%;box-shadow:0 0 15px #35d6c0}
.ear{position:absolute;top:40px;width:12px;height:30px;border-radius:8px;background:#7694a9}.ear.l{left:-9px}.ear.r{right:-9px}
.chart{display:flex;align-items:end;gap:7px;height:55px;margin-top:28px;z-index:2}.bar{width:12px;border-radius:5px 5px 2px 2px;background:linear-gradient(#9b8cff,#35d6c0);animation:grow 1.3s ease-in-out infinite alternate}.bar:nth-child(1){height:18px}.bar:nth-child(2){height:30px;animation-delay:.15s}.bar:nth-child(3){height:24px;animation-delay:.3s}.bar:nth-child(4){height:45px;animation-delay:.45s}.bar:nth-child(5){height:37px;animation-delay:.6s}
.brand{margin-top:22px;font-size:clamp(27px,5vw,43px);font-weight:800;letter-spacing:5px;opacity:0;animation:reveal .8s ease 2.5s forwards;z-index:2}.brand span{color:#35d6c0}.tag{font-size:12px;letter-spacing:2px;color:#9aacc4;margin-top:9px;opacity:0;animation:reveal .8s ease 3.25s forwards;z-index:2;text-align:center}
.sound{position:absolute;right:18px;top:15px;background:#17283d;border:1px solid #38516c;color:#d8e6f4;padding:9px 13px;border-radius:20px;cursor:pointer;font-size:12px;z-index:5}
@keyframes bob{0%,100%{transform:translateY(0) rotate(-2deg)}50%{transform:translateY(-12px) rotate(2deg)}}
@keyframes blink{0%,46%,50%,100%{transform:scaleY(1)}48%{transform:scaleY(.12)}}
@keyframes grow{to{filter:brightness(1.5);transform:scaleY(.7);transform-origin:bottom}}
@keyframes reveal{to{opacity:1;transform:translateY(0)}}
</style></head><body><div class="wrap"><div class="grid"></div>
<button class="sound" id="sound">♫ Enable intro sound</button>
<div class="robot"><div class="antenna"></div><div class="ear l"></div><div class="ear r"></div><div class="eye e1"></div><div class="eye e2"></div><div class="mouth"></div></div>
<div class="chart"><i class="bar"></i><i class="bar"></i><i class="bar"></i><i class="bar"></i><i class="bar"></i></div>
<div class="brand">PRICE<span>PILOT</span></div><div class="tag">PREDICT DEMAND · OPTIMIZE PRICING · DRIVE INTELLIGENCE</div>
</div><script>
document.getElementById('sound').addEventListener('click',function(){
 try{const C=window.AudioContext||window.webkitAudioContext;const c=new C();[440,660,880].forEach((f,i)=>{const o=c.createOscillator(),g=c.createGain();o.type='sine';o.frequency.value=f;g.gain.setValueAtTime(.0001,c.currentTime+i*.18);g.gain.exponentialRampToValueAtTime(.07,c.currentTime+i*.18+.04);g.gain.exponentialRampToValueAtTime(.0001,c.currentTime+i*.18+.28);o.connect(g);g.connect(c.destination);o.start(c.currentTime+i*.18);o.stop(c.currentTime+i*.18+.3)});this.textContent='♫ Sound enabled';}catch(e){this.textContent='Sound unavailable';}
});
</script></body></html>
"""

# Load the user's theme stylesheet.
if CSS_PATH.exists():
    st.markdown(f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

# Remove legacy V2 inline green overrides; add structural components.
st.markdown("""
<style>
:root{--pp-teal:#35D6C0}
.block-container{padding-top:1.65rem;max-width:1580px}
.pp-eyebrow{color:#35D6C0;font-size:11px;font-weight:800;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px}
.pp-title{font-size:34px;font-weight:800;letter-spacing:-1.5px;color:#F4F7FC;margin:0}
.pp-subtitle{color:#91A2BB;font-size:14px;margin-top:7px}
.pp-panel{background:linear-gradient(145deg,rgba(22,36,58,.92),rgba(13,23,39,.92));border:1px solid rgba(148,171,205,.15);border-radius:16px;padding:18px 20px}
.pp-chip{display:inline-block;padding:5px 10px;border:1px solid rgba(53,214,192,.25);border-radius:30px;color:#8fe8dc;background:rgba(53,214,192,.07);font-size:11px;font-weight:700;letter-spacing:.5px}
.pp-footer{text-align:center;border-top:1px solid rgba(148,171,205,.14);padding:22px 0 5px;color:#91A2BB;font-size:12px}
.stButton>button,.stDownloadButton>button,[data-testid="stFormSubmitButton"]>button{min-height:46px;height:auto;padding:11px 18px;white-space:normal;line-height:1.35;color:#061A20!important;font-weight:800!important}
.stButton>button p,.stDownloadButton>button p,.stButton>button span,.stDownloadButton>button span{color:#061A20!important;font-weight:800!important;white-space:normal!important;line-height:1.35!important}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2{font-size:24px}
/* Minimal navigation control: replace the old stacked radio-button menu */
[data-testid="stSidebar"] [data-testid="stSelectbox"]{margin-top:10px}
[data-testid="stSidebar"] [data-testid="stSelectbox"] label{color:#91A2BB;font-size:10px;font-weight:800;letter-spacing:1.8px;text-transform:uppercase}
[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"]>div{background:linear-gradient(135deg,#142238,#101b2c);border:1px solid rgba(53,214,192,.28);border-radius:12px;min-height:48px;box-shadow:0 5px 18px rgba(0,0,0,.16)}
[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] *{color:#F4F7FC}
[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] svg{fill:#35D6C0}
</style>
""", unsafe_allow_html=True)

# Animated first-run welcome. Audio is optional and requires a click.
if "pp_intro_complete" not in st.session_state:
    st.session_state.pp_intro_complete = False

if not st.session_state.pp_intro_complete:
    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
    components.html(INTRO_HTML, height=445, scrolling=False)
    _, center, _ = st.columns([1, 1.3, 1])
    with center:
        if st.button("LAUNCH PRICEPILOT  →", type="primary", use_container_width=True, key="pp_launch"):
            st.session_state.pp_intro_complete = True
            st.rerun()
        st.caption("Your retail intelligence workspace is ready.")
    st.stop()

# ============================================================
# DATA + API
# ============================================================
@st.cache_data
def load_retail_data():
    df = pd.read_csv(DATA_PATH)
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

try:
    retail_data = load_retail_data()
    data_available, data_error = True, None
except Exception as error:
    retail_data, data_available, data_error = pd.DataFrame(), False, str(error)

def check_api_health():
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        return response.json() if response.status_code == 200 else None
    except (requests.RequestException, ValueError):
        return None

def check_endpoint(path):
    try:
        response = requests.get(f"{API_URL}{path}", timeout=3)
        return {
            "status": "Online" if response.status_code == 200 else "Needs Attention",
            "http_code": response.status_code,
            "response_time": response.elapsed.total_seconds() * 1000,
            "details": "Successfully responded" if response.status_code == 200 else f"HTTP {response.status_code}"
        }
    except requests.RequestException as error:
        return {"status": "Offline", "http_code": "N/A", "response_time": None, "details": str(error)}

def check_openapi_routes():
    try:
        response = requests.get(f"{API_URL}/openapi.json", timeout=5)
        return response.json().get("paths", {}) if response.status_code == 200 else {}
    except (requests.RequestException, ValueError):
        return {}

api_health = check_api_health()

def style_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT, family="DM Sans"),
        margin=dict(l=15, r=15, t=48, b=15),
        title=dict(font=dict(size=16, color=TEXT)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#B9C7D9")),
        xaxis=dict(gridcolor="rgba(145,162,187,.12)", zerolinecolor="rgba(145,162,187,.2)"),
        yaxis=dict(gridcolor="rgba(145,162,187,.12)", zerolinecolor="rgba(145,162,187,.2)")
    )
    return fig

def download_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def section(title, subtitle=None):
    st.markdown(f"<div class='pp-eyebrow'>PRICEPILOT WORKSPACE</div><h2 style='margin:0'>{title}</h2>", unsafe_allow_html=True)
    if subtitle:
        st.caption(subtitle)

def page_header(title, subtitle, tag):
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap;margin:4px 0 22px">
      <div><div class="pp-eyebrow">{tag}</div><div class="pp-title">{title}</div><div class="pp-subtitle">{subtitle}</div></div>
      <div class="pp-chip">● LIVE WORKSPACE</div>
    </div>""", unsafe_allow_html=True)

PAGES = [
    "Overview", "Demand Forecasting", "Dynamic Pricing",
    "Competitor Analysis", "Model Performance", "Data Quality",
    "API & System Health"
]
ICONS = ["▦", "⌁", "◇", "◎", "▤", "✓", "⌘"]

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="padding:8px 4px 18px">
      <div style="font-size:25px;font-weight:900;letter-spacing:-1px;color:#F4F7FC">◈ PRICE<span style="color:#35D6C0">PILOT</span></div>
      <div style="font-size:10px;letter-spacing:2px;color:#91A2BB;margin-top:5px">RETAIL INTELLIGENCE PLATFORM</div>
    </div>""", unsafe_allow_html=True)
    st.divider()
    st.markdown("<div class='pp-eyebrow'>WORKSPACE</div>", unsafe_allow_html=True)
    page = st.selectbox(
        "NAVIGATE TO",
        PAGES,
        format_func=lambda value: f"{ICONS[PAGES.index(value)]}   {value}",
        label_visibility="visible",
        key="pp_page_navigation"
    )
    st.divider()
    st.markdown("<div class='pp-eyebrow'>SYSTEM MONITOR</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-size:12px;color:{'#65DDBD' if data_available else '#FF7185'}'>● Dataset {'Loaded' if data_available else 'Unavailable'}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='font-size:12px;color:{'#65DDBD' if api_health else '#FF7185'};margin-top:8px'>● FastAPI {'Connected' if api_health else 'Offline'}</div>",
        unsafe_allow_html=True
    )
    st.divider()
    st.caption(f"PRICEPILOT {VERSION} · BUILD 03.0")
    if st.button("Replay introduction", use_container_width=True):
        st.session_state.pp_intro_complete = False
        st.rerun()

# ============================================================
# GLOBAL HEADER
# ============================================================
st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:18px">
 <div><div class="pp-eyebrow">RETAIL ANALYTICS / DECISION SUPPORT</div><div style="font-size:13px;color:#91A2BB">Your command center for demand forecasting and pricing scenarios</div></div>
 <div class="pp-chip">◉ SYSTEM MONITORED</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 1. OVERVIEW
# ============================================================
if page == "Overview":
    page_header("Executive Overview", "A consolidated view of retail activity, demand signals and store performance.", "01 / BUSINESS OVERVIEW")
    if not data_available:
        st.error(f"Dataset unavailable: {data_error}")
    else:
        f1, f2, f3 = st.columns([1.4, 1, 1])
        min_date, max_date = retail_data["Date"].min().date(), retail_data["Date"].max().date()
        with f1:
            selected_dates = st.date_input("Analysis period", value=(min_date, max_date), min_value=min_date, max_value=max_date, key="overview_dates")
        with f2:
            store_filter = st.selectbox("Store", ["All Stores"] + sorted(retail_data["Store ID"].astype(str).unique()), key="overview_store")
        with f3:
            category_filter = st.selectbox("Category", ["All Categories"] + sorted(retail_data["Category"].dropna().unique()), key="overview_category")
        filtered_data = retail_data.copy()
        if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
            start_date, end_date = selected_dates
            filtered_data = filtered_data[(filtered_data["Date"].dt.date >= start_date) & (filtered_data["Date"].dt.date <= end_date)]
        if store_filter != "All Stores":
            filtered_data = filtered_data[filtered_data["Store ID"].astype(str) == store_filter]
        if category_filter != "All Categories":
            filtered_data = filtered_data[filtered_data["Category"] == category_filter]
        if filtered_data.empty:
            st.warning("No records found for the selected filters.")
        else:
            total_records = len(filtered_data)
            total_units = filtered_data["Units Sold"].sum()
            total_demand = filtered_data["Demand"].sum()
            average_price = filtered_data["Price"].mean()
            estimated_sales = (filtered_data["Units Sold"] * filtered_data["Price"]).sum()
            average_daily_demand = filtered_data.groupby("Date")["Demand"].sum().mean()
            total_products = filtered_data["Product ID"].nunique()
            total_stores = filtered_data["Store ID"].nunique()
            section("Performance snapshot", "Key indicators update with the selected filters.")
            kpis = [
                ("UNITS SOLD", f"{total_units:,.0f}"),
                ("ESTIMATED SALES VALUE", f"₹{estimated_sales:,.0f}"),
                ("TOTAL DEMAND", f"{total_demand:,.0f}"),
                ("AVERAGE PRICE", f"₹{average_price:,.2f}"),
                ("DATASET RECORDS", f"{total_records:,}"),
                ("PRODUCTS", f"{total_products:,}"),
                ("ACTIVE STORES", f"{total_stores:,}"),
                ("AVG. DAILY DEMAND", f"{average_daily_demand:,.0f}")
            ]
            for row in range(2):
                cols = st.columns(4)
                for col, (label, value) in zip(cols, kpis[row*4:(row+1)*4]):
                    col.metric(label, value)
            st.divider()
            daily = filtered_data.groupby("Date", as_index=False).agg({"Units Sold": "sum", "Demand": "sum"}).sort_values("Date")
            daily_long = daily.melt(id_vars=["Date"], value_vars=["Units Sold", "Demand"], var_name="Metric", value_name="Units")
            trend = px.line(daily_long, x="Date", y="Units", color="Metric", template="plotly_dark", color_discrete_sequence=[TEAL, "#9B8CFF"], title="Daily units sold vs. recorded demand")
            trend.update_layout(hovermode="x unified", xaxis_title="Date", yaxis_title="Units")
            st.plotly_chart(style_chart(trend), use_container_width=True)
            category_data = filtered_data.groupby("Category", as_index=False).agg({"Units Sold": "sum", "Demand": "sum"}).sort_values("Units Sold", ascending=False)
            left, right = st.columns(2)
            with left:
                fig = px.pie(category_data, names="Category", values="Units Sold", hole=.62, template="plotly_dark", title="Sales mix by category", color_discrete_sequence=[TEAL, "#9B8CFF", "#C5F36B", "#F5BE67", "#6FA8FF"])
                st.plotly_chart(style_chart(fig), use_container_width=True)
            with right:
                fig = px.bar(category_data.sort_values("Demand"), x="Demand", y="Category", orientation="h", template="plotly_dark", title="Demand by category", color="Demand", color_continuous_scale=["#243B55", TEAL])
                st.plotly_chart(style_chart(fig), use_container_width=True)
            product_data = filtered_data.groupby(["Product ID", "Category"], as_index=False).agg({"Units Sold": "sum", "Demand": "sum", "Price": "mean"}).sort_values("Units Sold", ascending=False).head(10)
            fig = px.bar(product_data.sort_values("Units Sold"), x="Units Sold", y="Product ID", color="Category", orientation="h", template="plotly_dark", title="Top 10 products by units sold")
            st.plotly_chart(style_chart(fig), use_container_width=True)
            st.dataframe(product_data.rename(columns={"Product ID":"Product","Units Sold":"Total Units Sold","Demand":"Total Demand","Price":"Average Price"}), use_container_width=True, hide_index=True)
            store_data = filtered_data.groupby("Store ID", as_index=False).agg({"Units Sold":"sum","Demand":"sum"}).sort_values("Units Sold", ascending=False)
            fig = px.bar(store_data, x="Store ID", y="Units Sold", color="Units Sold", template="plotly_dark", title="Store performance", color_continuous_scale=["#243B55", TEAL])
            st.plotly_chart(style_chart(fig), use_container_width=True)
            st.dataframe(store_data.rename(columns={"Store ID":"Store","Units Sold":"Total Units Sold","Demand":"Total Demand"}), use_container_width=True, hide_index=True)
            best_product, best_category, best_store = product_data.iloc[0], category_data.iloc[0], store_data.iloc[0]
            a, b = st.columns(2)
            with a:
                st.success(f"Top product: {best_product['Product ID']} — {best_product['Units Sold']:,.0f} units sold.")
                st.info(f"Leading category: {best_category['Category']} — {best_category['Units Sold']:,.0f} units sold.")
            with b:
                st.success(f"Leading store: {best_store['Store ID']} — {best_store['Units Sold']:,.0f} units sold.")
                st.info(f"Demand minus units sold: {total_demand-total_units:,.0f} units. This is descriptive, not confirmed lost sales.")
            with st.expander("Explore filtered source records"):
                st.dataframe(filtered_data.head(100), use_container_width=True, hide_index=True)
            st.download_button("↓  Download filtered retail data", download_csv(filtered_data), "pricepilot_filtered_retail_data.csv", "text/csv")
            st.caption("Synthetic retail dataset. Estimated sales value is Units Sold × Price, not verified accounting revenue.")

# ============================================================
# 2. DEMAND FORECASTING
# ============================================================
elif page == "Demand Forecasting":
    page_header("Demand Forecasting", "Generate a product-level demand estimate through the FastAPI inference service.", "02 / PREDICTIVE INTELLIGENCE")
    if not data_available:
        st.error(f"Could not load dataset: {data_error}")
    elif not api_health:
        st.error("FastAPI is offline. Start the backend in a separate terminal.")
        st.code("python -m uvicorn api.main:app --reload --log-level debug")
    else:
        st.success("Inference service connected.")
        c1, c2 = st.columns(2)
        with c1:
            stores = sorted(retail_data["Store ID"].astype(str).unique())
            selected_store = st.selectbox("Store", stores, key="forecast_store")
        with c2:
            products = sorted(retail_data[retail_data["Store ID"].astype(str) == selected_store]["Product ID"].astype(str).unique())
            selected_product = st.selectbox("Product", products, key="forecast_product")
        forecast_date = st.date_input("Forecast date", value=date(2024,1,31), min_value=date(2022,4,1), max_value=date(2100,12,31), key="forecast_date")
        st.caption("Historical demand and calendar features are calculated automatically by the API.")
        if st.button("Generate demand forecast  →", type="primary", use_container_width=True, key="generate_forecast"):
            payload = {"store_id":selected_store,"product_id":selected_product,"forecast_date":forecast_date.isoformat()}
            try:
                with st.spinner("Generating demand prediction…"):
                    response = requests.post(f"{API_URL}/predict", json=payload, timeout=30)
                if response.status_code == 200:
                    st.session_state["latest_forecast"] = response.json()
                    st.success("Prediction generated.")
                else:
                    try: detail = response.json().get("detail", response.text)
                    except ValueError: detail = response.text
                    st.error(f"API error {response.status_code}: {detail}")
            except requests.RequestException as error:
                st.error(f"Could not connect to API: {error}")
        result = st.session_state.get("latest_forecast")
        if result:
            predicted_demand = float(result.get("predicted_demand",0))
            unit = result.get("unit","units")
            st.divider()
            c1,c2,c3 = st.columns(3)
            c1.metric("PREDICTED DEMAND",f"{predicted_demand:,.2f} {unit}")
            c2.metric("STORE",result.get("store_id","N/A"))
            c3.metric("PRODUCT",result.get("product_id","N/A"))
            details = {"Product ID":result.get("product_id"),"Store ID":result.get("store_id"),"Forecast Date":result.get("forecast_date"),"Predicted Demand":predicted_demand,"Unit":unit,"Prediction Model":result.get("model"),"Historical Features":result.get("historical_features","Automatically calculated")}
            st.dataframe(pd.DataFrame({"Parameter":list(details.keys()),"Result":list(details.values())}),use_container_width=True,hide_index=True)
            fig = px.bar(pd.DataFrame({"Metric":["Predicted Demand"],"Units":[predicted_demand]}),x="Metric",y="Units",text="Units",template="plotly_dark",title="Predicted product demand")
            fig.update_traces(marker_color=TEAL,texttemplate="%{text:.2f}",textposition="outside")
            st.plotly_chart(style_chart(fig),use_container_width=True)
            st.download_button("↓  Download forecast result",download_csv(pd.DataFrame([details])),"pricepilot_forecast.csv","text/csv")
            st.caption("Single-date model prediction; an estimate, not a guaranteed future sales figure.")

# ============================================================
# 3. DYNAMIC PRICING
# ============================================================
elif page == "Dynamic Pricing":
    page_header("Dynamic Pricing Engine", "Compare candidate prices using demand scenarios, estimated costs and margin constraints.", "03 / PRICING INTELLIGENCE")
    if not data_available:
        st.error(f"Dataset unavailable: {data_error}")
    elif not api_health:
        st.error("FastAPI is offline. Start the backend first.")
        st.code("python -m uvicorn api.main:app --reload")
    elif not api_health.get("pricing_model_available",False):
        st.error("The pricing demand model is not available in the API.")
    else:
        st.success("Pricing API connected · LightGBM pricing demand model available")
        st.markdown("#### Product configuration")
        c1,c2 = st.columns(2)
        with c1:
            pricing_store = st.selectbox("Store",sorted(retail_data["Store ID"].astype(str).unique()),key="pricing_store")
        store_rows = retail_data[retail_data["Store ID"].astype(str)==pricing_store]
        with c2:
            pricing_product = st.selectbox("Product",sorted(store_rows["Product ID"].astype(str).unique()),key="pricing_product")
        history = store_rows[store_rows["Product ID"].astype(str)==pricing_product].sort_values("Date")
        current_price = float(history.iloc[-1]["Price"])
        competitor_price = float(history.iloc[-1]["Competitor Pricing"])
        latest_date = history.iloc[-1]["Date"].date()
        c1,c2,c3=st.columns(3)
        c1.metric("CURRENT DATASET PRICE",f"₹{current_price:,.2f}")
        c2.metric("RECORDED COMPETITOR PRICE",f"₹{competitor_price:,.2f}")
        c3.metric("LATEST RECORD",latest_date.strftime("%d %b %Y"))
        st.divider()
        st.markdown("#### Scenario assumptions")
        a,b=st.columns(2)
        with a:
            cost_percentage=st.slider("Estimated unit cost (% of current price)",50,90,70,5)/100
            minimum_margin=st.slider("Minimum profit margin",0,40,10,5)/100
        with b:
            max_price_change=st.slider("Maximum price change",5,20,10,5)/100
            elasticity=st.number_input("Demand elasticity assumption",min_value=-3.0,max_value=-0.1,value=-1.0,step=.1,help="Manual scenario assumption, not a causal elasticity learned from observational data.")
        st.info("Unit cost is estimated as a percentage of current price. Elasticity is manually specified for scenario simulation. Verify assumptions before business use.")
        pricing_date=st.date_input("Scenario date",value=date(2024,1,31),min_value=date(2022,4,1),max_value=date(2100,12,31),key="pricing_date")
        if st.button("Evaluate pricing scenarios  →",type="primary",use_container_width=True):
            payload={"store_id":pricing_store,"product_id":pricing_product,"forecast_date":pricing_date.isoformat(),"cost_percentage":cost_percentage,"minimum_margin":minimum_margin,"max_price_change":max_price_change,"price_elasticity":float(elasticity)}
            try:
                with st.spinner("Evaluating candidate prices and demand scenarios…"):
                    response=requests.post(f"{API_URL}/pricing/recommend",json=payload,timeout=60)
                if response.status_code==200:
                    st.session_state["latest_pricing_recommendation"]=response.json()
                    st.success("Pricing scenario completed.")
                else:
                    try: detail=response.json().get("detail",response.text)
                    except ValueError: detail=response.text
                    st.error(f"Pricing API error ({response.status_code}): {detail}")
            except requests.RequestException as error:
                st.error(f"Could not connect to pricing API: {error}")
        result=st.session_state.get("latest_pricing_recommendation")
        if result:
            recommendation=result.get("recommendation",{})
            candidates=recommendation.get("candidate_results",result.get("candidate_results",[]))
            if recommendation:
                st.divider()
                c1,c2,c3,c4=st.columns(4)
                c1.metric("RECOMMENDED PRICE",f"₹{recommendation.get('recommended_price',0):,.2f}")
                c2.metric("ESTIMATED DEMAND",f"{recommendation.get('predicted_demand',0):,.2f} units")
                c3.metric("ESTIMATED PROFIT",f"₹{recommendation.get('estimated_profit',0):,.2f}")
                c4.metric("ESTIMATED MARGIN",f"{recommendation.get('estimated_margin',0):.2f}%")
                details={"Current Price":recommendation.get("current_price"),"Recommended Price":recommendation.get("recommended_price"),"Baseline Demand":recommendation.get("baseline_demand"),"Predicted Demand":recommendation.get("predicted_demand"),"Estimated Unit Cost":recommendation.get("estimated_unit_cost"),"Estimated Revenue":recommendation.get("estimated_revenue"),"Estimated Profit":recommendation.get("estimated_profit"),"Profit Margin":recommendation.get("estimated_margin"),"Cost Assumption":recommendation.get("cost_assumption"),"Minimum Margin Assumption":recommendation.get("minimum_margin"),"Maximum Price Change":recommendation.get("maximum_price_change"),"Price Elasticity Assumption":recommendation.get("price_elasticity_assumption"),"Boundary Selected":recommendation.get("boundary_selected")}
                st.dataframe(pd.DataFrame({"Parameter":list(details.keys()),"Value":list(details.values())}),use_container_width=True,hide_index=True)
                if recommendation.get("boundary_selected"):
                    st.warning("Selected price is at the allowed price-change boundary. Review assumptions before using it.")
                else:
                    st.success("Selected price is within the permitted scenario range.")
                st.info(recommendation.get("model_note","Demand response is simulated using the selected elasticity assumption."))
                if recommendation.get("recommendation_status"):
                    st.caption(f"Recommendation status: {recommendation['recommendation_status']}")
            if candidates:
                candidate_df=pd.DataFrame(candidates)
                st.divider()
                if {"Candidate Price","Estimated Profit"}.issubset(candidate_df.columns):
                    fig=px.line(candidate_df,x="Candidate Price",y="Estimated Profit",markers=True,template="plotly_dark",title="Estimated profit across candidate prices")
                    fig.update_traces(line_color=TEAL,marker_size=9)
                    st.plotly_chart(style_chart(fig),use_container_width=True)
                if {"Candidate Price","Predicted Demand"}.issubset(candidate_df.columns):
                    fig=px.line(candidate_df,x="Candidate Price",y="Predicted Demand",markers=True,template="plotly_dark",title="Demand response across candidate prices")
                    fig.update_traces(line_color="#9B8CFF",marker_size=9)
                    st.plotly_chart(style_chart(fig),use_container_width=True)
                st.dataframe(candidate_df,use_container_width=True,hide_index=True)
                st.download_button("↓  Download pricing scenario report",download_csv(candidate_df),"pricepilot_pricing_scenarios.csv","text/csv")
            else:
                st.warning("Recommendation returned without candidate scenario details.")
            st.caption("Scenario estimates use synthetic data and explicit assumptions. They do not prove causal price elasticity or guarantee business outcomes.")

# ============================================================
# 4. COMPETITOR ANALYSIS
# ============================================================
elif page == "Competitor Analysis":
    page_header("Competitor Intelligence","Review product-level price positioning and recorded competitor price gaps.","04 / MARKET POSITIONING")
    if not data_available:
        st.error(f"Dataset unavailable: {data_error}")
    else:
        comp=retail_data.groupby(["Product ID","Category"],as_index=False).agg({"Price":"mean","Competitor Pricing":"mean"}).rename(columns={"Price":"Our Price","Competitor Pricing":"Competitor Price"})
        comp["Price Difference"]=comp["Our Price"]-comp["Competitor Price"]
        valid=comp["Competitor Price"].notna()&(comp["Competitor Price"]!=0)
        comp["Difference (%)"]=pd.NA
        comp.loc[valid,"Difference (%)"]=comp.loc[valid,"Price Difference"]/comp.loc[valid,"Competitor Price"]*100
        comp["Market Position"]="Unavailable"
        comp.loc[comp["Price Difference"]<0,"Market Position"]="Cheaper"
        comp.loc[comp["Price Difference"]>0,"Market Position"]="More Expensive"
        comp.loc[comp["Price Difference"]==0,"Market Position"]="Same Price"
        f1,f2=st.columns(2)
        with f1:
            cat=st.selectbox("Category",["All Categories"]+sorted(comp["Category"].dropna().unique()),key="competitor_category")
        with f2:
            pos=st.selectbox("Market position",["All Positions","Cheaper","More Expensive","Same Price","Unavailable"],key="competitor_position")
        filtered=comp.copy()
        if cat!="All Categories": filtered=filtered[filtered["Category"]==cat]
        if pos!="All Positions": filtered=filtered[filtered["Market Position"]==pos]
        if filtered.empty:
            st.warning("No products match the selected filters.")
        else:
            cheaper=int((filtered["Market Position"]=="Cheaper").sum())
            expensive=int((filtered["Market Position"]=="More Expensive").sum())
            same=int((filtered["Market Position"]=="Same Price").sum())
            gap=filtered["Difference (%)"].mean()
            c1,c2,c3,c4=st.columns(4)
            c1.metric("PRODUCTS CHEAPER",cheaper)
            c2.metric("PRODUCTS ABOVE",expensive)
            c3.metric("SAME PRICE",same)
            c4.metric("AVERAGE PRICE GAP",f"{gap:+.2f}%" if pd.notna(gap) else "N/A")
            avg_our,avg_comp=filtered["Our Price"].mean(),filtered["Competitor Price"].mean()
            c1,c2=st.columns(2)
            c1.metric("OUR AVG. PRICE",f"₹{avg_our:,.2f}")
            c2.metric("COMPETITOR AVG. PRICE",f"₹{avg_comp:,.2f}" if pd.notna(avg_comp) else "N/A")
            compare=pd.DataFrame({"Price Type":["Our Average Price","Competitor Average Price"],"Average Price":[avg_our,avg_comp]}).dropna()
            fig=px.bar(compare,x="Price Type",y="Average Price",color="Price Type",text="Average Price",template="plotly_dark",title="Average price positioning",color_discrete_sequence=[TEAL,"#9B8CFF"])
            fig.update_traces(texttemplate="₹%{text:.2f}",textposition="outside")
            fig.update_layout(showlegend=False)
            st.plotly_chart(style_chart(fig),use_container_width=True)
            melted=filtered.melt(id_vars=["Product ID"],value_vars=["Our Price","Competitor Price"],var_name="Price Type",value_name="Price").dropna()
            fig=px.bar(melted,x="Product ID",y="Price",color="Price Type",barmode="group",template="plotly_dark",title="Product price comparison",color_discrete_sequence=[TEAL,"#9B8CFF"])
            st.plotly_chart(style_chart(fig),use_container_width=True)
            gaps=filtered.dropna(subset=["Price Difference"])
            if not gaps.empty:
                fig=px.bar(gaps.sort_values("Price Difference"),x="Product ID",y="Price Difference",color="Market Position",template="plotly_dark",title="Price gap by product",color_discrete_map={"Cheaper":TEAL,"More Expensive":"#FF7185","Same Price":"#F5BE67"},hover_data=["Our Price","Competitor Price","Difference (%)"])
                fig.add_hline(y=0,line_dash="dash",line_color="white")
                st.plotly_chart(style_chart(fig),use_container_width=True)
                high=gaps.loc[gaps["Price Difference"].idxmax()]
                low=gaps.loc[gaps["Price Difference"].idxmin()]
                a,b=st.columns(2)
                a.info(f"Largest positive gap: {high['Product ID']} at ₹{high['Price Difference']:.2f} above competitor average.")
                b.success(f"Lowest gap: {low['Product ID']} at ₹{low['Price Difference']:.2f} relative to competitor average.")
            else:
                st.info("No valid price-gap data is available.")
            st.dataframe(filtered.sort_values("Difference (%)",ascending=False,na_position="last").round(2),use_container_width=True,hide_index=True)
            st.download_button("↓  Download competitor analysis",download_csv(filtered),"pricepilot_competitor_analysis.csv","text/csv",use_container_width=True)
            st.caption("Competitor prices are synthetic observations from the supplied dataset, not live market prices. These descriptive comparisons do not establish optimal pricing or profitability.")

# ============================================================
# 5. MODEL PERFORMANCE
# ============================================================
elif page == "Model Performance":
    page_header("Model Performance","Review chronological test-set metrics for demand forecasting and pricing demand models.","05 / MODEL EVALUATION")
    model_path=BASE_DIR/"models"/"pricing_model_performance.csv"
    demand_models=pd.DataFrame({"Model":["XGBoost","LightGBM"],"MAE":[31.201,31.405],"RMSE":[39.780,40.002],"R² Score":[.1914,.1823]})
    best_mae=demand_models.loc[demand_models["MAE"].idxmin()]
    best_rmse=demand_models.loc[demand_models["RMSE"].idxmin()]
    best_r2=demand_models.loc[demand_models["R² Score"].idxmax()]
    c1,c2,c3,c4=st.columns(4)
    c1.metric("MODELS EVALUATED",len(demand_models))
    c2.metric("BEST MAE",f"{best_mae['MAE']:.3f}",best_mae["Model"])
    c3.metric("BEST RMSE",f"{best_rmse['RMSE']:.3f}",best_rmse["Model"])
    c4.metric("BEST R²",f"{best_r2['R² Score']:.4f}",best_r2["Model"])
    st.dataframe(demand_models.style.format({"MAE":"{:.3f}","RMSE":"{:.3f}","R² Score":"{:.4f}"}),use_container_width=True,hide_index=True)
    a,b=st.columns(2)
    with a:
        for metric,title in [("MAE","Mean absolute error"),("RMSE","Root mean squared error")]:
            fig=px.bar(demand_models,x="Model",y=metric,color="Model",text=metric,template="plotly_dark",title=title,color_discrete_sequence=[TEAL,"#9B8CFF"])
            fig.update_traces(textposition="outside")
            st.plotly_chart(style_chart(fig),use_container_width=True)
    with b:
        fig=px.bar(demand_models,x="Model",y="R² Score",color="Model",text="R² Score",template="plotly_dark",title="Coefficient of determination",color_discrete_sequence=[TEAL,"#9B8CFF"])
        fig.update_traces(textposition="outside")
        fig.update_layout(yaxis_range=[0,1])
        st.plotly_chart(style_chart(fig),use_container_width=True)
        st.info("A higher R² indicates more target variation explained by the model. Current demand model scores are modest.")
    st.markdown("#### Evaluation metric guide")
    a,b,c=st.columns(3)
    a.markdown("**MAE**");a.write("Average absolute prediction error. Lower is better.")
    b.markdown("**RMSE**");b.write("Penalizes larger errors more strongly. Lower is better.")
    c.markdown("**R²**");c.write("Explained variation relative to a mean baseline. Higher is generally better.")
    baseline=40.971
    improvement=(baseline-best_mae["MAE"])/baseline*100
    a,b=st.columns(2)
    a.success(f"XGBoost MAE is {best_mae['MAE']:.3f}, about {improvement:.1f}% below the previous-day baseline MAE of {baseline:.3f}.")
    b.warning("XGBoost R² is 0.1914; substantial demand variation remains unexplained.")
    st.caption("The demand evaluation uses a chronological test period. The rolling one-step-ahead setup uses actual prior-day observations for later predictions.")
    st.divider()
    st.markdown("#### Pricing demand model performance")
    if model_path.exists():
        try:
            pricing_models=pd.read_csv(model_path)
            if pricing_models.empty:
                st.warning("Pricing model performance file contains no results.")
            else:
                st.dataframe(pricing_models,use_container_width=True,hide_index=True)
                nums=pricing_models.select_dtypes(include="number").columns.tolist()
                model_col=next((x for x in pricing_models.columns if x.lower() in ["model","model_name"]),None)
                metrics=[x for x in nums if x.lower() in ["mae","rmse","r2","r²","r2 score"]]
                if model_col and metrics:
                    selected=st.selectbox("Pricing evaluation metric",metrics,key="pricing_performance_metric")
                    fig=px.bar(pricing_models,x=model_col,y=selected,color=model_col,text=selected,template="plotly_dark",title=f"Pricing model {selected}")
                    st.plotly_chart(style_chart(fig),use_container_width=True)
        except Exception as error:
            st.error(f"Could not read pricing performance report: {error}")
    else:
        st.warning(f"Pricing model performance report not found: {model_path}")
    pricing_reference=pd.DataFrame({"Model":["LightGBM","XGBoost"],"MAE":[16.166304,21.320515],"RMSE":[22.209424,28.142336],"R² Score":[.747946,.595295]})
    c1,c2,c3=st.columns(3)
    c1.metric("BEST PRICING MAE","16.166","LightGBM")
    c2.metric("BEST PRICING RMSE","22.209","LightGBM")
    c3.metric("BEST PRICING R²","0.7479","LightGBM")
    st.dataframe(pricing_reference.style.format({"MAE":"{:.6f}","RMSE":"{:.6f}","R² Score":"{:.6f}"}),use_container_width=True,hide_index=True)
    demand_export=demand_models.copy();demand_export.insert(0,"Evaluation Type","Demand Forecasting")
    pricing_export=pricing_reference.copy();pricing_export.insert(0,"Evaluation Type","Pricing Demand")
    st.download_button("↓  Download complete model performance report",download_csv(pd.concat([demand_export,pricing_export],ignore_index=True)),"pricepilot_model_performance.csv","text/csv",use_container_width=True)
    st.caption("Pricing predictive accuracy does not establish causal price elasticity or prove that recommendations improve real-world profit.")

# ============================================================
# 6. DATA QUALITY
# ============================================================
elif page == "Data Quality":
    page_header("Data Quality Center","Validate source records, inspect distributions and export quality-control reports.","06 / DATA GOVERNANCE")
    if not data_available:
        st.error(f"Dataset unavailable: {data_error}")
    else:
        df=retail_data.copy()
        rows,cols=len(df),len(df.columns)
        cells=rows*cols
        missing=df.isna().sum()
        total_missing=int(missing.sum())
        duplicates=int(df.duplicated().sum())
        missing_pct=total_missing/cells*100 if cells else 0
        numeric=df.select_dtypes(include="number").columns.tolist()
        negatives=sum(int((df[x]<0).sum()) for x in numeric)
        invalid_price=int((df["Price"]<=0).sum()) if "Price" in df else 0
        invalid_comp=int((df["Competitor Pricing"]<=0).sum()) if "Competitor Pricing" in df else 0
        invalid_dates=int(df["Date"].isna().sum()) if "Date" in df else 0
        checks=pd.DataFrame([
            {"Validation":"Missing values","Issues Found":total_missing,"Description":"Empty or unavailable cell values"},
            {"Validation":"Duplicate records","Issues Found":duplicates,"Description":"Completely duplicated rows"},
            {"Validation":"Negative numeric values","Issues Found":negatives,"Description":"Negative values in numeric columns"},
            {"Validation":"Invalid dates","Issues Found":invalid_dates,"Description":"Date values that could not be interpreted"},
            {"Validation":"Non-positive selling prices","Issues Found":invalid_price,"Description":"Selling prices equal to or below zero"},
            {"Validation":"Non-positive competitor prices","Issues Found":invalid_comp,"Description":"Competitor prices equal to or below zero"}
        ])
        checks["Status"]=checks["Issues Found"].apply(lambda x:"Passed" if x==0 else "Needs Attention")
        passed=int((checks["Issues Found"]==0).sum())
        health=passed/len(checks)*100 if len(checks) else 100
        c1,c2,c3,c4,c5=st.columns(5)
        c1.metric("RECORDS",f"{rows:,}")
        c2.metric("FEATURES",cols)
        c3.metric("MISSING CELLS",f"{total_missing:,}")
        c4.metric("DUPLICATES",f"{duplicates:,}")
        c5.metric("MISSING DATA",f"{missing_pct:.2f}%")
        a,b=st.columns([1,2])
        a.metric("DATASET HEALTH SCORE",f"{health:.1f}%")
        if health==100:a.success("All listed checks passed.")
        elif health>=70:a.warning("Some checks require attention.")
        else:a.error("Several checks require review.")
        fig=px.pie(names=["Passed","Needs Attention"],values=[passed,len(checks)-passed],hole=.65,template="plotly_dark",title="Validation check results",color_discrete_sequence=[TEAL,"#FF7185"])
        b.plotly_chart(style_chart(fig),use_container_width=True)
        st.caption("Score is the share of listed checks with zero detected issues; it is not a measure of overall data accuracy.")
        st.dataframe(checks,use_container_width=True,hide_index=True)
        missing_report=pd.DataFrame({"Column":df.columns,"Missing Values":df.isna().sum().values,"Missing Percentage":(df.isna().mean().values*100).round(2),"Data Type":df.dtypes.astype(str).values}).sort_values("Missing Values",ascending=False)
        st.markdown("#### Missing value analysis")
        missing_nonzero=missing_report[missing_report["Missing Values"]>0]
        if missing_nonzero.empty:st.success("No missing values detected.")
        else:
            fig=px.bar(missing_nonzero,x="Column",y="Missing Values",text="Missing Values",template="plotly_dark",title="Missing values by column",color="Missing Values",color_continuous_scale=["#243B55",TEAL])
            st.plotly_chart(style_chart(fig),use_container_width=True)
        with st.expander("View complete missing-value report"):
            st.dataframe(missing_report,use_container_width=True,hide_index=True)
        profile=pd.DataFrame([{"Column":x,"Data Type":str(df[x].dtype),"Non-Null Values":int(df[x].count()),"Missing Values":int(df[x].isna().sum()),"Unique Values":int(df[x].nunique(dropna=True)),"Missing (%)":round(df[x].isna().mean()*100,2)} for x in df.columns])
        st.markdown("#### Column profiling")
        st.dataframe(profile,use_container_width=True,hide_index=True)
        st.markdown("#### Date and timeline validation")
        if "Date" in df:
            valid_dates=df["Date"].dropna()
            if not valid_dates.empty:
                dmin,dmax=valid_dates.min(),valid_dates.max()
                a,b,c=st.columns(3)
                a.metric("FIRST DATE",dmin.strftime("%d %b %Y"))
                b.metric("LAST DATE",dmax.strftime("%d %b %Y"))
                c.metric("UNIQUE DATES",f"{valid_dates.nunique():,}")
                counts=valid_dates.dt.normalize().value_counts().sort_index()
                expected=pd.date_range(dmin.normalize(),dmax.normalize(),freq="D")
                missing_dates=expected.difference(pd.DatetimeIndex(counts.index))
                a,b=st.columns(2)
                a.metric("EXPECTED CALENDAR DAYS",f"{len(expected):,}")
                b.metric("DATES WITHOUT RECORDS",f"{len(missing_dates):,}")
                timeline=counts.rename("Record Count").reset_index();timeline.columns=["Date","Record Count"]
                fig=px.line(timeline,x="Date",y="Record Count",markers=True,template="plotly_dark",title="Records across timeline")
                fig.update_traces(line_color=TEAL)
                st.plotly_chart(style_chart(fig),use_container_width=True)
                if len(missing_dates):
                    st.warning(f"{len(missing_dates)} calendar dates have no records. This does not prove individual store-product observations are missing.")
                    st.dataframe(pd.DataFrame({"Dates Without Records":missing_dates.strftime("%Y-%m-%d")}),use_container_width=True,hide_index=True)
                else:st.success("Every calendar date in the dataset range has records.")
            else:st.warning("No valid dates available.")
        outlier_rows=[];outlier_indices=set()
        for column in numeric:
            values=pd.to_numeric(df[column],errors="coerce").dropna()
            if len(values)<4:continue
            q1,q3=values.quantile(.25),values.quantile(.75);iqr=q3-q1
            low,high=q1-1.5*iqr,q3+1.5*iqr
            vals=pd.to_numeric(df[column],errors="coerce")
            mask=(vals<low)|(vals>high)
            outlier_rows.append({"Column":column,"Q1":round(q1,3),"Q3":round(q3,3),"IQR":round(iqr,3),"Lower Bound":round(low,3),"Upper Bound":round(high,3),"Potential Outliers":int(mask.sum())})
            outlier_indices.update(df.index[mask].tolist())
        outliers=pd.DataFrame(outlier_rows)
        st.markdown("#### Numeric outlier detection")
        st.caption("IQR flags potential outliers for review; it does not automatically classify them as errors.")
        if not outliers.empty:
            st.metric("POTENTIAL OUTLIER OBSERVATIONS",f"{int(outliers['Potential Outliers'].sum()):,}")
            fig=px.bar(outliers.sort_values("Potential Outliers"),x="Potential Outliers",y="Column",orientation="h",template="plotly_dark",title="Potential outliers by numeric feature",color="Potential Outliers",color_continuous_scale=["#243B55",TEAL])
            st.plotly_chart(style_chart(fig),use_container_width=True)
            st.dataframe(outliers,use_container_width=True,hide_index=True)
            if outlier_indices:
                outlier_records=df.loc[sorted(outlier_indices)].copy()
                with st.expander("Preview records containing potential outliers"):
                    st.dataframe(outlier_records.head(100),use_container_width=True,hide_index=True)
                st.download_button("↓  Download potential outlier records",download_csv(outlier_records),"pricepilot_potential_outliers.csv","text/csv")
        else:
            outlier_total=0;st.info("Not enough numeric data for outlier detection.")
        st.markdown("#### Numeric feature distribution")
        if numeric:
            selected=st.selectbox("Numeric feature",numeric,key="quality_numeric_feature")
            fig=px.histogram(df,x=selected,nbins=35,template="plotly_dark",title=f"Distribution of {selected}",color_discrete_sequence=[TEAL])
            st.plotly_chart(style_chart(fig),use_container_width=True)
            with st.expander("View numeric statistical summary"):
                st.dataframe(df[numeric].describe().T.reset_index().rename(columns={"index":"Feature"}),use_container_width=True,hide_index=True)
        preview=st.select_slider("Rows to preview",options=[10,20,50,100,250],value=50,key="quality_preview_rows")
        st.dataframe(df.head(preview),use_container_width=True,hide_index=True)
        st.caption(f"Showing {min(preview,len(df)):,} of {len(df):,} records.")
        a,b=st.columns(2)
        a.download_button("↓  Download validation report",download_csv(checks),"pricepilot_validation_report.csv","text/csv",use_container_width=True)
        b.download_button("↓  Download column profile",download_csv(profile),"pricepilot_column_profile.csv","text/csv",use_container_width=True)
        full=pd.DataFrame({"Metric":["Total Records","Total Columns","Total Cells","Missing Values","Missing Percentage","Duplicate Rows","Negative Numeric Values","Invalid Dates","Non-Positive Selling Prices","Non-Positive Competitor Prices","Potential Outlier Observations","Validation Checks Passed","Total Validation Checks","Dataset Health Score"],"Value":[rows,cols,cells,total_missing,round(missing_pct,3),duplicates,negatives,invalid_dates,invalid_price,invalid_comp,int(outliers["Potential Outliers"].sum()) if not outliers.empty else 0,passed,len(checks),round(health,2)]})
        st.download_button("↓  Download complete quality summary",download_csv(full),"pricepilot_complete_quality_summary.csv","text/csv",use_container_width=True)
        st.caption("Reports flag detected conditions without modifying the original dataset. Outliers and missing dates require context before being classified as errors.")

# ============================================================
# 7. API & SYSTEM HEALTH
# ============================================================
elif page == "API & System Health":
    page_header("API & System Health","Monitor service connectivity, model availability, registered routes and backend readiness.","07 / PLATFORM MONITORING")
    if st.button("↻  Refresh system status",type="primary",use_container_width=True,key="refresh_system_status"):
        st.rerun()
    root=check_endpoint("/")
    health=check_endpoint("/health")
    paths=check_openapi_routes()
    connected=api_health is not None
    demand_loaded=api_health.get("demand_model_loaded",api_health.get("model_loaded",False)) if api_health else False
    pricing_loaded=api_health.get("pricing_model_available",False) if api_health else False
    backend_data=api_health.get("dataset_loaded",False) if api_health else False
    record_count=api_health.get("total_records","Unknown") if api_health else "Unknown"
    a,b,c,d=st.columns(4)
    a.metric("DASHBOARD","Online")
    b.metric("FASTAPI","Connected" if connected else "Offline")
    c.metric("XGBOOST MODEL","Loaded" if demand_loaded else "Unavailable")
    d.metric("PRICING MODEL","Loaded" if pricing_loaded else "Unavailable")
    a,b,c=st.columns(3)
    a.metric("DASHBOARD DATASET","Loaded" if data_available else "Unavailable")
    b.metric("BACKEND DATASET","Loaded" if backend_data else "Unavailable")
    c.metric("BACKEND RECORDS",f"{record_count:,}" if isinstance(record_count,(int,float)) else str(record_count))
    st.markdown("#### Live endpoint connectivity")
    endpoint_rows=[]
    for method,path,check in [("GET","/",root),("GET","/health",health)]:
        endpoint_rows.append({"Method":method,"Endpoint":path,"Status":check["status"],"HTTP Code":check["http_code"],"Response Time (ms)":round(check["response_time"],2) if check["response_time"] is not None else "N/A","Details":check["details"]})
    st.dataframe(pd.DataFrame(endpoint_rows),use_container_width=True,hide_index=True)
    expected=[("GET","/","API information"),("GET","/health","Service and model health"),("POST","/predict","Demand prediction"),("POST","/pricing/recommend","Scenario-based pricing recommendation")]
    route_rows=[]
    for method,path,purpose in expected:
        registered=method.lower() in paths.get(path,{}).keys() if paths else False
        status="Backend Offline" if not connected else "Documentation Unavailable" if not paths else "Registered - Live Checked" if registered and method=="GET" else "Registered - Not Executed" if registered else "Not Registered"
        route_rows.append({"Method":method,"Endpoint":path,"Purpose":purpose,"Registration Status":status,"Execution Status":"Checked" if method=="GET" else "Not tested"})
    st.markdown("#### Registered API endpoints")
    st.dataframe(pd.DataFrame(route_rows),use_container_width=True,hide_index=True)
    st.caption("GET routes are checked directly. POST routes are verified through OpenAPI documentation and are not executed by this health check.")
    components_status=[
        ("Streamlit Dashboard","Running","Interactive user interface"),
        ("FastAPI Backend","Connected" if connected else "Offline","Prediction and pricing services"),
        ("XGBoost Demand Model","Loaded" if demand_loaded else "Unavailable","Demand forecasting"),
        ("LightGBM Pricing Model","Available" if pricing_loaded else "Unavailable","Pricing demand estimation"),
        ("Pricing Scenario Engine","Available" if pricing_loaded else "Unavailable","Candidate price and profit scenarios"),
        ("Retail Dataset","Loaded" if data_available else "Unavailable","Dashboard retail data"),
        ("Backend Dataset","Loaded" if backend_data else "Unavailable","API prediction data"),
        ("Docker","Not deployed","Planned containerization")
    ]
    st.markdown("#### Backend components")
    st.dataframe(pd.DataFrame(components_status,columns=["Component","Status","Purpose"]),use_container_width=True,hide_index=True)
    checks=[("Streamlit Dashboard",True),("Dashboard Dataset",data_available),("FastAPI Backend",connected),("Root Endpoint",root["status"]=="Online"),("Health Endpoint",health["status"]=="Online"),("XGBoost Model",bool(demand_loaded)),("Pricing Model",bool(pricing_loaded)),("Backend Dataset",bool(backend_data))]
    passed=sum(bool(x[1]) for x in checks);total=len(checks);score=passed/total*100 if total else 0
    a,b=st.columns([1,2])
    a.metric("SYSTEM AVAILABILITY SCORE",f"{score:.1f}%")
    if score==100:a.success("All monitored components are available.")
    elif score>=70:a.warning("Some components need attention.")
    else:a.error("Multiple components are unavailable.")
    b.dataframe(pd.DataFrame([{"System Check":name,"Status":"Online" if ok else "Unavailable"} for name,ok in checks]),use_container_width=True,hide_index=True)
    st.caption("Availability score reflects listed checks at refresh time; it is not prediction accuracy or production uptime.")
    st.markdown("#### System architecture")
    st.code("Retail Dataset → Data Validation → Feature Engineering → XGBoost + LightGBM → Demand Prediction → Pricing Scenario Engine → FastAPI → Streamlit Dashboard → Docker (planned)",language="text")
    report_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report=pd.DataFrame([
        {"Check":"Report Generated","Status":report_time,"Details":"Local dashboard time"},
        {"Check":"Dashboard","Status":"Online","Details":"Streamlit application is running"},
        {"Check":"FastAPI","Status":"Connected" if connected else "Offline","Details":"Backend health endpoint"},
        {"Check":"Root Endpoint","Status":root["status"],"Details":root["details"]},
        {"Check":"Health Endpoint","Status":health["status"],"Details":health["details"]},
        {"Check":"XGBoost Model","Status":"Loaded" if demand_loaded else "Unavailable","Details":"Demand forecasting model"},
        {"Check":"Pricing Model","Status":"Loaded" if pricing_loaded else "Unavailable","Details":"Pricing demand model"},
        {"Check":"Dashboard Dataset","Status":"Loaded" if data_available else "Unavailable","Details":data_error or f"{len(retail_data):,} records"},
        {"Check":"Backend Dataset","Status":"Loaded" if backend_data else "Unavailable","Details":f"{record_count} records reported by API"},
        {"Check":"Docker","Status":"Not deployed","Details":"Containerization is planned"},
        {"Check":"System Availability Score","Status":f"{score:.1f}%","Details":f"{passed}/{total} monitored checks passed"}
    ])
    st.dataframe(report,use_container_width=True,hide_index=True)
    st.download_button("↓  Download system health report",download_csv(report),"pricepilot_system_health_report.csv","text/csv",use_container_width=True)
    if connected:st.success("FastAPI is responding to health checks.")
    else:
        st.warning("FastAPI is offline. Start the backend in a separate terminal.")
        st.code("python -m uvicorn api.main:app --reload --log-level debug")

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="pp-footer">
  <div style="font-weight:800;color:#DCE7F5;letter-spacing:1px">◈ PRICEPILOT</div>
  <div style="margin-top:7px">© 2026 Lipsita Tripathy. All Rights Reserved.</div>
  <div style="margin-top:4px">Designed &amp; Developed by Lipsita Tripathy</div>
  <div style="margin-top:7px;font-size:10px;color:#6F829D">AI-powered retail intelligence · Scenario estimates are decision-support outputs, not guarantees.</div>
</div>
""",unsafe_allow_html=True)
