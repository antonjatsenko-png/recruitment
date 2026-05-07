import streamlit as st
from docxtpl import DocxTemplate
import io
import os

# Налаштування сторінки
st.set_page_config(page_title="Генератор Рапортів", page_icon="📄")
st.title("📝 Формування рапорту")

# 1. СПИСОК ШАБЛОНІВ
# Додайте сюди назви файлів так, як вони підписані у вас на GitHub
templates = {
    "Рекомендаційний лист ЗСУ": "recommendation_template.docx",
    "Рекомендаційний лист НГУ": "recommendation_template_ngu.docx"
}

selected_label = st.selectbox("Оберіть тип документа:", list(templates.keys()))
TEMPLATE_FILE = templates[selected_label]

# Перевірка наявності файлу на сервері
if not os.path.exists(TEMPLATE_FILE):
    st.error(f"❌ Файл '{TEMPLATE_FILE}' не знайдено на GitHub!")
    st.info("Завантажте файл у репозиторій або перевірте правильність назви в коді.")
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

    # Блок 2: Нові поля (редагуйте назви тут)
    st.header("⚙️ 2. Додаткові поля")
    new_field_1 = st.text_input("Нове поле 1 (наприклад: Поточний підрозділ)")
    new_field_2 = st.text_area("Нове поле 2 (наприклад: Додаткова інформація)")

    # Блок 3: Дані про посади
    st.header("🎯 3. Інформація про посади")
    with st.expander("Розгорнути для заповнення деталей посад"):
        v_unit = st.text_input("В/ч (куди призначають)")
        v_position = st.text_area("Посада (вакантна)")
        v_shpk = st.text_input("ШПК (вак.)")
        v_vos = st.text_input("ВОС (вак.)")
        v_tarif = st.text_input("Тариф (вак.)")
        v_salary = st.text_input("Оклад (вак.)")
        
        st.divider()
        
        c_unit = st.text_input("В/ч (зараз)")
        c_position = st.text_area("Посада (зараз)")
        c_shpk = st.text_input("ШПК (зараз)")
        c_vos = st.text_input("ВОС (зараз)")
        c_tarif = st.text_input("Тариф (зараз)")
        c_salary = st.text_input("Оклад (зараз)")

    submit_button = st.form_submit_button(label="⚡ Згенерувати .docx")

# 3. ЛОГІКА ГЕНЕРАЦІЇ
if submit_button:
    try:
        # Формуємо словник для Word (назви зліва — це те, що в {{ }} в Word)
        context = {
            'pib': pib, 'pib_rod': pib_rod, 
            'zvannia': zvannia, 'zvannia_rod': zvannia_rod,
            'rnokpp': rnokpp, 'birth_date': birth_date,
            'education': education, 'service_start': service_start,
            'new_var_1': new_field_1, # В Word пишемо {{ new_var_1 }}
            'new_var_2': new_field_2, # В Word пишемо {{ new_var_2 }}
            'v_unit': v_unit, 'v_position': v_position, 'v_shpk': v_shpk, 
            'v_vos': v_vos, 'v_tarif': v_tarif, 'v_salary': v_salary,
            'c_unit': c_unit, 'c_position': c_position, 'c_shpk': c_shpk, 
            'c_vos': c_vos, 'c_tarif': c_tarif, 'c_salary': c_salary
        }

        # Завантаження та обробка обраного шаблону
        doc = DocxTemplate(TEMPLATE_FILE)
        doc.render(context)

        # Передача файлу в пам'ять
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
