import streamlit as st
import requests
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import joblib


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def loadModel():
	model_d = tf.keras.models.load_model('model_diabetes.h5')
	model_h = tf.keras.models.load_model('model_heart.h5')
	model_s = tf.keras.models.load_model('model_stroke.h5')
	return model_d, model_h, model_s

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def loadScaler():
	ss_d = joblib.load('ss_d.bin')
	ss_h = joblib.load('ss_h.bin')
	ss_s = joblib.load('ss_s.bin')
	return ss_d, ss_h, ss_s

def normalize_data(datas, scalers, model_h):
    data_diabetes = [datas[0]]
    data_diabetes = scalers[0].transform(data_diabetes)
    data_heart = [datas[1]]
    data_heart = scalers[1].transform(data_heart)
    datas[2].insert(3, predict_heart(data_heart, model_h))
    data_stroke = [datas[2]]
    data_stroke = scalers[2].transform(data_stroke)
    return data_diabetes, data_heart, data_stroke

def predict_diabetes(datas, model):
    return 1 if model.predict(datas)[0][0] > 0.5 else 0

def predict_heart(datas, model):
    return 1 if model.predict(datas)[0][0] > 0.5 else 0

def predict_stroke(datas, model):
    return 1 if model.predict(datas)[0][0] > 0.5 else 0

def rekomendasi(name, prediksi_d, prediksi_h, prediksi_s):
    if prediksi_d == 0 and prediksi_h == 0 and prediksi_s == 0:
        with st.expander("Lihat Hasil Rekomendasi Gaya Hidup"):
            st.write("SELAMAT", name.upper(), ", KEMUNGKINAN ANDA MEMILIKI KE 3 PENYAKIT SANGATLAH KECIL")
            st.markdown("")
            st.write("Teruskan gaya hidup sehat yang anda jalani.")
            st.write("Jangan lupa untuk selalu berolahraga dan menjaga pola tidur yang baik. Makan makanan yang bergizi dan penuhi 4 sehat 5 sempurna.")
            st.markdown(
                "<img src='https://www.nicepng.com/png/detail/8-83629_google-thumbs-up-emoji.png' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                unsafe_allow_html=True)
            ""

    elif prediksi_d == 0 and prediksi_h == 0 and prediksi_s == 1:
        with st.expander("Lihat Hasil Rekomendasi Gaya Hidup"):
            st.write("Halo ", name,
                     ". Berdasarkan riwayat kesehatan anda, anda memiliki kemungkinan mengidap penyakit stroke.")
            st.markdown("")
            st.write("Ini adalah rekomendasi gaya hidup sehat yang perlu anda jalani.")
            st.markdown("**MAKANAN**")
            st.write(":heavy_check_mark: Harus Diperbanyak :heavy_check_mark:")
            st.write("+ Perbanyak asupan buah - buahan, seperti pepaya, melon, mangga, jeruk, dan lainnya")
            st.write("+ Perbanyak asupan sayuran, seperti brokoli, bayam, kangkung, sawi dan sayuran hijau lain")
            ""
            st.write(":x: Harus Dihindari :x:")
            st.write("+ Hindari buah nanas, kedondong, nangka dan durian")
            st.write("+ Hindari ubi, kacang merah, sawi dan lobak")
            st.write("+ Hindari makanan berlemak dan mengandung kolesterol tinggi, seperti kambing, sosis, "
                     "kulit ayam, lemak hewan, jeroan, kepiting, cumi - cumi, udang dan kerang, margarin dan mentega")
            st.write(
                "+ Batasi Asupan Garam (tidak lebih dari 1 sendok teh sehari) dengan jangan mengonsumsi makanan sumber Na, Seperti ikan asin, teri, udang kering, "
                "telur asin, kue yang mengandung soda kue atau garam dapur, vetsin, soda kue, kecap, maggi, petis, tauco, saus tomat ")
            ""
            st.write("**OLAHRAGA**")
            st.write("- Lakukan olahraga minimal 30 menit setiap hari")
            st.write("- Olahraga ringan saja, seperti jalan santai, atau bersepeda")
            ""
            st.write("**POLA PERILAKU**")
            st.write("- Jangan merokok")
            st.write("- Jangan mengonsumsi alkohol dan minuman bersoda")
            st.write("- Kurangi stres dan hindari penyebabnya")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    "<img src='https://akcdn.detik.net.id/community/media/visual/2020/03/26/da451b98-12c6-43d5-8539-d20708b02d02.jpeg?w=700&q=90' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            with col2:
                st.markdown(
                    "<img src='https://nowjakarta.co.id/uploads/article/image/303/cfdjune2019_2_10_radityafadilla-thumbnail.jpg' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            with col3:
                st.markdown(
                    "<img src='https://previews.123rf.com/images/phonprom/phonprom1212/phonprom121200032/17005407-no-smoking-no-drinking.jpg' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            ""

    elif prediksi_d == 0 and prediksi_h == 1 and prediksi_s == 0:
        with st.expander("Lihat Hasil Rekomendasi Gaya Hidup"):
            st.write("Halo ", name,
                     ". Berdasarkan riwayat kesehatan anda, anda memiliki kemungkinan mengidap penyakit jantung.")
            st.markdown("")
            st.write("Ini adalah rekomendasi gaya hidup sehat yang perlu anda jalani.")
            st.markdown("**MAKANAN**")
            st.write(":heavy_check_mark: Harus Diperbanyak :heavy_check_mark:")
            st.write(
                "+ Perbanyak asupan buah - buahan, seperti alpukat, tomat, stroberi, blueberry, atau raspberry, jeruk, melon, dan pepaya")
            st.write("+ Perbanyak asupan sayuran, seperti brokoli, bayam, kangkung, sawi dan sayuran hijau lain")
            st.write("+ Konsumsi ikan berlemak yang kaya dengan omega-3 seperti salmon, makarel, ikan sarden, dan tuna")
            st.write("+ Kacang, cokelat hitam, bawang putih dan teh hijau baik dan membuat jantung lebih sehat")
            ""
            st.write(":x: Harus Dihindari :x:")
            st.write("+ Hindari daging merah, sayuran yang digoreng dan buah kalengan")
            st.write("+ Hindari makanan berlemak dan mengandung kolesterol tinggi, seperti kambing, sosis, "
                     "kulit ayam, lemak hewan, jeroan, kepiting, cumi - cumi, udang dan kerang, margarin dan mentega")
            st.write("+ Kurangi konsumsi gula, termasuk susu, dan manisan")
            st.write("+ Batasi asupan kalori, seperti gorengan, kue, biskuit, termasuk nasi")
            st.write(
                "+ Batasi asupan garam (tidak lebih dari 1 sendok teh sehari) dengan jangan mengonsumsi makanan sumber Na, Seperti ikan asin, teri, udang kering, "
                "telur asin, kue yang mengandung soda kue atau garam dapur, vetsin, soda kue, kecap, maggi, petis, tauco, saus tomat")
            ""
            st.write("**OLAHRAGA**")
            st.write("- Lakukan olahraga minimal 30 menit setiap hari, namun jangan berlebihan")
            st.write("- Olahraga ringan saja, seperti jalan santai, atau bersepeda")
            ""
            st.write("**POLA PERILAKU**")
            st.write("- Hindari kebiasaan merokok")
            st.write("- Jangan mengonsumsi alkohol dan minuman bersoda")
            st.write("- Minum air putih, sekitar 8 gelas dalam sehari")
            st.write("- Kurangi stres dan hindari penyebabnya")
            st.write("- Istirahat yang Cukup, tidurlah sekitar 6–8 jam dalam sehari")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    "<img src='https://akcdn.detik.net.id/community/media/visual/2020/03/26/da451b98-12c6-43d5-8539-d20708b02d02.jpeg?w=700&q=90' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            with col2:
                st.markdown(
                    "<img src='https://nowjakarta.co.id/uploads/article/image/303/cfdjune2019_2_10_radityafadilla-thumbnail.jpg' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            with col3:
                st.markdown(
                    "<img src='https://previews.123rf.com/images/phonprom/phonprom1212/phonprom121200032/17005407-no-smoking-no-drinking.jpg' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            ""

    elif prediksi_d == 1 and prediksi_h == 0 and prediksi_s == 0:
        with st.expander("Lihat Hasil Rekomendasi Gaya Hidup"):
            st.write("Halo ", name,
                     ". Berdasarkan riwayat kesehatan anda, anda memiliki kemungkinan mengidap penyakit diabetes.")
            st.markdown("")
            st.write("Ini adalah rekomendasi gaya hidup sehat yang perlu anda jalani.")
            st.markdown("**MAKANAN**")
            st.write(":heavy_check_mark: Harus Diperbanyak :heavy_check_mark:")
            st.write(
                "+ Makanlah sesuatu setiap 3 jam dan makanan utama tidak lebih dari empat-lima jam terpisah.")
            st.write(
                "+ Lebih selektif dalam memakan buah, buah yang aman untuk anda makan adalah anggur, apel, jeruk, beri, kiwi, jambu biji dan pir")
            st.write(
                "+ Perbanyak asupan sayuran, seperti wortel, pare, brokoli, bayam, kangkung, sawi dan sayuran hijau lain")
            st.write(
                "+ Konsumsi suplemen, seperti Vitamin C, Vitamin D, Vitamin E, dan Magnesium")
            ""
            st.write(":x: Harus Dihindari :x:")
            st.write("+ Kurangi konsumsi gula dan hindari makanan manis")
            st.write("+ Hindari makanan berlemak dan makanan yang digoreng")
            st.write(
                "+ Batasi asupan karbohidrat, seperti nasi putih, roti putih, dan kentang goreng, ganti dengan makanan, seperti beras merah, roti dari biji-bijian utuh, atau ubi jalar yang dipanggang")
            st.write(
                "+ Batasi asupan garam (tidak lebih dari 1 sendok teh sehari) dengan jangan mengonsumsi makanan sumber Na, Seperti ikan asin, teri, udang kering, "
                "telur asin, kue yang mengandung soda kue atau garam dapur, vetsin, soda kue, kecap, maggi, petis, tauco, saus tomat")

            ""
            st.write("**OLAHRAGA**")
            st.write("- Makan 2 jam sebelum berolahraga")
            st.write("- Anda sebaiknya menunda olahraga ketika kadar gula darah berada di atas 250 mg/dL")
            st.write("- Lakukan olahraga minimal 30 menit setiap hari")
            st.write("- Olahraga Berjalan, Jogging atau lari, Bersepeda, Senam aerobik, Senam Diabetes, Berenang")
            ""
            st.write("**POLA PERILAKU**")
            st.write("- Jangan mengonsumsi alkohol dan minuman bersoda")
            st.write("- Minum air putih, sekitar 8 gelas dalam sehari")
            st.write("- Istirahat yang Cukup, tidurlah sekitar 6–8 jam dalam sehari")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    "<img src='https://akcdn.detik.net.id/community/media/visual/2020/03/26/da451b98-12c6-43d5-8539-d20708b02d02.jpeg?w=700&q=90' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            with col2:
                st.markdown(
                    "<img src='https://nowjakarta.co.id/uploads/article/image/303/cfdjune2019_2_10_radityafadilla-thumbnail.jpg' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            with col3:
                st.markdown(
                    "<img src='https://res.cloudinary.com/dk0z4ums3/image/upload/v1618195657/attached_image/jangan-remehkan-manfaat-air-putih.jpg' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            ""

    elif prediksi_d == 0 and prediksi_h == 1 and prediksi_s == 1:
        with st.expander("Lihat Hasil Rekomendasi Gaya Hidup"):
            st.write("Halo ", name,
                     ". Berdasarkan riwayat kesehatan anda, anda memiliki kemungkinan mengidap penyakit jantung dan stroke.")
            st.markdown("")
            st.write("Ini adalah rekomendasi gaya hidup sehat yang perlu anda jalani.")
            st.markdown("**MAKANAN**")
            st.write(":heavy_check_mark: Harus Diperbanyak :heavy_check_mark:")
            st.write(
                "+ Perbanyak asupan buah - buahan, seperti alpukat, tomat, stroberi, blueberry, atau raspberry, jeruk, melon, mangga dan pepaya")
            st.write("+ Perbanyak asupan sayuran, seperti brokoli, bayam, kangkung dan sayuran hijau lain")
            st.write("+ Konsumsi ikan berlemak yang kaya dengan omega-3 seperti salmon, makarel, ikan sarden, dan tuna")
            st.write("+ Cokelat hitam, bawang putih dan teh hijau baik dan membuat jantung lebih sehat")
            ""
            st.write(":x: Harus Dihindari :x:")
            st.write("+ Hindari buah nanas, kedondong, nangka dan durian")
            st.write("+ Hindari ubi, kacang merah, sawi dan lobak")
            st.write("+ Hindari daging merah, sayuran yang digoreng dan buah kalengan")
            st.write("+ Hindari makanan berlemak dan mengandung kolesterol tinggi, seperti kambing, sosis, "
                     "kulit ayam, lemak hewan, jeroan, kepiting, cumi - cumi, udang dan kerang, margarin dan mentega")
            st.write("+ Kurangi konsumsi gula, termasuk susu, dan manisan")
            st.write("+ Batasi asupan kalori, seperti gorengan, kue, biskuit, termasuk nasi")
            st.write(
                "+ Batasi asupan garam (tidak lebih dari 1 sendok teh sehari) dengan jangan mengonsumsi makanan sumber Na, Seperti ikan asin, teri, udang kering, "
                "telur asin, kue yang mengandung soda kue atau garam dapur, vetsin, soda kue, kecap, maggi, petis, tauco, saus tomat")
            ""
            st.write("**OLAHRAGA**")
            st.write("- Lakukan olahraga minimal 30 menit setiap hari, namun jangan berlebihan")
            st.write("- Olahraga ringan saja, seperti jalan santai, atau bersepeda")
            ""
            st.write("**POLA PERILAKU**")
            st.write("- Hindari kebiasaan merokok")
            st.write("- Jangan mengonsumsi alkohol dan minuman bersoda")
            st.write("- Minum air putih, sekitar 8 gelas dalam sehari")
            st.write("- Kurangi stres dan hindari penyebabnya")
            st.write("- Istirahat yang cukup, tidurlah sekitar 6–8 jam dalam sehari")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    "<img src='https://akcdn.detik.net.id/community/media/visual/2020/03/26/da451b98-12c6-43d5-8539-d20708b02d02.jpeg?w=700&q=90' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            with col2:
                st.markdown(
                    "<img src='https://nowjakarta.co.id/uploads/article/image/303/cfdjune2019_2_10_radityafadilla-thumbnail.jpg' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            with col3:
                st.markdown(
                    "<img src='https://previews.123rf.com/images/phonprom/phonprom1212/phonprom121200032/17005407-no-smoking-no-drinking.jpg' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            ""

    elif prediksi_d == 1 and prediksi_h == 0 and prediksi_s == 1:
        with st.expander("Lihat Hasil Rekomendasi Gaya Hidup"):
            st.write("Halo ", name,
                     ". Berdasarkan riwayat kesehatan anda, anda memiliki kemungkinan mengidap penyakit diabetes dan stroke.")
            st.markdown("")
            st.write("Ini adalah rekomendasi gaya hidup sehat yang perlu anda jalani.")
            st.markdown("**MAKANAN**")
            st.write(":heavy_check_mark: Harus Diperbanyak :heavy_check_mark:")
            st.write(
                "+ Makanlah sesuatu setiap 3 jam dan makanan utama tidak lebih dari empat-lima jam terpisah.")
            st.write(
                "+ Lebih selektif dalam memakan buah, buah yang aman untuk anda makan adalah anggur, apel, jeruk, beri, kiwi, jambu biji dan pir")
            st.write(
                "+ Perbanyak asupan sayuran, seperti wortel, pare, brokoli, bayam, kangkung, sawi dan sayuran hijau lain")
            st.write(
                "+ Konsumsi suplemen untuk diabetes, seperti Vitamin C, Vitamin D, Vitamin E, dan Magnesium")
            ""
            st.write(":x: Harus Dihindari :x:")
            st.write("+ Hindari buah nanas, kedondong, nangka dan durian")
            st.write("+ Hindari ubi, kacang merah, sawi dan lobak")
            st.write("+ Kurangi konsumsi gula dan hindari makanan manis")
            st.write("+ Hindari makanan berlemak, mengandung kolesterol tinggi dan makanan yang digoreng")
            st.write(
                "+ Batasi asupan karbohidrat, seperti nasi putih, roti putih, dan kentang goreng, ganti dengan makanan, seperti beras merah, roti dari biji-bijian utuh, atau ubi jalar yang dipanggang")
            st.write(
                "+ Batasi asupan garam (tidak lebih dari 1 sendok teh sehari) dengan jangan mengonsumsi makanan sumber Na, Seperti ikan asin, teri, udang kering, "
                "telur asin, kue yang mengandung soda kue atau garam dapur, vetsin, soda kue, kecap, maggi, petis, tauco, saus tomat")

            ""
            st.write("**OLAHRAGA**")
            st.write("- Makan 2 jam sebelum berolahraga")
            st.write("- Anda sebaiknya menunda olahraga ketika kadar gula darah berada di atas 250 mg/dL")
            st.write("- Lakukan olahraga minimal 30 menit setiap hari")
            st.write("- Olahraga ringan saja, seperti jalan santai, atau bersepeda")
            ""
            st.write("**POLA PERILAKU**")
            st.write("- Jangan merokok")
            st.write("- Jangan mengonsumsi alkohol dan minuman bersoda")
            st.write("- Minum air putih, sekitar 8 gelas dalam sehari")
            st.write("- Istirahat yang Cukup, tidurlah sekitar 6–8 jam dalam sehari")
            st.write("- Kurangi stres dan hindari penyebabnya")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    "<img src='https://akcdn.detik.net.id/community/media/visual/2020/03/26/da451b98-12c6-43d5-8539-d20708b02d02.jpeg?w=700&q=90' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            with col2:
                st.markdown(
                    "<img src='https://nowjakarta.co.id/uploads/article/image/303/cfdjune2019_2_10_radityafadilla-thumbnail.jpg' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            with col3:
                st.markdown(
                    "<img src='https://res.cloudinary.com/dk0z4ums3/image/upload/v1618195657/attached_image/jangan-remehkan-manfaat-air-putih.jpg' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            ""

    elif prediksi_d == 1 and prediksi_h == 1 and prediksi_s == 0:
        with st.expander("Lihat Hasil Rekomendasi Gaya Hidup"):
            st.write("Halo ", name,
                     ". Berdasarkan riwayat kesehatan anda, anda memiliki kemungkinan mengidap penyakit diabetes dan jantung.")
            st.markdown("")
            st.write("Ini adalah rekomendasi gaya hidup sehat yang perlu anda jalani.")
            st.markdown("**MAKANAN**")
            st.write(":heavy_check_mark: Harus Diperbanyak :heavy_check_mark:")
            st.write(
                "+ Makanlah sesuatu setiap 3 jam namun hindari konsumsi yang manis dan makanan utama tidak lebih dari empat-lima jam terpisah.")
            st.write(
                "+ Lebih selektif dalam memakan buah, buah yang aman untuk anda makan adalah anggur, apel, jeruk, beri, kiwi, jambu biji dan pir")
            st.write(
                "+ Perbanyak asupan sayuran, seperti wortel, pare, brokoli, bayam, kangkung, sawi dan sayuran hijau lain")
            st.write(
                "+ Konsumsi suplemen untuk diabetes, seperti Vitamin C, Vitamin D, Vitamin E, dan Magnesium")
            st.write("+ Konsumsi ikan berlemak yang kaya dengan omega-3 seperti salmon, makarel, ikan sarden, dan tuna")
            st.write("+ Kacang, cokelat hitam, bawang putih dan teh hijau baik dan membuat jantung lebih sehat")
            ""
            st.write(":x: Harus Dihindari :x:")
            st.write("+ Hindari daging merah, sayuran yang digoreng dan buah kalengan")
            st.write("+ Kurangi konsumsi gula, termasuk susu, dan hindari makanan manis")
            st.write("+ Hindari makanan berlemak, mengandung kolesterol tinggi dan makanan yang digoreng")
            st.write(
                "+ Batasi asupan karbohidrat, seperti nasi putih, roti putih, dan kentang goreng, ganti dengan makanan, seperti beras merah, roti dari biji-bijian utuh, atau ubi jalar yang dipanggang")
            st.write(
                "+ Batasi asupan garam (tidak lebih dari 1 sendok teh sehari) dengan jangan mengonsumsi makanan sumber Na, Seperti ikan asin, teri, udang kering, "
                "telur asin, kue yang mengandung soda kue atau garam dapur, vetsin, soda kue, kecap, maggi, petis, tauco, saus tomat")
            ""
            st.write("**OLAHRAGA**")
            st.write("- Makan 2 jam sebelum berolahraga")
            st.write("- Anda sebaiknya menunda olahraga ketika kadar gula darah berada di atas 250 mg/dL")
            st.write("- Lakukan olahraga minimal 30 menit setiap hari, namun jangan berlebihan")
            st.write("- Olahraga ringan saja, seperti jalan santai, atau bersepeda")
            ""
            st.write("**POLA PERILAKU**")
            st.write("- Hindari kebiasaan merokok")
            st.write("- Jangan mengonsumsi alkohol dan minuman bersoda")
            st.write("- Minum air putih, sekitar 8 gelas dalam sehari")
            st.write("- Kurangi stres dan hindari penyebabnya")
            st.write("- Istirahat yang cukup, tidurlah sekitar 6–8 jam dalam sehari")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    "<img src='https://akcdn.detik.net.id/community/media/visual/2020/03/26/da451b98-12c6-43d5-8539-d20708b02d02.jpeg?w=700&q=90' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            with col2:
                st.markdown(
                    "<img src='https://nowjakarta.co.id/uploads/article/image/303/cfdjune2019_2_10_radityafadilla-thumbnail.jpg' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            with col3:
                st.markdown(
                    "<img src='https://res.cloudinary.com/dk0z4ums3/image/upload/v1618195657/attached_image/jangan-remehkan-manfaat-air-putih.jpg' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            ""

    elif prediksi_d == 1 and prediksi_h == 1 and prediksi_s == 1:
        with st.expander("Lihat Hasil Rekomendasi Gaya Hidup"):
            st.write("Halo ", name,
                     ". Berdasarkan riwayat kesehatan anda, anda memiliki kemungkinan mengidap penyakit diabetes, jantung, dan stroke.")
            st.markdown("")
            st.write("Ini adalah rekomendasi gaya hidup sehat yang perlu anda jalani.")
            st.markdown("**MAKANAN**")
            st.write(":heavy_check_mark: Harus Diperbanyak :heavy_check_mark:")
            st.write(
                "+ Makanlah sesuatu setiap 3 jam namun hindari konsumsi yang manis dan makanan utama tidak lebih dari empat-lima jam terpisah.")
            st.write(
                "+ Lebih selektif dalam memakan buah, buah yang aman untuk anda makan adalah anggur, apel, jeruk, beri, kiwi, jambu biji dan pir")
            st.write(
                "+ Perbanyak asupan sayuran, seperti wortel, pare, brokoli, bayam, kangkung, sawi dan sayuran hijau lain")
            st.write(
                "+ Konsumsi suplemen untuk diabetes, seperti Vitamin C, Vitamin D, Vitamin E, dan Magnesium")
            st.write("+ Konsumsi ikan berlemak yang kaya dengan omega-3 seperti salmon, makarel, ikan sarden, dan tuna")
            st.write("+ Cokelat hitam, bawang putih dan teh hijau baik dan membuat jantung lebih sehat")
            ""
            st.write(":x: Harus Dihindari :x:")
            st.write("+ Hindari buah nanas, kedondong, nangka dan durian")
            st.write("+ Hindari ubi, kacang merah, sawi dan lobak")
            st.write("+ Hindari daging merah, sayuran yang digoreng dan buah kalengan")
            st.write("+ Kurangi konsumsi gula, termasuk susu, dan hindari makanan manis")
            st.write("+ Hindari makanan berlemak, mengandung kolesterol tinggi dan makanan yang digoreng")
            st.write(
                "+ Batasi asupan karbohidrat, seperti nasi putih, roti putih, dan kentang goreng, ganti dengan makanan, seperti beras merah, roti dari biji-bijian utuh, atau ubi jalar yang dipanggang")
            st.write(
                "+ Batasi asupan garam (tidak lebih dari 1 sendok teh sehari) dengan jangan mengonsumsi makanan sumber Na, Seperti ikan asin, teri, udang kering, "
                "telur asin, kue yang mengandung soda kue atau garam dapur, vetsin, soda kue, kecap, maggi, petis, tauco, saus tomat")
            ""
            st.write("**OLAHRAGA**")
            st.write("- Makan 2 jam sebelum berolahraga")
            st.write("- Anda sebaiknya menunda olahraga ketika kadar gula darah berada di atas 250 mg/dL")
            st.write("- Lakukan olahraga minimal 30 menit setiap hari, namun jangan berlebihan")
            st.write("- Olahraga ringan saja, seperti jalan santai, atau bersepeda")
            ""
            st.write("**POLA PERILAKU**")
            st.write("- Hindari kebiasaan merokok")
            st.write("- Jangan mengonsumsi alkohol dan minuman bersoda")
            st.write("- Minum air putih, sekitar 8 gelas dalam sehari")
            st.write("- Kurangi stres dan hindari penyebabnya")
            st.write("- Istirahat yang cukup, tidurlah sekitar 6–8 jam dalam sehari")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    "<img src='https://akcdn.detik.net.id/community/media/visual/2020/03/26/da451b98-12c6-43d5-8539-d20708b02d02.jpeg?w=700&q=90' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            with col2:
                st.markdown(
                    "<img src='https://nowjakarta.co.id/uploads/article/image/303/cfdjune2019_2_10_radityafadilla-thumbnail.jpg' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            with col3:
                st.markdown(
                    "<img src='https://res.cloudinary.com/dk0z4ums3/image/upload/v1618195657/attached_image/jangan-remehkan-manfaat-air-putih.jpg' style='display: block; margin-left: auto; margin-right: auto;' width ='200'>",
                    unsafe_allow_html=True)
            ""

def main():
    model_d, model_h, model_s = loadModel()
    ss_d, ss_h, ss_s = loadScaler()
    scaler = [ss_d, ss_h, ss_s]
    st.title("APLIKASI KESEHATAN REKOMENDASI GAYA HIDUP")
    st.markdown("Aplikasi ini dibuat untuk memberikan rekomendasi gaya hidup sehat berdasarkan riwayat kesehatan pengguna")
    name = st.text_input("Masukkan nama anda :")
    age = st.slider("Masukkan usia anda :",0,100)
    pilih_sex = st.radio("Pilih jenis kelamin :",options=['Laki-laki','Perempuan'])
    if pilih_sex == 'Laki-laki':
        sex = 1
    else :
        sex = 0
    col1, col2, col3 = st.columns(3)
    with col1:
        tinggi = st.slider("Masukkan tinggi badan anda (m) :",0.1,3.0)
    with col2:
        berat = st.number_input("Masukkan berat badan anda (Kg) :",0.1,300.0)
    with col3:
        "Berat Massa Index (BMI) Anda"
        bmi = berat/(tinggi*tinggi)
        bmi
    
    st.markdown("***")

    st.header("""
		Form Jantung
	""")

    display_cp = st.checkbox("Apakah anda mengalami sakit di dada atau bagian tubuh lain? Centang jika iya")
    cp = 3
    if display_cp:
        pilih_cp = st.radio("Pilih jenis sakit yang anda rasakan :",options=['Sakit di dada ketika lelah (Typical Angina / Angin Duduk)',
                                                                              'Sakit di dada yang tidak stabil dan lebih parah (Atypical angina)',
                                                                              'Sakit di bagian tubuh lain (Non-anginal pain)'])
        if pilih_cp == 'Sakit di dada ketika lelah (Typical Angina / Angin Duduk)':
            cp = 0
        elif pilih_cp == 'Sakit di dada yang tidak stabil dan lebih parah (Atypical angina)':
            cp = 1
        elif pilih_cp == 'Sakit di bagian tubuh lain (Non-anginal pain)':
            cp = 2
    col1, col2, col3 = st.columns(3)
    with col1:
        trestbps = st.number_input("Masukkan tekanan darah sistolik :",50,300,120)
    with col2:
        bp = st.number_input("Masukkan tekanan darah diastolik :",20,150,80)
    with col3:
        "Tekanan Darah Anda"
        trestbps, "/", bp
    if trestbps <= 140 and bp <= 80:
        hypertension = 0
    else:
        hypertension = 1
    chol = st.number_input("Masukkan kadar kolesterol anda (mg/dl) :",100,400,190)
    glucose = st.number_input("Masukkan rata-rata kadar gula anda (mg/ml) :",10.0,300.0,120.0)
    avg_glucose_level = int(glucose)
    if glucose <= 120.0 :
        fbs = 0
    else:
        fbs = 1
    display_restecg = st.checkbox("Apakah anda pernah melakukan pemeriksaan elektrokardiografi / rekam jantung? Centang jika iya")
    restecg = 0
    slope = 2
    ca = 0
    oldpeak = 1.0
    if display_restecg:
        pilih_restecg = st.radio("Bagaimana hasil elektrokardiografi anda : ",options=['Normal',
                                                                                       'Terdapat gelombang yang tidak wajar',
                                                                                       'Menunjukan kemungkinan pembesaran bilik kiri jantung'])
        if pilih_restecg == 'Normal':
            restecg = 0
        elif pilih_restecg == 'Terdapat gelombang yang tidak wajar':
            restecg = 1
        elif pilih_restecg == 'Menunjukan kemungkinan pembesaran bilik kiri jantung':
            restecg = 2
        pilih_slope = st.radio("Bagaimana bentuk segmen ST setelah kurva :", options=['Menanjak (Upsloping)',
                                                                                      'Mendatar (Flat)',
                                                                                      'Menurun (Downsloping)'])
        if pilih_slope == 'Menanjak (Upsloping)':
            slope = 1
        elif pilih_slope == 'Mendatar (Flat)':
            slope = 2
        elif pilih_slope == 'Menurun (Downsloping)':
            slope = 3
        ca = st.number_input("Jumlah pembuluh darah yang diwarnai dengan fluoroskopi :", 0, 3, 1)
        oldpeak = st.number_input("Masukkan nilai selisih ST depresi sebeluh dan setelah berolahraga : ",0.0,10.0,1.0)
    thalach = st.number_input("Masukkan detak jantung tertinggi anda setelah berolahraga (per Menit) : ",20,220,170)
    pilih_exang = st.checkbox("Apakah ketika melakukan aktivitas fisik berat seperti olahraga, dada anda terasa sakit? Centang jika iya")
    exang = 0
    if pilih_exang:
        exang = 1
    display_thal = st.checkbox("Apakah anda pernah memiliki kelainan thalassemia / kerusakan pembuluh darah? Centang jika iya")
    thal = 0
    if display_thal:
        pilih_thal = st.checkbox("Apakah kelainan anda permanen? Centang jika iya")
        thal = 2
        if pilih_thal:
            thal = 1

    st.markdown("***")

    st.header("""
		Form Diabetes
	""")

    pregnancies = 0
    if sex == 0:
        display_pregnancies = st.checkbox("Apakah anda pernah mengalami kehamilan? Centang jika iya")
        if display_pregnancies:
            pregnancies = st.number_input("Berapa kali anda mengalami kehamilan?", 1, 20, 1)

    display_skinthickness = st.checkbox("Apakah anda mengetahui berapa ketebalan lipatan kulit trisep (TSFT) anda? Centang jika iya")
    if sex == 1:
        skinthickness = 12
    else:
        skinthickness = 23
    if display_skinthickness:
        skinthickness = st.number_input("Berapa ketebalan lipatan kulit trisep (TSFT) anda (mm)?",1,100,20)

    display_insulin = st.checkbox("Apakah anda mengetahui kadar insulin dalam tubuh anda? Centang jika iya")
    insulin = 125
    if display_insulin:
        insulin = st.number_input("Berapa kadar insulin dalam tubuh anda?", 1, 300, 125)

    pilih_dpf = st.checkbox("Apakah keluarga anda memiliki riwayat diabetes? Centang jika iya")
    dpf = 0
    if pilih_dpf:
        dpf = 1

    st.markdown("***")

    st.header("""
        Form Stroke
    """)

    pilih_evermarried = st.radio("Pilih status pernikahan anda :",
                        options=['Belum menikah',
                                 'Sudah atau pernah menikah'])
    if pilih_evermarried == 'Belum menikah':
        evermarried = 0
    elif pilih_evermarried == 'Sudah atau pernah menikah':
        evermarried = 1

    pilih_work_type = st.radio("Pilih jenis pekerjaan anda :",
                                 options=['Belum pernah bekerja',
                                          'Masih anak-anak',
                                          'Pegawai pemerintah',
                                          'Wiraswasta',
                                          'Pekerja serabutan'])
    if pilih_work_type == 'Belum pernah bekerja':
        work_type = 4
    elif pilih_work_type == 'Masih anak-anak':
        work_type = 3
    elif pilih_work_type == 'Pegawai pemerintah':
        work_type = 2
    elif pilih_work_type == 'Wiraswasta':
        work_type = 1
    elif pilih_work_type == 'Pekerja serabutan':
        work_type = 0

    pilih_residence_type = st.radio("Pilih area tempat tinggal anda :",
                                 options=['Perkotaan',
                                          'Pedesaan'])
    if pilih_residence_type == 'Perkotaan':
        residence_type = 0
    elif pilih_residence_type == 'Pedesaan':
        residence_type = 1

    pilih_smoking_status = st.radio("Pilih status merokok anda :",
                                    options=['Tidak pernah merokok',
                                             'Pernah merokok',
                                             'Merokok'])
    if pilih_smoking_status == 'Tidak pernah merokok':
        smoking_status = 0
    elif pilih_smoking_status == 'Pernah merokok':
        smoking_status = 1
    elif pilih_smoking_status == 'Merokok':
        smoking_status = 2

    datapengguna = []
    # "Diabetes"
    # st.write(pregnancies, glucose, bp, skinthickness, insulin, bmi, dpf, age)
    data_d = [pregnancies, glucose, bp, skinthickness, insulin, bmi, dpf, age]
    datapengguna.append(data_d)
    # "Jantung"
    # st.write(age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal)
    data_h = [age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]
    datapengguna.append(data_h)
    # "Stroke"
    # st.write(sex, age, hypertension,evermarried,work_type,residence_type,avg_glucose_level,bmi,smoking_status)
    data_s = [sex, age, hypertension,evermarried,work_type,residence_type,avg_glucose_level,bmi,smoking_status]
    datapengguna.append(data_s)

    butt = st.button('Prediksi')
    if butt:
        if name:
            data_d, data_h, data_s =normalize_data(datapengguna, scaler, model_h)
            prediksi_diabetes = predict_diabetes(data_d, model_d)
            prediksi_heart = predict_heart(data_h, model_h)
            prediksi_stroke = predict_stroke(data_s, model_s)
            # prediksi_diabetes, prediksi_heart, prediksi_stroke = predict_request('http://466e-34-147-70-188.ngrok.io/predict',datapengguna)
            # st.write(prediksi_diabetes," ", prediksi_heart, " ", prediksi_stroke)
            rekomendasi(name,prediksi_diabetes, prediksi_heart, prediksi_stroke)
        else:
            st.warning('Tolong masukkan nama anda.')
            st.stop()

if __name__ == "__main__":
	main()