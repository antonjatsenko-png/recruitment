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
    "Рекомендаційний лист НГУ": "recommendation_template_ngu.docx",
    "Письмова згода (рапорт)": "Письмова згода.docx"
}

selected_label = st.selectbox("Оберіть тип документа:", list(templates.keys()))
TEMPLATE_FILE = templates[selected_label]

# Перевірка наявності файлу шаблону
if not os.path.exists(TEMPLATE_FILE):
    st.error(f"❌ Файл '{TEMPLATE_FILE}' не знайдено на GitHub!")
    st.info("Переконайтеся, що файл завантажений у корінь репозиторія і назва збігається символ в символ.")
    st.stop()

st.write(f"Вибрано шаблон: **{selected_label}**")

# 2. ФОРМА ВВОДУ ДАНИХ
with st.form("raport_form"):
    
    # Спільні поля для абсолютно всіх документів
    st.header("👤 Основні дані кандидата")
    col_main1, col_main2 = st.columns(2)
    with col_main1:
        pib = st.text_input("ПІБ кандидата (Називний відмінок)", placeholder="Баришич Лука Маріянович")
    with col_main2:
        zvannia = st.text_input("Звання кандидата (Називний відмінок)", placeholder="солдат")

    st.divider()

    # --- ДИНАМІЧНИЙ ІНТЕРФЕЙС ЗАЛЕЖНО ВІД ШАБЛОНУ ---
    
    if selected_label == "Письмова згода (рапорт)":
        # ПОЛЯ ТІЛЬКИ ДЛЯ РАПОРТУ ПИСЬМОВОЇ ЗГОДИ
        st.header("📋 Анкета для письмової згоди (СЗЧ)")
        
        # ДОДАНО ПОЛЕ ДЛЯ ПОСАДИ, НА ЯКУ РОЗГЛЯДАЄТЬСЯ ЛЮДИНА
        target_position = st.text_area(
            "Посада, на яку розглядається людина (у родовому відмінку)", 
            value="старшого оператора відділення управління пункту управління батальйону безпілотних систем"
        )
        st.caption("Текст вище буде вставлено у фразу: '...для подальшого проходження служби на посаді [ваша посада] був відібраний...'")
        
        col_top1, col_top2 = st.columns(2)
        with col_top1:
            chief_rank = st.text_input("Звання командира (шапка)", value="полковнику")
            chief_name = st.text_input("Прізвище командира (шапка)", value="Владиславу СОЛОНЬКУ")
            age = st.text_input("Вік", placeholder="28 років")
            phone = st.text_input("Телефон користувача", placeholder="+380504403020")
        
        with col_top2:
            vch = st.text_input("В/ч (звідки людина в СЗЧ)", placeholder="А5002")
            health = st.text_input("Стан здоров'я", placeholder="Потребує уточнення (ВЛК), має проблеми з колінами")
            sud = st.text_input("Судимості", value="Відсутні")
            rus = st.text_input("Родичі на ТОТ", value="Відсутні")
            alco = st.text_input("Алкоголь / наркотики", placeholder="Алкоголь — інколи, поза службою; наркотики — не вживає.")
        
        st.subheader("📝 Досвід кандидата")
        war_exp = st.text_area("Бойовий досвід", placeholder="Роботіно, 2024р. піхота. Остання посада – пілот БПЛА")
        civil_exp = st.text_area("Цивільний досвід", placeholder="Директор промислового підприємства 3 роки, металургія. Освіта: вища...")
        
        st.subheader("✍️ Хто підписує клопотання внизу?")
        col_sign1, col_sign2 = st.columns(2)
        with col_sign1:
            sign_pos = st.text_input("Посада підписувача", value="Т. в. о. командира батальйону безпілотних систем")
            sign_rank = st.text_input("Звання підписувача", placeholder="підполковник")
        with col_sign2:
            sign_pib = st.text_input("Ім'я та Прізвище підписувача", placeholder="Артем ГНАТЮК")

    else:
        # ПОЛЯ ТІЛЬКИ ДЛЯ РЕКОМЕНДАЦІЙНИХ ЛИСТІВ (ЗСУ / НГУ)
        st.header("⚙️ Реквізити для рекомендаційного листа")
        
        col_rec1, col_rec2 = st.columns(2)
        with col_rec1:
            pib_rod = st.text_input("ПІБ кандидата (Родовий відмінок)", placeholder="Баришича Луки Маріяновича")
            zvannia_rod = st.text_input("Звання кандидата (Родовий відмінок)", placeholder="солдата")
            rnokpp = st.text_input("РНОКПП (ІПН)", placeholder="3513609410")
            birth_date = st.text_input("Дата народження", placeholder="13.03.1996")
        
        with col_rec2:
            education = st.text_input("Освіта", placeholder="НТУУ 'КПІ', 2024")
            service_start = st.text_input("У ЗСУ з (дата)", placeholder="30.11.2024")
            combat_history = st.text_area("Періоди участі у бойових діях", value="не приймав")

        st.subheader("🎯 Інформація про посади")
        pos_c1, pos_c2 = st.columns(2)
        with pos_c1:
            st.markdown("**🎯 Вакантна посада (куди)**")
            v_unit = st.text_input("В/ч (куди призначають)", placeholder="3027 ОТЗ")
            v_position = st.text_area("Повне найменування вакантної посади")
            v_shpk = st.text_input("ШПК (вакантна)")
            v_vos = st.text_input("ВОС (вакантна)")
            v_tarif = st.text_input("Тарифний розряд (вакантна)")
            v_salary = st.text_input("Посадовий оклад (вакантна)")
            v_staff = st.text_input("Штат (вакантна)")
        
        with pos_c2:
            st.markdown("**🏢 Поточна посада (зараз)**")
            c_unit = st.text_input("В/ч (де зараз служить)")
            c_position = st.text_area("Повне найменування поточної посади")
            c_shpk = st.text_input("ШПК (поточна)")
            c_vos = st.text_input("ВОС (поточна)")
            c_tarif = st.text_input("Тарифний розряд (поточна)")
            c_salary = st.text_input("Посадовий оклад (поточна)")

        st.subheader("✍️ Хто підписує рекомендацію?")
        col_rec_sign1, col_rec_sign2 = st.columns(2)
        with col_rec_sign1:
            new_field_1 = st.text_input("Т.в.о. / Командир (Прізвище, ініціали)", placeholder="Петренко І.І.")
        with col_rec_sign2:
            new_field_2 = st.text_input("Посада підписувача листа", placeholder="Командир військової частини А7777")

    submit_button = st.form_submit_button(label="⚡ Згенерувати документ")

# 3. ЛОГІКА ГЕНЕРАЦІЇ ПІСЛЯ НАТИСКАННЯ КНОПКИ
if submit_button:
    try:
        context = {
            # Мітки для "Письмової згоди"
            'target_position': target_position if 'target_position' in locals() else "",
            'chief_rank': chief_rank if 'chief_rank' in locals() else "",
            'chief_name': chief_name if 'chief_name' in locals() else "",
            'age': age if 'age' in locals() else "",
            'phone': phone if 'phone' in locals() else "",
            'vch': vch if 'vch' in locals() else "",
            'health': health if 'health' in locals() else "",
            'sud': sud if 'sud' in locals() else "",    
            'rus': rus if 'rus' in locals() else "",    
            'alco': alco if 'alco' in locals() else "", 
            'war_exp': war_exp if 'war_exp' in locals() else "",
            'civil_exp': civil_exp if 'civil_exp' in locals() else "",
            'sign_pos': sign_pos if 'sign_pos' in locals() else "",
            'sign_rank': sign_rank if 'sign_rank' in locals() else "",
            'sign_pib': sign_pib if 'sign_pib' in locals() else "",
            'PIB': pib,
            
            # Мітки для "Рекомендаційних листів"
            'pib': pib,
            'pib_rod': pib_rod if 'pib_rod' in locals() else "",
            'zvannia': zvannia,
            'zvannia_rod': zvannia_rod if 'zvannia_rod' in locals() else "",
            'rnokpp': rnokpp if 'rnokpp' in locals() else "",
            'birth_date': birth_date if 'birth_date' in locals() else "",
            'education': education if 'education' in locals() else "",
            'service_start': service_start if 'service_start' in locals() else "",
            'combat_history': combat_history if 'combat_history' in locals() else "",
            'v_unit': v_unit if 'v_unit' in locals() else "",
            'v_position': v_position if 'v_position' in locals() else "",
            'v_shpk': v_shpk if 'v_shpk' in locals() else "",
            'v_vos': v_vos if 'v_vos' in locals() else "",
            'v_tarif': v_tarif if 'v_tarif' in locals() else "",
            'v_salary': v_salary if 'v_salary' in locals() else "",
            'v_staff': v_staff if 'v_staff' in locals() else "",
            'c_unit': c_unit if 'c_unit' in locals() else "",
            'c_position': c_position if 'c_position' in locals() else "",
            'c_shpk': c_shpk if 'c_shpk' in locals() else "",
            'c_vos': c_vos if 'c_vos' in locals() else "",
            'c_tarif': c_tarif if 'c_tarif' in locals() else "",
            'c_salary': c_salary if 'c_salary' in locals() else "",
            'new_var_1': new_field_1 if 'new_field_1' in locals() else "",
            'new_var_2': new_field_2 if 'new_field_2' in locals() else ""
        }

        doc = DocxTemplate(TEMPLATE_FILE)
        doc.render(context)

        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.success(f"✅ Документ за шаблоном '{selected_label}' успішно створено!")
        
        last_name = pib.split()[0] if pib else "документ"
        st.download_button(
            label="⬇️ СКАЧАТИ ГОТОВИЙ ФАЙЛ (.DOCX)",
            data=buffer,
            file_name=f"{selected_label}_{last_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"Сталася критична помилка: {e}")
