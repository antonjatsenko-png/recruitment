import streamlit as st
from docxtpl import DocxTemplate
import io
import os

# Налаштування сторінки
st.set_page_config(page_title="Генератор Рапортів", page_icon="📄")

st.title("📝 Формування рапорту")

# Дивимось, які файли бачить сервер (для відладки)
# st.write("Файли в репозиторії:", os.listdir(".")) 

# Шлях до шаблону - ПЕРЕВІРТЕ ЦЮ НАЗВУ!
TEMPLATE_FILE = "recommendation_template.docx"

if not os.path.exists(TEMPLATE_FILE):
    st.error(f"❌ Помилка: Файл '{TEMPLATE_FILE}' не знайдено на GitHub!")
    st.info("Переконайтеся, що файл завантажений у корінь репозиторія і назва збігається символ в символ.")
    st.stop()

st.write("Заповніть дані нижче:")

with st.form("raport_form"):
    st.header("👤 1. Персональні дані кандидата")
    col1, col2 = st.columns(2)
    
    with col1:
        pib = st.text_input("ПІБ (Називний)", placeholder="Баришич Лука Маріянович")
        pib_rod = st.text_input("ПІБ (Родовий - кого?)", placeholder="Баришича Луки Маріяновича")
        zvannia = st.text_input("Звання (Називний)", placeholder="солдат")
        zvannia_rod = st.text_input("Звання (Родовий)", placeholder="солдата")
        rnokpp = st.text_input("РНОКПП", placeholder="3513609410")
        birth_date = st.text_input("Дата народження", placeholder="13.03.1996")
    
    with col2:
        education = st.text_input("Освіта", placeholder="НТУУ 'КПІ', 2024")
        service_start = st.text_input("У ЗСУ з", placeholder="30.11.2024")
        combat_history = st.text_area("Бойові дії", value="не приймав")

    st.divider()

    st.header("🎯 2. Вакантна посада")
    v_unit = st.text_input("В/ч (куди)", placeholder="3027 ОТЗ")
    v_position = st.text_area("Назва посади (вак.)")
    
    v_c1, v_c2, v_c3 = st.columns(3)
    with v_c1:
        v_shpk = st.text_input("ШПК (вак.)")
        v_vos = st.text_input("ВОС (вак.)")
    with v_c2:
        v_tarif = st.text_input("Тариф (вак.)")
        v_salary = st.text_input("Оклад (вак.)")
    with v_c3:
        v_staff = st.text_input("Штат (вак.)")

    st.divider()

    st.header("🏢 3. Поточна посада")
    c_unit = st.text_input("В/ч (зараз)")
    c_position = st.text_area("Назва посади (зараз)")
    
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        c_shpk = st.text_input("ШПК (зараз)")
        c_vos = st.text_input("ВОС (зараз)")
    with c_col2:
        c_tarif = st.text_input("Тариф (зараз)")
        c_salary = st.text_input("Оклад (зараз)")

    submit_button = st.form_submit_button(label="⚡ Згенерувати .docx")

if submit_button:
    try:
        context = {
            'pib': pib, 'pib_rod': pib_rod, 'zvannia': zvannia, 'zvannia_rod': zvannia_rod,
            'rnokpp': rnokpp, 'birth_date': birth_date, 'education': education,
            'service_start': service_start, 'combat_history': combat_history,
            'v_unit': v_unit, 'v_position': v_position, 'v_shpk': v_shpk, 'v_vos': v_vos,
            'v_tarif': v_tarif, 'v_salary': v_salary, 'v_staff': v_staff,
            'c_unit': c_unit, 'c_position': c_position, 'c_shpk': c_shpk,
            'c_vos': c_vos, 'c_tarif': c_tarif, 'c_salary': c_salary
        }

        doc = DocxTemplate(TEMPLATE_FILE)
        doc.render(context)

        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.success("✅ Готово!")
        st.download_button(
            label="⬇️ Скачати",
            data=buffer,
            file_name=f"Рапорт_{pib.split()[0] if pib else 'документ'}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"Помилка при генерації: {e}")
