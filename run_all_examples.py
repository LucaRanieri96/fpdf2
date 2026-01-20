#!/usr/bin/env python3
"""
Script per eseguire tutti gli esempi e generare tutti i PDF
"""
import os
import sys
from pathlib import Path

# Aggiungi la directory examples al path
examples_dir = Path(__file__).parent / "examples"
sys.path.insert(0, str(examples_dir))

def run_all_examples():
    """Esegue tutti gli esempi nella cartella examples"""
    
    examples = [
        ("01_hello_world", "Hello World - Il primo PDF"),
        ("02_basic_formatting", "Formattazione base del testo"),
        ("03_table_example", "Tabelle"),
        ("04_multi_page", "Multi-pagina con header/footer"),
        ("05_shapes_and_colors", "Forme e colori"),
    ]
    
    print("=" * 60)
    print("ESECUZIONE ESEMPI FPDF2")
    print("=" * 60)
    print()
    
    for module_name, description in examples:
        print(f"📄 {description}...")
        try:
            module = __import__(module_name)
            # Esegui la funzione principale del modulo
            if hasattr(module, f'create_{module_name[3:]}'):
                func = getattr(module, f'create_{module_name[3:]}')
                func()
            else:
                # Prova con altri nomi comuni
                for func_name in dir(module):
                    if func_name.startswith('create_'):
                        func = getattr(module, func_name)
                        if callable(func):
                            func()
                            break
        except Exception as e:
            print(f"   ❌ Errore: {e}")
        print()
    
    print("=" * 60)
    print("✅ Fatto! Controlla la cartella 'output/' per i PDF generati")
    print("=" * 60)

if __name__ == "__main__":
    # Cambia directory alla root del progetto
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    run_all_examples()
