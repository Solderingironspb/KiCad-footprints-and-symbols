import os
import sys
from pathlib import Path

def modify_simple(file_path):
    """
    Самая простая версия: ищем и заменяем по всему файлу
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Проверяем наличие слоя
        if '"F.CrtYd"' not in content:
            return "no_crtyd", "Файл не содержит слой F.CrtYd"
        
        # Считаем изменения
        width_before = content.count('(width 0.05)')
        layer_before = content.count('"F.CrtYd"')
        
        # Простая замена - сначала ширину, потом слой
        # Это безопасно, потому что width 0.05 есть только в элементах на F.CrtYd
        content = content.replace('(width 0.05)', '(width 0.1)')
        content = content.replace('"F.CrtYd"', '"F.SilkS"')
        
        # Считаем изменения после
        width_after = content.count('(width 0.1)')
        width_changes = width_before - (content.count('(width 0.05)'))
        layers_changed = layer_before
        
        # Записываем изменения
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return "modified", f"Ширина линий: {width_changes}, слоев: {layers_changed}"
        
    except Exception as e:
        return "error", f"Ошибка: {str(e)}"

def main_simple():
    """
    Самая простая основная функция
    """
    print("KiCad Layer Editor - Простая замена")
    print("=" * 50)
    print("Замена F.CrtYd на F.SilkS с width 0.05 → 0.1")
    print("=" * 50)
    
    # Тестируем на примере
    test_content = '''(fp_rect
    (start -6.83 -4)
    (end 6.83 4)
    (stroke
        (width 0.05)
        (type solid)
    )
    (fill no)
    (layer "F.CrtYd")
)'''
    
    print("Тест обработки:")
    print("ДО:")
    print(test_content)
    
    # Показываем, что будет
    test_result = test_content.replace('(width 0.05)', '(width 0.1)')
    test_result = test_result.replace('"F.CrtYd"', '"F.SilkS"')
    
    print("\nПОСЛЕ:")
    print(test_result)
    
    print("\n" + "=" * 50)
    
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
    print("-" * 50)
    
    stats = {"total": 0, "modified": 0, "no_changes": 0, "no_crtyd": 0, "errors": 0}
    
    for file_path in files:
        stats["total"] += 1
        print(f"\n{stats['total']}. Обработка: {file_path.name}")
        
        result, message = modify_simple(file_path)
        
        if result == "modified":
            stats["modified"] += 1
            print(f"  ✓ {message}")
        elif result == "no_changes":
            stats["no_changes"] += 1
            print(f"  ○ {message}")
        elif result == "no_crtyd":
            stats["no_crtyd"] += 1
            print(f"  - {message}")
        else:
            stats["errors"] += 1
            print(f"  ✗ {message}")
    
    print("\n" + "=" * 50)
    print("ИТОГИ:")
    print(f"Всего обработано: {stats['total']}")
    print(f"Изменено: {stats['modified']}")
    print(f"Без изменений: {stats['no_changes']}")
    print(f"Без слоя F.CrtYd: {stats['no_crtyd']}")
    print(f"Ошибок: {stats['errors']}")
    print("\nГотово!")

if __name__ == "__main__":
    main_simple()