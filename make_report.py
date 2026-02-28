import os
from datetime import datetime
from docxtpl import DocxTemplate

def get_input(prompt, default=""):
    user_input = input(f"{prompt} {f'[{default}]' if default else ''}: ").strip()
    return user_input if user_input else default

def main():
    template_path = "recommendation_template.docx"
    
    if not os.path.exists(template_path):
        print(f"Помилка: Файл '{template_path}' не знайдено!")
        print("Створіть Word-файл з назвою template.docx у цій же папці.")
        return

    print("=== АВТОМАТИЗАЦІЯ РАПОРТУ ===")
    print("Введіть дані (натисніть Enter, щоб залишити пустим або використати значення в дужках):")
    
    context = {}

    # Блок 1: Персональні дані
    print("\n--- ПЕРСОНАЛЬНІ ДАНІ КАНДИДАТА ---")
    context['pib'] = get_input("Прізвище, ім'я, по батькові")
    context['pib_rod'] = get_input("Прізвище, ім'я, по батькові (родовий)")
    context['zvannia'] = get_input("Військове звання")
    context['zvannia_rod'] = get_input("Військове звання (родовий)")
    context['rnokpp'] = get_input("РНОКПП")
    context['birth_date'] = get_input("Дата народження")
    context['education'] = get_input("Освіта, рік закінчення")
    context['service_start'] = get_input("У ЗСУ з")
    context['combat_history'] = get_input("Участь у бойових діях", "не приймав")

    # Блок 2: Вакантна посада
    print("\n--- ІНФОРМАЦІЯ ПРО ВАКАНТНУ ПОСАДУ ---")
    context['v_position'] = get_input("Повне найменування посади")
    context['v_shpk'] = get_input("ШПК посади")
    context['v_vos'] = get_input("ВОС посади")
    context['v_tarif'] = get_input("Тарифний розряд")
    context['v_salary'] = get_input("Посадовий оклад")
    context['v_staff'] = get_input("Штат")

    # Блок 3: Поточна посада
    print("\n--- ІНФОРМАЦІЯ ПРО ПОТОЧНУ ПОСАДУ ---")
    context['c_unit'] = get_input("Військова частина (зараз)")
    context['c_position'] = get_input("Повне найменування посади")
    context['c_shpk'] = get_input("ШПК посади")
    context['c_vos'] = get_input("ВОС посади")
    context['c_tarif'] = get_input("Тарифний розряд")
    context['c_salary'] = get_input("Посадовий оклад")

    # Генерація
    print("\nГенерація документа...")
    try:
        doc = DocxTemplate(template_path)
        doc.render(context)
        
        # Назва файлу за прізвищем
        last_name = context['pib'].split()[0] if context['pib'] else "raport"
        timestamp = datetime.now().strftime("%H%M")
        output_name = f"Рапорт_{last_name}_{timestamp}.docx"
        
        doc.save(output_name)
        print(f"Успішно! Файл збережено: {output_name}")
        
        # Автоматичне відкриття файлу на Mac
        os.system(f"open '{output_name}'")
        
    except Exception as e:
        print(f"Сталася помилка при збереженні: {e}")

if __name__ == "__main__":
    main()