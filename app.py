"""Dashboard Restoran Nusantara - studi kasus portofolio (dataset simulasi). Palet: daun pisang, kunyit, sambal."""
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Restoran Nusantara", page_icon="🍽️", layout="wide")
LEAF, DEEP, TURM, SAMBAL, CREAM, SAND, INK, GREY = "#5E8C61", "#1F4D3A", "#E3A83B", "#C8472B", "#F7F1E5", "#EADFC8", "#1F2A24", "#7A7367"
CAT = {"Makanan": SAMBAL, "Minuman": LEAF, "Snack": TURM}
rp = lambda x: f"Rp {x:,.0f}".replace(",", ".")
jt = lambda x: f"Rp {x/1e6:,.1f} jt".replace(",", "X").replace(".", ",").replace("X", ".")
ribu = lambda n: f"{n:,}".replace(",", ".")
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DAYS_ID = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700;800&family=Inter:wght@400;500;600&display=swap');
.stApp {{background:{CREAM}; color:{INK}; font-family:'Inter',sans-serif;}}
.stApp h1,.stApp h2,.stApp h3,.stApp label,.stApp p {{color:{INK};}}
span[data-baseweb="tag"] {{background:{DEEP} !important;}} span[data-baseweb="tag"] span {{color:#fff !important;}}
.hero {{background-color:{DEEP}; border-radius:22px; padding:34px 40px 28px; position:relative; overflow:hidden;
  background-image: radial-gradient(circle at 25% 25%, {TURM}30 0 16%, transparent 17%), radial-gradient(circle at 75% 75%, {TURM}30 0 16%, transparent 17%),
                    radial-gradient(circle at 75% 25%, #ffffff12 0 9%, transparent 10%), radial-gradient(circle at 25% 75%, #ffffff12 0 9%, transparent 10%);
  background-size:64px 64px;}}
.hero .eyebrow {{color:{TURM}; letter-spacing:4px; font-size:.75rem; font-weight:600;}}
.hero .title {{font-family:'Playfair Display',Georgia,serif; color:#FFF8E7; font-size:3.4rem; font-weight:800; line-height:1.1; margin:8px 0 6px;}}
.hero .tagline {{color:#E8DDC3; font-size:1.05rem; max-width:720px; line-height:1.5;}}
.stats {{display:flex; gap:0; margin-top:26px; background:#0F2E22cc; border-radius:14px; border:1px solid {TURM}66;}}
.st {{flex:1; padding:16px 22px; border-right:1px solid {TURM}44;}} .st:last-child {{border-right:none;}}
.st .sv {{font-family:'Playfair Display',Georgia,serif; color:{TURM}; font-size:1.9rem; font-weight:700; white-space:nowrap;}}
.st .sl {{color:#E8DDC3; font-size:.78rem; letter-spacing:1.5px; text-transform:uppercase; margin-top:2px;}}
.sec {{margin:46px 0 4px; display:flex; align-items:center; gap:14px;}}
.sec .blk {{width:12px; height:34px; background:{SAMBAL}; border-radius:3px;}}
.sec .t {{font-family:'Playfair Display',Georgia,serif; font-size:1.9rem; font-weight:700; color:{DEEP};}}
.sec .l {{flex:1; border-bottom:2px dotted {TURM}aa;}}
.q {{color:{GREY}; margin:0 0 16px 26px;}}
.rank {{background:#fff; border-radius:18px; padding:22px; border:1px solid {SAND}; box-shadow:0 6px 18px rgba(31,77,58,.08); height:100%;}}
.rank.first {{background:linear-gradient(145deg,{DEEP},#2D6A4F); border:none;}}
.rank .no {{color:{SAMBAL}; letter-spacing:3px; font-size:.72rem; font-weight:700;}} .rank.first .no {{color:{TURM};}}
.rank .n {{font-family:'Playfair Display',Georgia,serif; font-size:1.5rem; font-weight:700; margin:6px 0 4px; color:{DEEP};}} .rank.first .n {{color:#FFF8E7;}}
.rank .v {{font-family:'Playfair Display',Georgia,serif; font-size:2rem; font-weight:700; color:{SAMBAL};}} .rank.first .v {{color:{TURM};}}
.rank .u {{color:{GREY}; font-size:.88rem;}} .rank.first .u {{color:#E8DDC3;}}
.rank .bar {{height:6px; background:{SAND}; border-radius:6px; margin-top:12px;}} .rank.first .bar {{background:#ffffff30;}}
.rank .bar div {{height:6px; border-radius:6px; background:{SAMBAL};}} .rank.first .bar div {{background:{TURM};}}
.dp {{background:#fff; border-radius:16px; padding:18px 20px; border:1px solid {SAND}; border-top:5px solid {SAND};}} .dp.top {{border-top-color:{SAMBAL};}}
.dp .t {{color:{GREY}; letter-spacing:2px; font-size:.75rem; font-weight:600; text-transform:uppercase;}}
.dp .v {{font-family:'Playfair Display',Georgia,serif; font-size:2.2rem; font-weight:700; color:{DEEP};}} .dp.top .v {{color:{SAMBAL};}} .dp .s {{color:{GREY}; font-size:.85rem;}}
.say {{background:#fff; border-left:5px solid {TURM}; border-radius:10px; padding:14px 20px; margin:14px 0; box-shadow:0 3px 12px rgba(31,77,58,.07); line-height:1.6;}}
.line {{display:flex; justify-content:space-between; font-size:.95rem; padding-top:10px;}} .line .b {{color:{GREY}; font-weight:600;}}
.lbar {{height:7px; background:{SAND}; border-radius:7px; margin-top:5px;}} .lbar div {{height:7px; border-radius:7px; background:{DEEP};}}
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
    fig.update_xaxes(showgrid=False, linecolor=SAND); fig.update_yaxes(gridcolor=SAND, zeroline=False)
    return fig


def section(t, q):
    st.markdown(f'<div class="sec"><span class="blk"></span><span class="t">{t}</span><span class="l"></span></div><div class="q">{q}</div>', unsafe_allow_html=True)


def say(t):
    st.markdown(f'<div class="say">{t}</div>', unsafe_allow_html=True)


def line(a, b, ratio):
    st.markdown(f'<div class="line"><span>{a}</span><span class="b">{b}</span></div><div class="lbar"><div style="width:{ratio*100:.0f}%"></div></div>', unsafe_allow_html=True)


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

total = f["total_amount"].sum()
st.markdown(f"""<div class="hero"><div class="eyebrow">STUDI KASUS · DATASET SIMULASI</div>
<div class="title">Restoran Nusantara</div>
<div class="tagline">Menu mana yang menjadi bintang, kapan dapur paling sibuk, dan apakah diskon benar-benar berhasil. Januari – Juni 2026.</div>
<div class="stats">
<div class="st"><div class="sv">{jt(total)}</div><div class="sl">Total pendapatan</div></div>
<div class="st"><div class="sv">{ribu(len(f))}</div><div class="sl">Transaksi</div></div>
<div class="st"><div class="sv">{rp(f['total_amount'].mean())}</div><div class="sl">Rata-rata per transaksi</div></div>
<div class="st"><div class="sv">{rp(f['discount_amount'].sum())}</div><div class="sl">Diskon diberikan</div></div>
</div></div>""", unsafe_allow_html=True)

prod = f.groupby(["product", "category"], as_index=False).agg(pendapatan=("total_amount", "sum"), unit=("quantity", "sum"), harga=("unit_price", "mean")).sort_values("pendapatan", ascending=False).reset_index(drop=True)

section("Menu Andalan", "Tiga menu penyumbang pendapatan terbesar dan posisi menu lainnya.")
cols = st.columns(3)
for i, col in enumerate(cols):
    r = prod.iloc[i]
    col.markdown(f'<div class="rank {"first" if i == 0 else ""}"><div class="no">PERINGKAT {i+1}</div><div class="n">{r["product"]}</div><div class="v">{jt(r["pendapatan"])}</div><div class="u">{int(r["unit"])} porsi · {r["pendapatan"]/total*100:.1f}% dari total pendapatan</div><div class="bar"><div style="width:{r["pendapatan"]/prod["pendapatan"].max()*100:.0f}%"></div></div></div>', unsafe_allow_html=True)
st.write("")
a, b = st.columns([3, 2])
with a:
    st.markdown("**Pendapatan seluruh menu (juta rupiah)**")
    d = prod.assign(jt=prod["pendapatan"] / 1e6).sort_values("jt")
    fig = px.bar(d, x="jt", y="product", orientation="h", color="category", color_discrete_map=CAT, text=d["jt"].round(1).astype(str), labels={"jt": "Juta rupiah", "product": "", "category": ""})
    fig.update_traces(textposition="outside", marker_cornerradius=5)
    st.plotly_chart(fmt(fig, 470).update_layout(showlegend=True, legend=dict(orientation="h", y=-0.1)), width="stretch")
with b:
    st.markdown("**Kontribusi kategori**")
    cat = f.groupby("category", as_index=False)["total_amount"].sum()
    fig = px.pie(cat, names="category", values="total_amount", hole=0.6, color="category", color_discrete_map=CAT)
    fig.update_traces(textinfo="percent+label", textfont=dict(size=14))
    st.plotly_chart(fmt(fig, 470), width="stretch")

section("Peta Menu", "Menu mana yang dipertahankan, dipromosikan, atau dievaluasi.")
mu, mp = prod["unit"].median(), prod["harga"].median()
def kuad(r):
    if r["unit"] >= mu and r["harga"] >= mp: return "Bintang"
    if r["unit"] >= mu: return "Penarik pembeli"
    if r["harga"] >= mp: return "Perlu dipromosikan"
    return "Evaluasi"
prod["kelompok"] = prod.apply(kuad, axis=1)
x0, x1 = prod["unit"].min() * 0.85, prod["unit"].max() * 1.12; y0, y1 = prod["harga"].min() * 0.8, prod["harga"].max() * 1.15
fig = px.scatter(prod, x="unit", y="harga", size="pendapatan", color="kelompok", text="product", size_max=46,
                 color_discrete_map={"Bintang": DEEP, "Penarik pembeli": TURM, "Perlu dipromosikan": SAMBAL, "Evaluasi": "#9A9488"},
                 labels={"unit": "Porsi terjual (makin ke kanan makin laris)", "harga": "Harga per porsi (Rp)", "kelompok": ""})
for (xa, xb, ya, yb, col, name, ax, ay) in [(mu, x1, mp, y1, "rgba(31,77,58,.10)", "BINTANG", x1, y1), (mu, x1, y0, mp, "rgba(227,168,59,.13)", "PENARIK PEMBELI", x1, y0),
                                            (x0, mu, mp, y1, "rgba(200,71,43,.10)", "PERLU DIPROMOSIKAN", x0, y1), (x0, mu, y0, mp, "rgba(154,148,136,.12)", "EVALUASI", x0, y0)]:
    fig.add_shape(type="rect", x0=xa, x1=xb, y0=ya, y1=yb, fillcolor=col, line_width=0, layer="below")
    fig.add_annotation(x=ax, y=ay, text=f"<b>{name}</b>", showarrow=False, xanchor="right" if ax == x1 else "left", yanchor="top" if ay == y1 else "bottom", font=dict(size=11, color=GREY))
fig.update_traces(textposition="top center", marker=dict(line=dict(width=1, color="#fff")))
fig.update_xaxes(range=[x0, x1]); fig.update_yaxes(range=[y0, y1])
st.plotly_chart(fmt(fig, 520), width="stretch")
st.caption("Garis pembagi = nilai tengah. Harga dipakai sebagai pengganti margin karena data tidak memuat biaya bahan.")
g = prod.groupby("kelompok")["product"].apply(lambda s: ", ".join(s)).to_dict()
say(f"<b>Bintang</b> (laris dan harga tinggi): {g.get('Bintang', '-')}.<br><b>Penarik pembeli</b> (laris, harga rendah, cocok untuk bundling): {g.get('Penarik pembeli', '-')}.<br><b>Perlu dipromosikan</b> (harga tinggi, kurang laris): {g.get('Perlu dipromosikan', '-')}.")

section("Waktu Dapur Sibuk", "Kapan restoran paling ramai dan seberapa merata.")
sl = f.groupby("slot", observed=True).agg(n=("transaction_id", "size"), tiket=("total_amount", "mean")).reset_index()
topslot = sl.sort_values("n").iloc[-1]["slot"]
cols = st.columns(3)
for col, (_, r) in zip(cols, sl.iterrows()):
    col.markdown(f'<div class="dp {"top" if r["slot"] == topslot else ""}"><div class="t">{r["slot"]}</div><div class="v">{ribu(int(r["n"]))}</div><div class="s">transaksi · {r["n"]/len(f)*100:.0f}% · rata-rata {rp(r["tiket"])}</div></div>', unsafe_allow_html=True)
st.write("")
a, b = st.columns([2, 3])
h = f.groupby("hour", as_index=False).size()
with a:
    st.markdown("**Transaksi per jam**")
    fig = px.area(h, x="hour", y="size", color_discrete_sequence=[SAMBAL], labels={"hour": "Jam", "size": "Transaksi"}); fig.update_traces(line=dict(width=2.5), fillcolor="rgba(200,71,43,.18)")
    st.plotly_chart(fmt(fig, 340), width="stretch")
with b:
    st.markdown("**Peta kepadatan hari × jam** (makin pekat makin ramai)")
    hm = f.pivot_table(index="day_name", columns="hour", values="transaction_id", aggfunc="count", fill_value=0).reindex(DAYS); hm.index = DAYS_ID
    fig = px.imshow(hm, aspect="auto", color_continuous_scale=[CREAM, TURM, SAMBAL, DEEP], labels=dict(x="Jam", y="", color="Transaksi"))
    st.plotly_chart(fmt(fig, 340), width="stretch")
say(f"Jam tersibuk adalah <b>{int(h.loc[h['size'].idxmax(), 'hour'])}.00</b>. Keramaian cukup merata dari jam 10 sampai 22, sehingga jumlah staf perlu stabil sepanjang hari.")

section("Cara Pesan dan Bayar", "Lewat apa pelanggan memesan dan membayar. Klik kotak untuk memperbesar.")
tm = f.groupby(["order_type", "payment_method"], as_index=False)["total_amount"].sum()
fig = px.treemap(tm, path=["order_type", "payment_method"], values="total_amount", color="order_type", color_discrete_sequence=[DEEP, SAMBAL, "#8A6D2F"])
fig.update_traces(textinfo="label+percent parent", textfont=dict(color="#fff", size=15)); st.plotly_chart(fmt(fig, 380), width="stretch")

section("Efektivitas Diskon", "Jika diskon diberikan, apakah pelanggan membeli lebih banyak porsi.")
ds = f.groupby("discount_rate").agg(n=("transaction_id", "size"), porsi=("quantity", "mean")).reset_index(); ds["label"] = (ds["discount_rate"] * 100).round(0).astype(int).astype(str) + "%"
a, b = st.columns([3, 2])
with a:
    st.markdown("**Rata-rata porsi per transaksi menurut besar diskon**")
    fig = px.bar(ds, x="label", y="porsi", text=ds["porsi"].round(2), color_discrete_sequence=[DEEP], labels={"label": "Besar diskon", "porsi": "Porsi"})
    fig.update_traces(textposition="outside", marker_cornerradius=8); fig.update_yaxes(range=[0, max(3, ds["porsi"].max() * 1.3)])
    st.plotly_chart(fmt(fig, 330), width="stretch")
with b:
    st.markdown("**Seberapa sering diskon dipakai**")
    for _, r in ds.iterrows():
        line(f"Diskon {r['label']}", f"{r['n']/ds['n'].sum()*100:.0f}% transaksi", r["n"] / ds["n"].max())
say(f"Rata-rata porsi per transaksi nyaris sama di semua level diskon ({ds['porsi'].min():.2f} sampai {ds['porsi'].max():.2f}). Total diskon {rp(f['discount_amount'].sum())} belum terbukti menambah pembelian.")

with st.expander("Lihat data transaksi"):
    st.dataframe(f.drop(columns=["hour", "day_name", "slot"]), width="stretch")
