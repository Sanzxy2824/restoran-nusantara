"""Dashboard Streamlit - studi kasus portofolio (dataset simulasi)."""
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Restoran Nusantara Dashboard", page_icon="🍛", layout="wide")

C1, C2, DARK, SOFT, BG = "#9C3D1E", "#E0A458", "#4A1D0E", "#F6E3CC", "#FFF8F0"
PALETTE = ["#9C3D1E", "#E0A458", "#C46B3C", "#F0CFA0", "#4A1D0E", "#7A3A20"]
DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
rupiah = lambda x: f"Rp {x:,.0f}".replace(",", ".")
num = lambda x: f"{x:,.0f}".replace(",", ".")

st.markdown(f"""
<style>
.block-container {{padding-top: 1.5rem;}}
.hero {{background: linear-gradient(135deg, {DARK} 0%, {C1} 100%); color: #fff;
        padding: 28px 32px; border-radius: 18px; margin-bottom: 18px;}}
.hero h1 {{color:#fff; margin:0; font-size: 2rem;}}
.hero p {{color:{SOFT}; margin:6px 0 0 0;}}
.kpi {{background:#fff; border-radius:16px; padding:18px 20px; border-left:6px solid {C2};
       box-shadow:0 2px 10px rgba(0,0,0,.10);}}
.kpi .label {{font-size:.85rem; color:{C1}; font-weight:600;}}
.kpi .value {{font-size:1.55rem; font-weight:800; color:{DARK}; white-space:nowrap;}}
.insight {{background:{SOFT}; border-radius:12px; padding:12px 16px; margin:8px 0 16px 0; color:{DARK};}}
h3 {{color:{C1};}}
</style>
""", unsafe_allow_html=True)


def style(fig, h=360):
    fig.update_layout(height=h, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color=DARK), margin=dict(l=10, r=10, t=10, b=10), legend_title_text="")
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(0,0,0,.08)")
    return fig


def kpi(col, label, value):
    col.markdown(f'<div class="kpi"><div class="label">{label}</div><div class="value">{value}</div></div>',
                 unsafe_allow_html=True)


def insight(text):
    st.markdown(f'<div class="insight">💡 {text}</div>', unsafe_allow_html=True)


def show(fig, h=360):
    st.plotly_chart(style(fig, h), width="stretch")


def hero(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)


@st.cache_data
def load_data(path="data/restoran_nusantara_sales_raw.csv"):
    df = pd.read_csv(path)
    df = df.drop_duplicates(subset="transaction_id").copy()
    df["payment_method"] = df["payment_method"].fillna("Unknown")
    df["date"] = pd.to_datetime(df["date"])
    df["hour"] = df["time"].str[:2].astype(int)
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["day_name"] = df["date"].dt.day_name()
    return df


df = load_data()
st.sidebar.markdown("## 🍛 Filter")
d_min, d_max = df["date"].min().date(), df["date"].max().date()
date_range = st.sidebar.date_input("Rentang tanggal", (d_min, d_max), min_value=d_min, max_value=d_max)
all_cats, all_orders = sorted(df["category"].unique()), sorted(df["order_type"].unique())
cats = st.sidebar.multiselect("Kategori", all_cats, default=all_cats)
orders = st.sidebar.multiselect("Tipe pesanan", all_orders, default=all_orders)
st.sidebar.caption("Studi kasus portofolio · dataset simulasi\nDibuat oleh Ihsan Amiruddin")
if len(date_range) != 2:
    st.info("Pilih tanggal awal dan akhir."); st.stop()
f = df[df["date"].between(pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]))
       & df["category"].isin(cats) & df["order_type"].isin(orders)]
if f.empty:
    st.warning("Tidak ada data untuk filter ini."); st.stop()

hero("🍛 Restoran Nusantara · Sales Dashboard", "Analisis penjualan Januari–Juni 2026 · studi kasus dengan dataset simulasi")
k = st.columns(4)
kpi(k[0], "💰 Total Pendapatan", rupiah(f["total_amount"].sum()))
kpi(k[1], "🧾 Jumlah Transaksi", num(len(f)))
kpi(k[2], "🛒 Rata-rata / Transaksi", rupiah(f["total_amount"].mean()))
kpi(k[3], "🏷️ Total Diskon", rupiah(f["discount_amount"].sum()))
st.write("")
t1, t2, t3, t4 = st.tabs(["📈 Tren", "🍽️ Menu", "⏰ Jam Ramai", "💳 Pembayaran & Pesanan"])

with t1:
    a, b = st.columns(2)
    with a:
        st.subheader("Pendapatan Bulanan")
        m = f.groupby("month", as_index=False)["total_amount"].sum()
        fig = px.bar(m, x="month", y="total_amount", text_auto=".3s", color_discrete_sequence=[C1],
                     labels={"month": "", "total_amount": "Pendapatan (Rp)"})
        fig.update_traces(marker_cornerradius=8); show(fig)
    with b:
        st.subheader("Pendapatan Harian")
        d = f.groupby("date", as_index=False)["total_amount"].sum().rename(columns={"total_amount": "Harian"})
        d["Rata-rata 7 hari"] = d["Harian"].rolling(7).mean()
        show(px.line(d, x="date", y=["Harian", "Rata-rata 7 hari"], color_discrete_sequence=[C2, C1], labels={"value": "Rp", "date": ""}))
    insight("Pendapatan tertinggi terjadi di bulan Mei; Februari, April, dan Juni relatif lebih rendah.")

with t2:
    prod = f.groupby("product", as_index=False).agg(pendapatan=("total_amount", "sum"), terjual=("quantity", "sum"))
    a, b = st.columns([3, 2])
    with a:
        st.subheader("Pendapatan per Menu")
        t = prod.sort_values("pendapatan")
        fig = px.bar(t, x="pendapatan", y="product", orientation="h", text_auto=".3s", color="pendapatan",
                     color_continuous_scale=[SOFT, DARK], labels={"product": "", "pendapatan": "Pendapatan (Rp)"})
        fig.update_layout(coloraxis_showscale=False); show(fig, 470)
    with b:
        st.subheader("Kontribusi Kategori")
        cat = f.groupby("category", as_index=False)["total_amount"].sum()
        fig = px.pie(cat, names="category", values="total_amount", hole=0.5, color_discrete_sequence=PALETTE)
        fig.update_traces(textinfo="percent+label"); show(fig, 470)
    st.subheader("Unit Terjual vs Pendapatan")
    show(px.scatter(prod, x="terjual", y="pendapatan", text="product", size="pendapatan", color_discrete_sequence=[C1],
                    labels={"terjual": "Unit terjual", "pendapatan": "Pendapatan (Rp)"}).update_traces(textposition="top center"), 420)
    top = prod.nlargest(1, "pendapatan").iloc[0]
    insight(f"Menu dengan pendapatan tertinggi: <b>{top['product']}</b> ({rupiah(top['pendapatan'])}). Menu murah seperti Es Teh Manis laku banyak tetapi kontribusi rupiahnya kecil.")

with t3:
    a, b = st.columns(2)
    with a:
        st.subheader("Transaksi per Jam")
        h = f.groupby("hour", as_index=False).size()
        fig = px.bar(h, x="hour", y="size", color_discrete_sequence=[C1], labels={"hour": "Jam", "size": "Transaksi"})
        fig.update_traces(marker_cornerradius=6); show(fig)
    with b:
        st.subheader("Heatmap Hari × Jam")
        hm = f.pivot_table(index="day_name", columns="hour", values="transaction_id", aggfunc="count", fill_value=0).reindex(DAY_ORDER)
        show(px.imshow(hm, aspect="auto", color_continuous_scale=[BG, C2, DARK], labels={"x": "Jam", "y": "", "color": "Transaksi"}))
    peak = f.groupby("hour").size().idxmax()
    insight(f"Jam dengan transaksi terbanyak: <b>{peak}.00</b>. Pola ramainya cukup merata sepanjang hari, sehingga penjadwalan staf bisa lebih fleksibel.")

with t4:
    a, b = st.columns(2)
    with a:
        st.subheader("Metode Pembayaran")
        p = f.groupby("payment_method", as_index=False).size()
        fig = px.pie(p, names="payment_method", values="size", hole=0.5, color_discrete_sequence=PALETTE)
        fig.update_traces(textinfo="percent+label"); show(fig)
    with b:
        st.subheader("Pendapatan per Tipe Pesanan")
        o = f.groupby("order_type", as_index=False)["total_amount"].sum()
        fig = px.bar(o, x="order_type", y="total_amount", text_auto=".3s", color_discrete_sequence=[C2],
                     labels={"order_type": "", "total_amount": "Pendapatan (Rp)"})
        fig.update_traces(marker_cornerradius=8); show(fig)

with st.expander("📋 Lihat data transaksi"):
    st.dataframe(f.drop(columns=["hour", "month", "day_name"]), width="stretch")
