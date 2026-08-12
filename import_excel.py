import pandas as pd
import database as db
import os

# Excel fayldan ma'lumotlarni o'qish va bazaga yozish dasturi
EXCEL_FILE = 'savollar.xlsx'

def import_from_excel():
    if not os.path.exists(EXCEL_FILE):
        print(f"XATOLIK: {EXCEL_FILE} fayli topilmadi!")
        print("Iltimos, ushbu papkada 'savollar.xlsx' nomli fayl yarating.")
        print("Ustunlar: 'Savol', 'Variant 1', 'Variant 2', 'Variant 3', 'Variant 4', 'Togri javob (1-4)'")
        return

    try:
        df = pd.read_excel(EXCEL_FILE)
        added_count = 0
        
        for index, row in df.iterrows():
            question = str(row['Savol']).strip()
            
            # Variantlarni yig'ish (bo'sh bo'lmaganlarini)
            options = []
            for i in range(1, 5):
                col_name = f'Variant {i}'
                if col_name in df.columns and not pd.isna(row[col_name]):
                    options.append(str(row[col_name]).strip())
            
            try:
                correct_id = int(row['Togri javob (1-4)']) - 1 # Array 0 dan boshlanadi (0, 1, 2, 3)
            except (ValueError, TypeError):
                print(f"[{index+1}-qator] To'g'ri javob raqamida xatolik bor. O'tkazib yuborildi.")
                continue
                
            if len(options) < 2:
                print(f"[{index+1}-qator] Savolda kamida 2 ta variant bo'lishi kerak. O'tkazib yuborildi.")
                continue
                
            if not (0 <= correct_id < len(options)):
                print(f"[{index+1}-qator] To'g'ri javob raqami (1-4) variantlar soniga mos tushmadi. O'tkazib yuborildi.")
                continue

            # Bazaga qo'shish
            success = db.add_question(question, options, correct_id)
            if success:
                added_count += 1
                
        print(f"Muvaffaqiyatli! {added_count} ta yangi savol bazaga qo'shildi.")
        stats = db.get_stats()
        print(f"Bazada jami {stats['total']} ta savol mavjud.")
        
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

if __name__ == '__main__':
    db.init_db()
    import_from_excel()
