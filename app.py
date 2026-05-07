import streamlit as st
from docxtpl import DocxTemplate
import io
import os

# Налаштування сторінки
st.set_page_config(page_title="Генератор Рапортів", page_icon="📄")
st.title("📝 Формування рапорту")

# 1. СПИСОК ШАБЛОНІВ
templates = {
    "Рекомендаційний лист ЗСУ": "recommendation_template.docx",
    "Рекомендаційний лист НГУ": "recommendation_template_ngu.docx"
}

selected_label = st.selectbox("Оберіть тип документа:", list(templates.keys()))
TEMPLATE_FILE = templates[selected_label]

# Перевірка наявності файлу
if not os.path.exists(TEMPLATE_FILE):
    st.error(f"❌ Файл '{TEMPLATE_FILE}' не знайдено на GitHub!")
    st.stop()

st.write(f"Вибрано шаблон: **{selected_label}**")

# 2. ФОРМА ВВОДУ ДАНИХ
with st.form("raport_form"):
    
    # Блок 1: Персональні дані
    st.header("👤 1. Персональні дані")
    col1, col2 = st.columns(2)
    with col1:
        pib = st.text_input("ПІБ (Називний)", placeholder="Баришич Лука Маріянович")
        pib_rod = st.text_input("ПІБ (Родовий - кого?)", placeholder="Баришича Луки Маріяновича")
        zvannia = st.text_input("Звання (Називний)", placeholder="солдат")
        zvannia_rod = st.text_input("Звання (Родовий)", placeholder="солдата")
    with col2:
        rnokpp = st.text_input("РНОКПП", placeholder="3513609410")
        birth_date = st.text_input("Дата народження", placeholder="13.03.1996")
        education = st.text_input("Освіта", placeholder="НТУУ 'КПІ', 2024")
        service_start = st.text_input("У ЗСУ з", placeholder="30.11.2024")
        combat_history = st.text_input("Періоди участі у бойових діях", placeholder="30.11.2024-30.11.2025")

    # Блок 2: Т.В.О. та Додаткове поле
    st.header("⚙️ 2. Додаткові реквізити")
    c1, c2 = st.columns(2)
    with c1:
        new_field_1 = st.text_input("Т.в.о. (Прізвище, ініціали)")
    with c2:
        new_field_2 = st.text_input("Звання")

    # Блок 3: Дані про посади
    st.header("🎯 3. Інформація про посади")
    pos_col1, pos_col2 = st.columns(2)
    
    with pos_col1:
        st.markdown("**Вакантна посада**")
        v_unit = st.text_input("В/ч (куди призначають)")
        v_position = st.text_area("Повне найменування посади (вак.)")
        v_shpk = st.text_input("ШПК (вак.)")
        v_vos = st.text_input("ВОС (вак.)")
        v_tarif = st.text_input("Тариф (вак.)")
        v_salary = st.text_input("Оклад (вак.)")
        
    with pos_col2:
        st.markdown("**Поточна посада**")
        c_unit = st.text_input("В/ч (зараз)")
        c_position = st.text_area("Повне найменування посади (зараз)")
        c_shpk = st.text_input("ШПК (зараз)")
        c_vos = st.text_input("ВОС (зараз)")
        c_tarif = st.text_input("Тариф (зараз)")
        c_salary = st.text_input("Оклад (зараз)")

    submit_button = st.form_submit_button(label="⚡ Згенерувати .docx")

# 3. ЛОГІКА ГЕНЕРАЦІЇ
if submit_button:
    try:
        context = {
            'pib': pib, 'pib_rod': pib_rod, 
            'ceo': new_field_1, 
            'position': new_field_2,
            'zvannia': zvannia, 'zvannia_rod': zvannia_rod,
            'rnokpp': rnokpp, 'birth_date': birth_date,
            'education': education, 'service_start': service_start,
            'new_var_1': new_field_1, 
            'new_var_2': new_field_2, 
            'v_unit': v_unit, 'v_position': v_position, 'v_shpk': v_shpk, 
            'v_vos': v_vos, 'v_tarif': v_tarif, 'v_salary': v_salary,
            'c_unit': c_unit, 'c_position': c_position, 'c_shpk': c_shpk, 
            'combat_history': combat_history,
            'c_vos': c_vos, 'c_tarif': c_tarif, 'c_salary': c_salary
        }

        doc = DocxTemplate(TEMPLATE_FILE)
        doc.render(context)

        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.success(f"✅ Документ за шаблоном '{selected_label}' готовий!")
        
        st.download_button(
            label="⬇️ Скачати результат",
            data=buffer,
            file_name=f"Рапорт_{pib.split()[0] if pib else 'файл'}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"Сталася помилка: {e}")
