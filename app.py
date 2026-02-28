import streamlit as st
from docxtpl import DocxTemplate
import io

st.set_page_config(page_title="Генератор Рапортів", layout="centered")

st.header("📋 Формування рапорту")

# Створюємо форму для введення
with st.form("raport_form"):
    pib = st.text_input("ПІБ кандидата")
    zvannia = st.text_input("Звання")
    # Додайте тут інші поля за зразком...
    
    submitted = st.form_submit_button("Згенерувати документ")

if submitted:
    if not pib:
        st.error("Будь ласка, введіть ПІБ")
    else:
        # Завантажуємо шаблон (він має лежати в тому ж репозиторії)
        doc = DocxTemplate("template.docx")
        context = {
            'pib': pib,
            'zvannia': zvannia,
            # ... допишіть решту полів
        }
        
        doc.render(context)
        
        # Зберігаємо результат у буфер пам'яті
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        st.success("Рапорт готовий до скачування!")
        st.download_button(
            label="⬇️ Скачати рапорт (.docx)",
            data=buffer,
            file_name=f"Рапорт_{pib.replace(' ', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
