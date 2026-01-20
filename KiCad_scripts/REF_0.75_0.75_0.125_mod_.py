import os
import sys
from pathlib import Path

def modify_footprint_simple(file_path):
    """
    Простая версия модификации файла footprint
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        modified = False
        in_reference = False
        ref_modified = False
        
        for i, line in enumerate(lines):
            # Ищем начало Reference property
            if 'property "Reference"' in line:
                in_reference = True
                continue
            
            if in_reference:
                # Ищем блок font внутри Reference
                if '(font' in line and not ref_modified:
                    # Ищем следующие 2 строки с size и thickness
                    for j in range(i, min(i + 5, len(lines))):
                        if '(size 1 1)' in lines[j]:
                            lines[j] = lines[j].replace('(size 1 1)', '(size 0.75 0.75)')
                            modified = True
                        if '(thickness 0.15)' in lines[j]:
                            lines[j] = lines[j].replace('(thickness 0.15)', '(thickness 0.125)')
                            modified = True
                    ref_modified = True
                    in_reference = False
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(lines)
            return "modified", "Файл успешно изменен"
        else:
            return "no_changes", "Не найдены параметры для изменения"
            
    except Exception as e:
        return "error", f"Ошибка: {str(e)}"

def main_simple():
    """
    Упрощенная основная функция
    """
    print("KiCad Footprint Font Editor - Упрощенная версия")
    print("-" * 50)
    
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("Введите путь к файлу или папке: ").strip()
    
    path = Path(path)
    
    if path.is_file() and path.suffix == '.kicad_mod':
        files = [path]
    elif path.is_dir():
        files = list(path.glob("*.kicad_mod"))
    else:
        print("Ошибка: Неверный путь или тип файла")
        return
    
    if not files:
        print("Не найдено файлов .kicad_mod")
        return
    
    print(f"\nНайдено {len(files)} файлов для обработки")
    
    for file_path in files:
        print(f"\nОбработка: {file_path.name}")
        result, message = modify_footprint_simple(file_path)
        
        if result == "modified":
            print(f"  ✓ {message}")
        elif result == "no_changes":
            print(f"  ○ {message}")
        else:
            print(f"  ✗ {message}")
    
    print("\nГотово!")

if __name__ == "__main__":
    main_simple()