"""Dashboard Restoran Nusantara - studi kasus portofolio (dataset simulasi). Konsep: struk, papan peringkat, peta menu."""
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Restoran Nusantara", page_icon="🍛", layout="wide")
RED, YEL, INK, PAPER, SOFT, GREEN = "#C62828", "#F9A825", "#2B1B17", "#FFFDF8", "#FFF1D6", "#2E7D32"
rp = lambda x: f"Rp {x:,.0f}".replace(",", ".")
jt = lambda x: f"Rp {x/1e6:,.1f} jt".replace(",", ".")
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DAYS_ID = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
ICON = {"Makanan": "🍛", "Minuman": "🥤", "Snack": "🍟"}

st.markdown(f"""<style>
.stApp {{background:{PAPER}; color:{INK};}}
[data-testid="stSidebar"] {{background:{SOFT};}}
.stApp h1,.stApp h2,.stApp h3,.stApp label,.stApp p {{color:{INK};}}
span[data-baseweb="tag"] {{background:{RED} !important; color:#fff !important;}} span[data-baseweb="tag"] span {{color:#fff !important;}}
.banner {{background:{RED}; border-radius:20px; padding:26px 30px; color:#fff; position:relative; overflow:hidden;}}
.banner h1 {{color:#fff !important; font-size:2.3rem !important; margin:0 !important; padding:0 !important; font-weight:900;}}
.banner p {{color:#FFE9B0 !important; margin:6px 0 0;}}
.banner .tag {{background:{YEL}; color:{INK}; border-radius:999px; padding:2px 12px; font-size:.75rem; font-weight:800;}}
.receipt {{background:#fff; border:2px dashed #B9A68C; border-radius:6px; padding:16px 20px; font-family:'Courier New',monospace; color:{INK}; box-shadow:4px 4px 0 {YEL};}}
.receipt .h {{text-align:center; font-weight:800; letter-spacing:2px;}} .receipt hr {{border:none; border-top:2px dashed #B9A68C; margin:8px 0;}}
.receipt .row {{display:flex; justify-content:space-between; font-size:1rem; padding:2px 0;}} .receipt .big {{font-size:1.25rem; font-weight:800; color:{RED};}}
.sec {{font-size:1.5rem; font-weight:900; color:{INK}; margin:30px 0 2px; border-bottom:4px solid {YEL}; display:inline-block;}}
.q {{color:#6B5A4E; margin:4px 0 12px;}}
.pod {{border-radius:18px; padding:18px; text-align:center; background:{SOFT}; border:2px solid {YEL};}}
.pod.first {{background:{YEL}; border-color:{INK}; transform:scale(1.04);}}
.pod .m {{font-size:2.2rem;}} .pod .n {{font-weight:800; font-size:1.1rem;}} .pod .v {{font-size:1.4rem; font-weight:900; color:{RED};}} .pod.first .v {{color:{INK};}}
.dp {{border-radius:16px; padding:16px; background:#fff; border:2px solid {SOFT}; text-align:center;}} .dp.top {{border-color:{RED}; background:#FFF4F2;}}
.dp .t {{font-weight:800;}} .dp .v {{font-size:1.8rem; font-weight:900; color:{RED};}} .dp .s {{color:#6B5A4E; font-size:.9rem;}}
.say {{background:{SOFT}; border-radius:12px; padding:10px 16px; margin:10px 0; border-left:5px solid {RED};}}
</style>""", unsafe_allow_html=True)


@st.cache_data
def load(path="data/restoran_nusantara_sales_raw.csv"):
    df = pd.read_csv(path).drop_duplicates(subset="transaction_id").copy()
    df["payment_method"] = df["payment_method"].fillna("Unknown")
    df["date"] = pd.to_datetime(df["date"])
    df["hour"] = df["time"].str[:2].astype(int)
    df["day_name"] = df["date"].dt.day_name()
    df["slot"] = pd.cut(df["hour"], [9, 14, 17, 23], labels=["Siang (10–14)", "Sore (15–17)", "Malam (18–22)"])
    return df


def fmt(fig, h=380):
    fig.update_layout(height=h, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=10, b=10), font=dict(color=INK, size=14), showlegend=False)
    return fig


def section(t, q):
    st.markdown(f'<div class="sec">{t}</div><div class="q">{q}</div>', unsafe_allow_html=True)


def say(t):
    st.markdown(f'<div class="say">💬 {t}</div>', unsafe_allow_html=True)


df = load()
with st.expander("🔎 Atur filter (tanggal, kategori, tipe pesanan)"):
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

# ---------- Banner + struk ----------
a, b = st.columns([3, 2])
with a:
    st.markdown('<div class="banner"><span class="tag">STUDI KASUS · DATASET SIMULASI</span><h1>🍛 Restoran Nusantara</h1><p>Menu mana yang jadi bintang, kapan restoran ramai, dan apakah diskon berhasil? Januari–Juni 2026</p></div>', unsafe_allow_html=True)
with b:
    st.markdown(f"""<div class="receipt"><div class="h">STRUK RINGKASAN</div><hr>
    <div class="row"><span>Total pendapatan</span><span class="big">{jt(f['total_amount'].sum())}</span></div>
    <div class="row"><span>Jumlah transaksi</span><span>{len(f):,}</span></div>
    <div class="row"><span>Rata-rata / transaksi</span><span>{rp(f['total_amount'].mean())}</span></div>
    <div class="row"><span>Diskon diberikan</span><span>-{rp(f['discount_amount'].sum())}</span></div><hr>
    <div class="row"><span>Menu terlaris</span><span><b>{f.groupby('product')['quantity'].sum().idxmax()}</b></span></div></div>""".replace(",", "."), unsafe_allow_html=True)

# ---------- Papan peringkat ----------
prod = f.groupby(["product", "category"], as_index=False).agg(pendapatan=("total_amount", "sum"), unit=("quantity", "sum"), harga=("unit_price", "mean")).sort_values("pendapatan", ascending=False).reset_index(drop=True)
section("🏆 Papan Peringkat Menu", "Menu mana yang menyumbang pendapatan terbesar?")
t3 = prod.head(3)
cols = st.columns([1, 1.15, 1])
for col, i, medal, cls in zip(cols, [1, 0, 2], ["🥈", "🥇", "🥉"], ["", "first", ""]):
    r = t3.iloc[i]
    col.markdown(f'<div class="pod {cls}"><div class="m">{medal}</div><div class="n">{r["product"]}</div><div class="v">{jt(r["pendapatan"])}</div><div>{int(r["unit"])} porsi terjual</div></div>', unsafe_allow_html=True)
st.write("")
mx = prod["pendapatan"].max()
for i, r in prod.iloc[3:10].iterrows():
    st.progress(float(r["pendapatan"] / mx), text=f"{i+1}. {ICON.get(r['category'], '')} {r['product']} · {jt(r['pendapatan'])} · {int(r['unit'])} porsi")

# ---------- Peta menu ----------
section("🧭 Peta Menu", "Menu mana yang harus dipromosikan, dipertahankan, atau dievaluasi?")
mu, mp = prod["unit"].median(), prod["harga"].median()
def kuad(r):
    if r["unit"] >= mu and r["harga"] >= mp: return "⭐ Bintang"
    if r["unit"] >= mu: return "🧲 Penarik pembeli"
    if r["harga"] >= mp: return "📣 Perlu dipromosikan"
    return "🔍 Evaluasi"
prod["kelompok"] = prod.apply(kuad, axis=1)
fig = px.scatter(prod, x="unit", y="harga", size="pendapatan", color="kelompok", text="product", size_max=48,
                 color_discrete_map={"⭐ Bintang": GREEN, "🧲 Penarik pembeli": YEL, "📣 Perlu dipromosikan": RED, "🔍 Evaluasi": "#9E9E9E"},
                 labels={"unit": "Porsi terjual (makin ke kanan = makin laris)", "harga": "Harga per porsi (Rp)"})
fig.update_traces(textposition="top center"); fig.add_vline(x=mu, line_dash="dash", line_color="#B9A68C"); fig.add_hline(y=mp, line_dash="dash", line_color="#B9A68C")
fig.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.2, title=None))
st.plotly_chart(fmt(fig, 500).update_layout(showlegend=True), width="stretch")
st.caption("Garis putus-putus = nilai tengah. Harga dipakai sebagai pengganti margin karena data tidak memuat biaya bahan (HPP).")
g = prod.groupby("kelompok")["product"].apply(lambda s: ", ".join(s)).to_dict()
say(f"<b>⭐ Bintang:</b> {g.get('⭐ Bintang', '-')}. <b>🧲 Penarik pembeli:</b> {g.get('🧲 Penarik pembeli', '-')} (cocok untuk paket bundling). <b>📣 Perlu dipromosikan:</b> {g.get('📣 Perlu dipromosikan', '-')}.")

# ---------- Waktu makan ----------
section("🕒 Waktu Makan", "Kapan restoran paling ramai, dan seberapa merata?")
sl = f.groupby("slot", observed=True).agg(n=("transaction_id", "size"), tiket=("total_amount", "mean")).reset_index()
topslot = sl.sort_values("n").iloc[-1]["slot"]
cols = st.columns(3)
for col, (_, r) in zip(cols, sl.iterrows()):
    col.markdown(f'<div class="dp {"top" if r["slot"] == topslot else ""}"><div class="t">{r["slot"]}</div><div class="v">{r["n"]:,}</div><div class="s">transaksi · {r["n"]/len(f)*100:.0f}% · rata-rata {rp(r["tiket"])}</div></div>'.replace(",", "."), unsafe_allow_html=True)
st.write("")
a, b = st.columns(2)
h = f.groupby("hour", as_index=False).size()
with a:
    fig = px.area(h, x="hour", y="size", markers=True, color_discrete_sequence=[RED], labels={"hour": "Jam", "size": "Transaksi"})
    st.plotly_chart(fmt(fig, 320), width="stretch")
with b:
    d = f.groupby("day_name", as_index=False).size().set_index("day_name").reindex(DAYS).reset_index(); d["hari"] = DAYS_ID
    fig = px.bar(d, x="hari", y="size", text="size", color_discrete_sequence=[YEL], labels={"hari": "", "size": "Transaksi"})
    fig.update_traces(textposition="outside", marker_cornerradius=8); st.plotly_chart(fmt(fig, 320), width="stretch")
say(f"Jam tersibuk: <b>{int(h.loc[h['size'].idxmax(), 'hour'])}.00</b>. Pola ramainya cukup merata dari jam 10 sampai 22, jadi staf perlu stabil sepanjang hari.")

# ---------- Cara pesan & bayar ----------
section("🧾 Cara Pesan & Bayar", "Pelanggan memesan dan membayar lewat apa?")
tm = f.groupby(["order_type", "payment_method"], as_index=False)["total_amount"].sum()
fig = px.treemap(tm, path=["order_type", "payment_method"], values="total_amount", color="order_type", color_discrete_sequence=[RED, YEL, "#8D6E63"])
fig.update_traces(textinfo="label+percent parent"); st.plotly_chart(fmt(fig, 380), width="stretch")
st.caption("Ukuran kotak = pendapatan. Klik sebuah kotak untuk memperbesar.")

# ---------- Diskon ----------
section("🏷️ Apakah Diskon Berhasil?", "Kalau diskon diberikan, apakah pelanggan membeli lebih banyak porsi?")
ds = f.groupby("discount_rate").agg(n=("transaction_id", "size"), porsi=("quantity", "mean")).reset_index(); ds["label"] = (ds["discount_rate"] * 100).round(0).astype(int).astype(str) + "%"
a, b = st.columns([3, 2])
with a:
    fig = px.bar(ds, x="label", y="porsi", text=ds["porsi"].round(2), color_discrete_sequence=[RED], labels={"label": "Besar diskon", "porsi": "Rata-rata porsi per transaksi"})
    fig.update_traces(textposition="outside", marker_cornerradius=8); fig.update_yaxes(range=[0, max(3, ds["porsi"].max() * 1.3)])
    st.plotly_chart(fmt(fig, 340), width="stretch")
with b:
    st.markdown("**Seberapa sering diskon dipakai?**")
    for _, r in ds.iterrows():
        st.progress(float(r["n"] / ds["n"].max()), text=f"Diskon {r['label']} · {r['n']/ds['n'].sum()*100:.0f}% transaksi")
say(f"Rata-rata porsi per transaksi nyaris sama di semua level diskon ({ds['porsi'].min():.2f}–{ds['porsi'].max():.2f}). Total diskon {rp(f['discount_amount'].sum())} belum terbukti menambah pembelian.")

with st.expander("📋 Lihat data transaksi"):
    st.dataframe(f.drop(columns=["hour", "day_name", "slot"]), width="stretch")
