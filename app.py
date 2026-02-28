import streamlit as st
from docxtpl import DocxTemplate
import io
import os

# Налаштування сторінки
st.set_page_config(page_title="Генератор Рапортів", page_icon="📄")

st.title("📝 Формування рапорту")

# --- ПЕРЕВІРКА ФАЙЛУ ШАБЛОНУ ---
TEMPLATE_FILE = "recommendation_template.docx"

if not os.path.exists(TEMPLATE_FILE):
    st.error(f"❌ Помилка: Файл '{TEMPLATE_FILE}' не знайдено на GitHub!")
    st.info("Будь ласка, завантажте ваш шаблон Word у той же репозиторій, де лежить цей код.")
    st.stop()

st.write("Заповніть дані нижче для автоматичного заповнення таблиці:")

# --- ФОРМА ВВОДУ ДАНИХ ---
with st.form("raport_form"):
    
    # Блок 1: Персональні дані
    st.header("👤 1. Персональні дані кандидата")
    col1, col2 = st.columns(2)
    
    with col1:
        pib = st.text_input("Прізвище, ім'я, по батькові", placeholder="Баришич Лука Маріянович")
        pib_rod = st.text_input("Прізвище, ім'я, по батькові", placeholder="Баришич Лука Маріянович")
        zvannia = st.text_input("Військове звання", placeholder="солдат")
        zvannia_rod = st.text_input("Військове звання", placeholder="солдат")
        rnokpp = st.text_input("РНОКПП (ІПН)", placeholder="3513609410")
        birth_date = st.text_input("Дата народження", placeholder="13.03.1996")
    
    with col2:
        education = st.text_input("Освіта, рік закінчення", placeholder="НТУУ 'КПІ', 2024")
        service_start = st.text_input("У ЗСУ з", placeholder="30.11.2024")
        combat_history = st.text_area("Періоди участі в бойових діях", value="не приймав")

    st.divider()

    # Блок 2: Вакантна посада
    st.header("🎯 2. Інформація про вакантну посаду")
    v_unit = st.text_input("Військова частина (куди призначають)", placeholder="3027 ОТЗ – 1-го корпусу НГУ «Азов»")
    v_position = st.text_area("Повне найменування посади (вакантна)")
    
    v_col1, v_col2, v_col3 = st.columns(3)
    with v_col1:
        v_shpk = st.text_input("ШПК посади (вак.)", placeholder="солдат")
        v_vos = st.text_input("ВОС посади (вак.)", placeholder="547543П")
    with v_col2:
        v_tarif = st.text_input("Тарифний розряд (вак.)", placeholder="4/3")
        v_salary = st.text_input("Посадовий оклад (вак.)", placeholder="2730")
    with v_col3:
        v_staff = st.text_input("Штат (вак.)", placeholder="04/1925???")

    st.divider()

    # Блок 3: Поточна посада
    st.header("🏢 3. Інформація про поточну посаду")
    c_unit = st.text_input("Військова частина (зараз)", placeholder="А4799")
    c_position = st.text_area("Повне найменування посади (зараз)")
    
    c_col1, c_col2 = st.columns(2)
    with c_col1:
        c_shpk = st.text_input("ШПК посади (зараз)", placeholder="солдат")
        c_vos = st.text_input("ВОС посади (зараз)", placeholder="101533А")
    with c_col2:
        c_tarif = st.text_input("Тарифний розряд (зараз)", placeholder="3")
        c_salary = st.text_input("Посадовий оклад (зараз)", placeholder="2640")

    # Кнопка відправки
    submit_button = st.form_submit_button(label="⚡ Згенерувати .docx файл")

# --- ЛОГІКА ГЕНЕРАЦІЇ ---
if submit_button:
    try:
        # Створюємо словник даних
        context = {
            'pib': pib, 'pib_rod': pib_rod, 'zvannia': zvannia, 'zvannia_rod': zvannia_rod, 'rnokpp': rnokpp, 'birth_date': birth_date,
            'education': education, 'service_start': service_start, 'combat_history': combat_history,
            'v_unit': v_unit, 'v_position': v_position, 'v_shpk': v_shpk, 'v_vos': v_vos,
            'v_tarif': v_tarif, 'v_salary': v_salary, 'v_staff': v_staff,
            'c_unit': c_unit, 'c_position': c_position, 'c_shpk': c_shpk,
            'c_vos': c_vos, 'c_tarif': c_tarif, 'c_salary': c_salary
        }

        # Завантажуємо та рендеримо
        doc = DocxTemplate(TEMPLATE_FILE)
        doc.render(context)

        # Зберігаємо у байтовий потік (щоб не створювати файли на сервері)
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.success("✅ Документ успішно сформовано!")
        
        # Кнопка скачування
        st.download_button(
            label="⬇️ Скачати готовий рапорт",
            data=buffer,
            file_name=f"Рапорт_{pib.split()[0] if pib else 'кандидата'}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except Exception as e:
        st.error(f"Виникла помилка: {e}")
