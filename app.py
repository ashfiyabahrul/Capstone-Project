import streamlit as st
import pandas as pd
import altair as alt
from numerize import numerize
import streamlit.components.v1 as components
from lorem_text import lorem
import datetime as dt
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

def filter_dataframe(df: pd.DataFrame):
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]
    global rowsnum
    rowsnum = len(df)
    return df

df = pd.read_csv('datasetSatuDataIndonesia(clean).csv')
df['Tanggal Unggah'] = pd.to_datetime(df['Tanggal Unggah'])
df['Bulan Unggah']=pd.DatetimeIndex(df['Tanggal Unggah']).month
# CURR_MONTH = max(pd.DatetimeIndex(df['Tanggal Unggah']).month)
# PREV_MONTH = CURR_MONTH - 1

data = pd.pivot_table(
    data=df,
    index='Instansi',
    aggfunc={
        'Jumlah File':'sum'
        # 'profit':'sum',
        # 'order_id':pd.Series.nunique,
        # 'customer_id':pd.Series.nunique
    }
).reset_index()

rowsnum = len(df)
st.set_page_config(
    page_title ='Analisis Dataset Pada Website Satu Data Indonesia',
    layout='wide')
alt.themes.enable('dark')
custom_palette = alt.Scale(
    range=['#FF0000', '#00FF00', '#0000FF']  # Contoh palet warna kustom
)
# st.write('Hello World!')
# st.title('Analisis Dataset Pada Website Satu Data Indonesia')

st.markdown("<h1 style='text-align: center; color: red;'>Analisis Dataset Pada Website <span style='color: white;'>Satu Data Indonesia</span></h1>", unsafe_allow_html=True)

with st.sidebar:
    st.title("Analisis Dataset Satu Data")
    with st.expander("Disclaimer"):
        st.write("Data in this website is web scrapped from Satu Data Indonesia site on 09 June 2023.")

st.write('Pada tanggal 23 Desember 2022 yang lalu, pemerintah resmi meluncurkan portal Satu Data Indonesia (SDI) yang menjadi upaya untuk menghasilkan kebijakan yang tepat dengan data yang valid dan akurat. SDI merupakan kebijakan tata kelola data pemerintah yang bertujuan untuk menciptakan data berkualitas, mudah diakses, dan dapat dibagipakaikan antar-instansi pusat serta daerah.')
st.write('Portal SDI dapat berfungsi sebagai marketplace data pemerintah, yang mempertemukan supply dan demand terhadap data.')
st.write('Portal SDI terhubung dengan seluruh portal data di masing-masing instansi pemerintahan. Beragam jenis data baik statistik, spasial, maupun keuangan di seluruh strata pemerintah itu akan bermuara di portal SDI.')
st.write('Oleh sebab itu, instansi pemerintah pusat dan daerah diajak untuk meningkatkan kesadaran bersama tentang pentingnya data dalam satu kebijakan pembangunan, serta membudayakan data menjadi kekayaan dan kepentingan bersama sehingga dapat menghasilkan kebijakan yang tepat.')
with st.expander("Dataset Satu Data Indonesia"):
    st.dataframe(filter_dataframe(df))
    st.caption(str(rowsnum)+' rows is showed')

jumlah_dataset, jumlah_file, jumlah_instansi = st.columns(3)

st.markdown("""
<style>
div[data-testid="metric-container"] {
   background-color: rgba(28, 131, 225, 0.1);
   border: 1px solid rgba(28, 131, 225, 0.1);
   padding: 5% 5% 5% 10%;
   border-radius: 5px;
   color: white;
   overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: red;
}
</style>
"""
, unsafe_allow_html=True)

with jumlah_dataset:
    st.metric("Jumlah Dataset", value=numerize.numerize(rowsnum))

with jumlah_file:
    # curr_files = df[pd.DatetimeIndex(df['Tanggal Unggah']).month == max(pd.DatetimeIndex(df['Tanggal Unggah']).month),'Jumlah File']
    # prev_files = df[pd.DatetimeIndex(df['Tanggal Unggah']).month == max(pd.DatetimeIndex(df['Tanggal Unggah']).month)-1,'Jumlah File']
    # st.write(curr_files)
    # curr_files = data.loc[data['Bulan Unggah']==CURR_MONTH, 'Jumlah File'].values[0]
    # prev_files = data.loc[data['Bulan Unggah']==PREV_MONTH, 'Jumlah File'].values[0]
    
    # files_diff_pct = 100.0 * (curr_files - prev_files) / prev_files

    # st.metric("Jumlah File", value=numerize.numerize(curr_files), delta=f'{files_diff_pct:.2f}%')
    st.metric("Jumlah File", value=numerize.numerize(df['Jumlah File'].sum().item()))

with jumlah_instansi:
    st.metric("Jumlah Instansi", value=numerize.numerize(len(df['Instansi'].unique())))

# st.header("Files trend")
# # altair membuat object berupa chart dengan data di dalam parameter
# files_line = alt.Chart(df['Tanggal Unggah']).mark_line().encode(
#     alt.X('Tanggal Unggah', title='Tanggal Unggah', timeUnit='year'),
#     alt.Y('Jumlah File', title='Jumlah File', aggregate='sum')
# )

# st.altair_chart(files_line,use_container_width=True)

instansi_jumlahfile=alt.Chart(data).mark_bar().encode(
    x='Instansi',
    y='Jumlah File',
    color='Instansi',
    tooltip=['Instansi', 'Jumlah File']
).transform_window(
    rank='rank(Jumlah File)',
    sort=[alt.SortField('Jumlah File', order='descending')]
).transform_filter(
    (alt.datum.rank < 4)
).configure_legend(
    titleFontSize=14,  # Ukuran font judul legenda
    labelFontSize=10  # Ukuran font label legenda
).properties(
    title='3 Instansi Pemilik Jumlah File Terbanyak'
).interactive()

instansi_jumlahfilerendah=alt.Chart(data).mark_bar().encode(
    x='Instansi',
    y='Jumlah File',
    color='Instansi',
    tooltip=['Instansi', 'Jumlah File']
).transform_window(
    rank='rank(Jumlah File)',
    sort=[alt.SortField('Jumlah File', order='ascending')]
).transform_filter(
    (alt.datum.rank < 10)
).configure_legend(
    titleFontSize=14,  # Ukuran font judul legenda
    labelFontSize=10  # Ukuran font label legenda
).properties(
    title='10 Instansi Pemilik Jumlah File Terendah'
).interactive()

line_data = df.groupby('Bulan Unggah')['Jumlah File'].sum().reset_index()
bulanan = alt.Chart(line_data).mark_line().encode(
    x='Bulan Unggah',
    y='Jumlah File',
    tooltip=['Bulan Unggah', 'Jumlah File']
).properties(
    title='Tren Unggahan Dataset Bulanan'
).interactive()

line_data2 = df.groupby('Tanggal Unggah')['Jumlah File'].sum().reset_index()
harian = alt.Chart(line_data2).mark_line().encode(
    x='Tanggal Unggah',
    y='Jumlah File',
    tooltip=['Tanggal Unggah', 'Jumlah File']
).properties(
    title='Tren Unggahan Dataset Harian'
).interactive()


linechart, penjelasan = st.columns(2)
with linechart:
    st.altair_chart(bulanan, use_container_width=True)
with penjelasan:
    st.write('Dari Grafik disamping kita dapat menyimpulkan bahwa terdapat lonjakan jumlah file dataset yang diunggah pada bulan april dan oktober.')

linechart, penjelasan = st.columns(2)
with linechart:
    st.altair_chart(harian, use_container_width=True)
with penjelasan:
    st.write('Pada line chart disamping lagi-lagi ditunjukan bahwa terjadi kenaikan yang sangat tinggi pada tanggal 15 di bulan april. Ada apakah ini? Setelah ditelusuri ternyata ini terjadi setelah diadakannya rapat koordinasi untuk membahas percepatan terwujudnya satu data indonesia.')

penjelasan, top3instansi = st.columns(2)
with penjelasan:
    st.write('Grafik disamping menunjukkan bahwa pemerintah kota Banjarbaru, Provinsi Jawa Barat dan Kalimantan Barat menjadi top 3 teratas instansi pengunggah file dataset pada situs satu data indonesia')
with top3instansi:
    st.altair_chart(instansi_jumlahfile,use_container_width=True)



penjelasan, bottom10instansi = st.columns(2)
with penjelasan:
    st.write('Sedangkan pada grafik disamping ditunjukkan bahwa masih ada juga instansi yang belum memberikan banyak kontribusi pada situs satu data indonesia')
with bottom10instansi:
    st.altair_chart(instansi_jumlahfilerendah,use_container_width=True)

with st.expander("Kesimpulan dan Insight"):
    st.write("Masih banyak sekali instansi yang belum terlalu berkontribusi dalam mewujudkan satu data indonesia. Padahal ini sangat penting demi mewujudkan ketersediaan data bagi negara. Namun bisa jadi ini terjadi karena kurangnya sosialisasi dan koordinasi terhadap tiap pemerintah daerah, apalagi pemerintah daerah terpelosok yang mungkin bahkan belum mengetahui adanya platform satu data indonesia ini. Kenaikan aktifitas pengunggahan terbukti melonjak setelah diadakannya rapat koordinasi. Jadi dapat disimpulkan bahwa pemerintah pusat harus lebih aktif lagi dalam memberikan penyuluhan dan sosialisasi agar kesadaran terhadap situs satu data indonesia dapat terus menguat. -Muhammad Bahrul Ashfiya")
st.caption('Sumber: https://www.kominfo.go.id/content/detail/46520/pemerintah-luncurkan-portal-satu-data-indonesia/0/berita; https://sumutprov.go.id/artikel/artikel/rakor-penyelenggaraan-statistik-sektoral-percepat-terwujudnya-satu-data-indonesia;')