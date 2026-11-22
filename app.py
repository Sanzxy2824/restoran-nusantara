"""Dashboard Restoran Nusantara - studi kasus portofolio (dataset simulasi). Konsep: kartu menu fine dining."""
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Restoran Nusantara", page_icon="🍽️", layout="wide")
WINE, GOLD, INK, IVORY, SAND, GREY, OLIVE = "#6B1E2E", "#B08D57", "#2A2420", "#FBF8F3", "#F1EBE0", "#8A8178", "#5E6B3A"
rp = lambda x: f"Rp {x:,.0f}".replace(",", ".")
jt = lambda x: f"Rp {x/1e6:,.1f} jt".replace(",", "X").replace(".", ",").replace("X", ".")
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DAYS_ID = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Inter:wght@400;500;600&display=swap');
.stApp {{background:{IVORY}; color:{INK}; font-family:'Inter',sans-serif;}}
[data-testid="stSidebar"] {{background:{SAND};}}
.stApp h1,.stApp h2,.stApp h3,.stApp label,.stApp p,.stApp span {{color:{INK};}}
span[data-baseweb="tag"] {{background:{WINE} !important;}} span[data-baseweb="tag"] span {{color:#fff !important;}}
.serif {{font-family:'Playfair Display',Georgia,serif;}}
.hero {{background:linear-gradient(135deg,#4E1522,{WINE}); border-radius:4px; padding:34px 38px; min-height:210px;}}
.hero .eyebrow {{color:{GOLD}; letter-spacing:3px; font-size:.72rem; font-weight:600;}}
.hero h1 {{font-family:'Playfair Display',Georgia,serif !important; color:{IVORY} !important; font-size:2.8rem !important; font-weight:500 !important; margin:10px 0 8px !important; padding:0 !important;}}
.hero p {{color:#E6D9C3 !important; margin:0; font-size:1rem; line-height:1.5;}}
.menu {{background:#fff; border:1px solid {GOLD}; outline:1px solid {GOLD}55; outline-offset:4px; padding:22px 26px; min-height:210px;}}
.menu .ch {{text-align:center; letter-spacing:4px; color:{GOLD}; font-size:.72rem; font-weight:600; margin-bottom:10px;}}
.menu .r {{display:flex; align-items:baseline; gap:8px; padding:5px 0;}} .menu .r span {{font-size:.95rem;}}
.menu .r i {{flex:1; border-bottom:1px dotted {GREY};}} .menu .r b {{font-family:'Playfair Display',Georgia,serif; font-size:1.1rem; color:{WINE};}}
.sec {{margin:44px 0 4px; display:flex; align-items:center; gap:14px;}}
.sec .no {{font-family:'Playfair Display',Georgia,serif; color:{GOLD}; font-size:1.1rem;}}
.sec .t {{font-family:'Playfair Display',Georgia,serif; font-size:1.7rem; color:{INK};}}
.sec .l {{flex:1; border-bottom:1px solid {GOLD}88;}}
.q {{color:{GREY}; margin:0 0 16px; font-size:.95rem;}}
.rank {{border:1px solid #D9CFBF; background:#fff; padding:22px 22px 20px; height:100%;}}
.rank.first {{background:{WINE}; border-color:{WINE};}}
.rank .no {{color:{GOLD}; letter-spacing:3px; font-size:.7rem; font-weight:600;}}
.rank .n {{font-family:'Playfair Display',Georgia,serif; font-size:1.45rem; margin:6px 0 2px; color:{INK};}} .rank.first .n {{color:{IVORY};}}
.rank .v {{font-family:'Playfair Display',Georgia,serif; font-size:1.7rem; color:{WINE};}} .rank.first .v {{color:{GOLD};}}
.rank .u {{color:{GREY}; font-size:.85rem;}} .rank.first .u {{color:#E6D9C3;}}
.line {{display:flex; justify-content:space-between; font-size:.95rem; padding-top:12px;}} .line .a {{color:{INK};}} .line .b {{color:{GREY};}}
.bar {{height:3px; background:#E5DCCB; margin-top:5px;}} .bar div {{height:3px; background:{GOLD};}}
.dp {{background:#fff; border:1px solid #D9CFBF; border-top:3px solid #D9CFBF; padding:18px 20px;}} .dp.top {{border-top-color:{WINE};}}
.dp .t {{color:{GREY}; letter-spacing:2px; font-size:.72rem; font-weight:600; text-transform:uppercase;}}
.dp .v {{font-family:'Playfair Display',Georgia,serif; font-size:2rem; color:{WINE};}} .dp .s {{color:{GREY}; font-size:.85rem;}}
.say {{background:{SAND}; border-left:3px solid {GOLD}; padding:12px 18px; margin:14px 0; font-size:.97rem; line-height:1.55;}}
</style>""", unsafe_allow_html=True)


@st.cache_data
def load(path="data/restoran_nusantara_sales_raw.csv"):
    df = pd.read_csv(path).drop_duplicates(subset="transaction_id").copy()
    df["payment_method"] = df["payment_method"].fillna("Unknown")
    df["date"] = pd.to_datetime(df["date"])
    df["hour"] = df["time"].str[:2].astype(int)
    df["day_name"] = df["date"].dt.day_name()
    df["slot"] = pd.cut(df["hour"], [9, 14, 17, 23], labels=["Siang · 10–14", "Sore · 15–17", "Malam · 18–22"])
    return df


def fmt(fig, h=380):
    fig.update_layout(height=h, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=10, b=10),
                      font=dict(color=INK, size=13, family="Inter, sans-serif"), showlegend=False)
    fig.update_xaxes(showgrid=False, linecolor="#D9CFBF"); fig.update_yaxes(gridcolor="#E9E1D2", zeroline=False)
    return fig


def section(no, t, q):
    st.markdown(f'<div class="sec"><span class="no">{no}</span><span class="t">{t}</span><span class="l"></span></div><div class="q">{q}</div>', unsafe_allow_html=True)


def say(t):
    st.markdown(f'<div class="say">{t}</div>', unsafe_allow_html=True)


def line(a, b, ratio):
    st.markdown(f'<div class="line"><span class="a">{a}</span><span class="b">{b}</span></div><div class="bar"><div style="width:{ratio*100:.0f}%"></div></div>', unsafe_allow_html=True)


df = load()
with st.expander("Atur filter · tanggal, kategori, tipe pesanan"):
    c1, c2, c3 = st.columns(3)
    d0, d1 = df["date"].min().date(), df["date"].max().date()
    dr = c1.date_input("Rentang tanggal", (d0, d1), min_value=d0, max_value=d1)
    cats = c2.multiselect("Kategori", sorted(df["category"].unique()), default=sorted(df["category"].unique()))
    ords = c3.multiselect("Tipe pesanan", sorted(df["order_type"].unique()), default=sorted(df["order_type"].unique()))
if len(dr) != 2:
    st.info("Pilih tanggal awal dan akhir."); st.stop()
f = df[df["date"].between(pd.Timestamp(dr[0]), pd.Timestamp(dr[1])) & df["category"].isin(cats) & df["order_type"].isin(ords)]
if f.empty:
    st.warning("Tidak ada data untuk filter ini."); st.stop()

a, b = st.columns([3, 2])
with a:
    st.markdown('<div class="hero"><div class="eyebrow">STUDI KASUS · DATASET SIMULASI</div><h1>Restoran Nusantara</h1><p>Menu mana yang menjadi bintang, kapan restoran paling ramai, dan apakah diskon benar-benar berhasil. Januari – Juni 2026.</p></div>', unsafe_allow_html=True)
with b:
    top_menu = f.groupby("product")["quantity"].sum().idxmax()
    st.markdown(f"""<div class="menu"><div class="ch">RINGKASAN</div>
    <div class="r"><span>Total pendapatan</span><i></i><b>{jt(f['total_amount'].sum())}</b></div>
    <div class="r"><span>Jumlah transaksi</span><i></i><b>{str(f'{len(f):,}').replace(',', '.')}</b></div>
    <div class="r"><span>Rata-rata per transaksi</span><i></i><b>{rp(f['total_amount'].mean())}</b></div>
    <div class="r"><span>Diskon diberikan</span><i></i><b>{rp(f['discount_amount'].sum())}</b></div>
    <div class="r"><span>Menu paling laris</span><i></i><b>{top_menu}</b></div></div>""", unsafe_allow_html=True)

prod = f.groupby(["product", "category"], as_index=False).agg(pendapatan=("total_amount", "sum"), unit=("quantity", "sum"), harga=("unit_price", "mean")).sort_values("pendapatan", ascending=False).reset_index(drop=True)

section("I", "Peringkat Menu", "Menu mana yang menyumbang pendapatan terbesar.")
cols = st.columns(3)
for i, col in enumerate(cols):
    r = prod.iloc[i]
    col.markdown(f'<div class="rank {"first" if i == 0 else ""}"><div class="no">NO. {i+1}</div><div class="n">{r["product"]}</div><div class="v">{jt(r["pendapatan"])}</div><div class="u">{int(r["unit"])} porsi terjual</div></div>', unsafe_allow_html=True)
mx = prod["pendapatan"].max()
for i, r in prod.iloc[3:10].iterrows():
    line(f"{i+1:02d} &nbsp; {r['product']}", f"{jt(r['pendapatan'])} &nbsp;·&nbsp; {int(r['unit'])} porsi", r["pendapatan"] / mx)

section("II", "Peta Menu", "Menu mana yang dipertahankan, dipromosikan, atau dievaluasi.")
mu, mp = prod["unit"].median(), prod["harga"].median()
def kuad(r):
    if r["unit"] >= mu and r["harga"] >= mp: return "Bintang"
    if r["unit"] >= mu: return "Penarik pembeli"
    if r["harga"] >= mp: return "Perlu dipromosikan"
    return "Evaluasi"
prod["kelompok"] = prod.apply(kuad, axis=1)
fig = px.scatter(prod, x="unit", y="harga", size="pendapatan", color="kelompok", text="product", size_max=44, opacity=0.9,
                 color_discrete_map={"Bintang": OLIVE, "Penarik pembeli": GOLD, "Perlu dipromosikan": WINE, "Evaluasi": "#A79F94"},
                 labels={"unit": "Porsi terjual (makin ke kanan makin laris)", "harga": "Harga per porsi (Rp)", "kelompok": ""})
fig.update_traces(textposition="top center", marker=dict(line=dict(width=0))); fig.add_vline(x=mu, line_dash="dot", line_color=GREY); fig.add_hline(y=mp, line_dash="dot", line_color=GREY)
fig = fmt(fig, 500); fig.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.18, title=None))
st.plotly_chart(fig, width="stretch")
st.caption("Garis titik-titik menunjukkan nilai tengah. Harga dipakai sebagai pengganti margin karena data tidak memuat biaya bahan.")
g = prod.groupby("kelompok")["product"].apply(lambda s: ", ".join(s)).to_dict()
say(f"<b>Bintang</b> (laris dan harga tinggi): {g.get('Bintang', '-')}.<br><b>Penarik pembeli</b> (laris, harga rendah, cocok untuk paket bundling): {g.get('Penarik pembeli', '-')}.<br><b>Perlu dipromosikan</b> (harga tinggi, kurang laris): {g.get('Perlu dipromosikan', '-')}.")

section("III", "Waktu Makan", "Kapan restoran paling ramai, dan seberapa merata.")
sl = f.groupby("slot", observed=True).agg(n=("transaction_id", "size"), tiket=("total_amount", "mean")).reset_index()
topslot = sl.sort_values("n").iloc[-1]["slot"]
cols = st.columns(3)
for col, (_, r) in zip(cols, sl.iterrows()):
    col.markdown(f'<div class="dp {"top" if r["slot"] == topslot else ""}"><div class="t">{r["slot"]}</div><div class="v">{int(r["n"])}</div><div class="s">transaksi · {r["n"]/len(f)*100:.0f}% · rata-rata {rp(r["tiket"])}</div></div>', unsafe_allow_html=True)
st.write("")
a, b = st.columns(2)
h = f.groupby("hour", as_index=False).size()
with a:
    st.markdown("**Transaksi per jam**")
    fig = px.area(h, x="hour", y="size", color_discrete_sequence=[WINE], labels={"hour": "Jam", "size": "Transaksi"}); fig.update_traces(line=dict(width=2), fillcolor="rgba(107,30,46,.15)")
    st.plotly_chart(fmt(fig, 300), width="stretch")
with b:
    st.markdown("**Transaksi per hari**")
    d = f.groupby("day_name", as_index=False).size().set_index("day_name").reindex(DAYS).reset_index(); d["hari"] = DAYS_ID
    fig = px.bar(d, x="hari", y="size", text="size", color_discrete_sequence=[GOLD], labels={"hari": "", "size": "Transaksi"}); fig.update_traces(textposition="outside")
    st.plotly_chart(fmt(fig, 300), width="stretch")
say(f"Jam tersibuk adalah <b>{int(h.loc[h['size'].idxmax(), 'hour'])}.00</b>. Keramaian cukup merata dari jam 10 sampai 22, sehingga jumlah staf perlu stabil sepanjang hari.")

section("IV", "Cara Pesan dan Bayar", "Lewat apa pelanggan memesan dan membayar. Klik kotak untuk memperbesar.")
tm = f.groupby(["order_type", "payment_method"], as_index=False)["total_amount"].sum()
fig = px.treemap(tm, path=["order_type", "payment_method"], values="total_amount", color="order_type", color_discrete_sequence=[WINE, GOLD, "#7A6F63"])
fig.update_traces(textinfo="label+percent parent", textfont=dict(color="#fff")); st.plotly_chart(fmt(fig, 360), width="stretch")

section("V", "Efektivitas Diskon", "Jika diskon diberikan, apakah pelanggan membeli lebih banyak porsi.")
ds = f.groupby("discount_rate").agg(n=("transaction_id", "size"), porsi=("quantity", "mean")).reset_index(); ds["label"] = (ds["discount_rate"] * 100).round(0).astype(int).astype(str) + "%"
a, b = st.columns([3, 2])
with a:
    st.markdown("**Rata-rata porsi per transaksi, menurut besar diskon**")
    fig = px.bar(ds, x="label", y="porsi", text=ds["porsi"].round(2), color_discrete_sequence=[WINE], labels={"label": "Besar diskon", "porsi": "Porsi"})
    fig.update_traces(textposition="outside"); fig.update_yaxes(range=[0, max(3, ds["porsi"].max() * 1.3)])
    st.plotly_chart(fmt(fig, 320), width="stretch")
with b:
    st.markdown("**Seberapa sering diskon dipakai**")
    for _, r in ds.iterrows():
        line(f"Diskon {r['label']}", f"{r['n']/ds['n'].sum()*100:.0f}% transaksi", r["n"] / ds["n"].max())
say(f"Rata-rata porsi per transaksi nyaris sama di semua level diskon ({ds['porsi'].min():.2f} sampai {ds['porsi'].max():.2f}). Total diskon {rp(f['discount_amount'].sum())} belum terbukti menambah pembelian.")

with st.expander("Lihat data transaksi"):
    st.dataframe(f.drop(columns=["hour", "day_name", "slot"]), width="stretch")
