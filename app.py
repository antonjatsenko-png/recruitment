import streamlit as st
from docxtpl import DocxTemplate
import io
import os

# Налаштування сторінки
st.set_page_config(page_title="Генератор Рапортів", page_icon="📄")
st.title("📝 Формування рапорту")

# 1. СПИСОК ШАБЛОНІВ
templates = {
    "Рекомендаційний лист (ЗСУ/НГУ)": "recommendation_template.docx",
    "Письмова згода (рапорт)": "Письмова згода.docx"
}

selected_label = st.selectbox("Оберіть тип документа:", list(templates.keys()))
TEMPLATE_FILE = templates[selected_label]

if not os.path.exists(TEMPLATE_FILE):
    st.error(f"❌ Файл '{TEMPLATE_FILE}' не знайдено на GitHub!")
    st.stop()

# 2. ФОРМА ВВОДУ ДАНИХ
with st.form("raport_form"):
    
    # Спільні поля для всіх документів
    st.header("👤 Основні дані кандидата")
    c_pib1, c_pib2 = st.columns(2)
    with c_pib1:
        pib = st.text_input("ПІБ (Називний)", placeholder="Баришич Лука Маріянович")
    with c_pib2:
        zvannia = st.text_input("Звання (Називний)", placeholder="солдат")

    # --- УМОВНИЙ ІНТЕРФЕЙС ---
    
    if selected_label == "Письмова згода (рапорт)":
        st.header("📋 Анкета для письмової згоди")
        
        col_top1, col_top2 = st.columns(2)
        with col_top1:
            chief_rank = st.text_input("Звання командира (шапка)", value="полковнику")
            chief_name = st.text_input("Прізвище командира (шапка)", value="Владиславу СОЛОНЬКУ")
            sign_rank = st.text_input("Звання того, хто клопоче", value="підполковник")
            sign_pos = st.text_input("Посада того, хто клопоче", placeholder="Т. в. о. командира батальйону безпілотних систем")
            sign_pib = st.text_input("Ім'я та прізвище того, хто клопоче", placeholder="Артем ГНАТЮК")
            age = st.text_input("Вік", placeholder="28 років")
            phone = st.text_input("Телефон", placeholder="+380504403020")
        with col_top2:
            vch = st.text_input("В/ч (звідки СЗЧ)", placeholder="А5002")
            health = st.text_input("Стан здоров'я", placeholder="Потребує уточнення (ВЛК), має проблеми з колінами")
            # --- ДОДАНО ЦІ ПОЛЯ ---
            sud = st.text_input("Судимості", value="Відсутні")
            rus = st.text_input("Родичі на ТОТ", value="Відсутні")
            alco = st.text_input("Алкоголь/наркотики", placeholder="Алкоголь — інколи, але поза службою; наркотики — не вживає.")
        
        war_exp = st.text_area("Бойовий досвід", placeholder="Роботіно, 2024р. піхота. Остання посада – пілот БПЛА")
        civil_exp = st.text_area("Цивільний досвід", placeholder="Директор промислового підприємства 3 роки, металургія; директор з продажів 3 роки. Освіта: вища (бакалавр, спеціаліст, магістр), Менеджмент та маркетинг.")

    else:
        # ПОКАЗУЄМО ТІЛЬКИ ДЛЯ РЕКОМЕНДАЦІЙНИХ ЛИСТІВ
        st.header("⚙️ Реквізити для рекомендації")
        
        col_rec1, col_rec2 = st.columns(2)
        with col_rec1:
            pib_rod = st.text_input("ПІБ (Родовий відмінок)")
            zvannia_rod = st.text_input("Звання (Родовий відмінок)")
            rnokpp = st.text_input("РНОКПП")
        with col_rec2:
            birth_date = st.text_input("Дата народження")
            education = st.text_input("Освіта")
            service_start = st.text_input("У ЗСУ з")

        st.subheader("🎯 Посади")
        pos_c1, pos_c2 = st.columns(2)
        with pos_c1:
            st.markdown("**Вакантна посада**")
            v_unit = st.text_input("В/ч (куди)")
            v_position = st.text_area("Назва посади (вак.)")
            v_shpk = st.text_input("ШПК (вак.)")
            v_vos = st.text_input("ВОС (вак.)")
        with pos_c2:
            st.markdown("**Поточна посада**")
            c_unit = st.text_input("В/ч (зараз)")
            c_position = st.text_area("Назва посади (зараз)")
            c_shpk = st.text_input("ШПК (зараз)")
            c_vos = st.text_input("ВОС (зараз)")

        new_field_1 = st.text_input("Т.в.о. (Прізвище, ініціали підписувача)")
        new_field_2 = st.text_input("Посада підписувача")

    submit_button = st.form_submit_button(label="⚡ Згенерувати документ")

# 3. ЛОГІКА ГЕНЕРАЦІЇ
if submit_button:
    try:
        # Створюємо словник, використовуючи значення або пусті рядки
        context = {
            # Для Згоди
            'chief_rank': chief_rank if 'chief_rank' in locals() else "",
            'chief_name': chief_name if 'chief_name' in locals() else "",
            'sign_rank': sign_rank if 'sign_rank' in locals() else "",
            'sign_pos': sign_pos if 'sign_pos' in locals() else "",
            'sign_pib': sign_pib if 'sign_pib' in locals() else "",
            'age': age if 'age' in locals() else "",
            'phone': phone if 'phone' in locals() else "",
            'vch': vch if 'vch' in locals() else "",
            'sud': sud if 'sud' in locals() else "",    
            'rus': rus if 'rus' in locals() else "",    
            'alco': alco if 'alco' in locals() else "", 
            'health': health if 'health' in locals() else "",
            'war_exp': war_exp if 'war_exp' in locals() else "",
            'civil_exp': civil_exp if 'civil_exp' in locals() else "",
            'PIB': pib,
            
            # Для Рекомендацій
            'pib': pib,
            'pib_rod': pib_rod if 'pib_rod' in locals() else "",
            'zvannia': zvannia,
            'zvannia_rod': zvannia_rod if 'zvannia_rod' in locals() else "",
            'rnokpp': rnokpp if 'rnokpp' in locals() else "",
            'birth_date': birth_date if 'birth_date' in locals() else "",
            'education': education if 'education' in locals() else "",
            'service_start': service_start if 'service_start' in locals() else "",
            'v_unit': v_unit if 'v_unit' in locals() else "",
            'v_position': v_position if 'v_position' in locals() else "",
            'v_shpk': v_shpk if 'v_shpk' in locals() else "",
            'v_vos': v_vos if 'v_vos' in locals() else "",
            'c_unit': c_unit if 'c_unit' in locals() else "",
            'c_position': c_position if 'c_position' in locals() else "",
            'new_var_1': new_field_1 if 'new_field_1' in locals() else "",
            'new_var_2': new_field_2 if 'new_field_2' in locals() else "",
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
            file_name=f"Документ_{pib.split()[0] if pib else 'файл'}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"Помилка: {e}")
