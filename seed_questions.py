import database as db

# Boshlang'ich baza uchun tayyor savollar (Ilmiy, Diniy, Geografiya, Biologiya va Umumiy)
questions_data = [
    {"q": "Qur'oni Karimda nomi kelgan yagona sahoba kim?", "o": ["Abu Bakr (r.a)", "Umar (r.a)", "Zayd ibn Horisa (r.a)", "Ali (r.a)"], "c": 2},
    {"q": "Qaysi sayyora Quyosh atrofida eng tez aylanadi?", "o": ["Yer", "Merkuriy", "Venera", "Mars"], "c": 1},
    {"q": "O'zbekistondagi eng baland tog' cho'qqisi qaysi?", "o": ["Hazrati Sulton", "Bobotog'", "Adelung", "Beshbarmog'"], "c": 0},
    {"q": "Qon bosimini o'lchaydigan tibbiy asbob qanday ataladi?", "o": ["Termometr", "Tonometr", "Barometr", "Gidrometr"], "c": 1},
    {"q": "Dunyodagi eng katta quruqlik hayvoni qaysi?", "o": ["Jirafa", "Afrika fili", "Karkidon", "Oq ayiq"], "c": 1},
    {"q": "Atomning yadrosini nimalar tashkil etadi?", "o": ["Protonlar va Elektronlar", "Neytronlar va Elektronlar", "Protonlar va Neytronlar", "Faqat protonlar"], "c": 2},
    {"q": "O'zbekistonda eng katta maydonga ega viloyat qaysi?", "o": ["Navoiy", "Qashqadaryo", "Surxondaryo", "Qoraqalpog'iston"], "c": 0},
    {"q": "Qaysi qon guruhi 'Universal donor' hisoblanadi?", "o": ["I (O)", "II (A)", "III (B)", "IV (AB)"], "c": 0},
    {"q": "Dunyodagi eng katta ko'l qaysi?", "o": ["Baykal", "Kaspiy dengizi", "Viktoriya", "Orol"], "c": 1},
    {"q": "Suv qachon eng yuqori zichlikka ega bo'ladi?", "o": ["0°C da", "+4°C da", "+100°C da", "-4°C da"], "c": 1},
    {"q": "G'arbda 'Avitsenna' nomi bilan mashhur bo'lgan alloma kim?", "o": ["Al-Xorazmiy", "Abu Nasr Forobiy", "Abu Ali ibn Sino", "Beruniy"], "c": 2},
    {"q": "Islom tarixida birinchi bo'lib muazzinlik (azon aytish) qilgan sahoba kim?", "o": ["Bilol ibn Raboh", "Salmon Forsiy", "Umar ibn Xattob", "Ammor ibn Yosir"], "c": 0},
    {"q": "Dunyodagi eng uzun daryo qaysi?", "o": ["Amazonka", "Nil", "Yanszi", "Missisipi"], "c": 0},
    {"q": "Fotosintez jarayonida o'simlik qanday gazni yutadi?", "o": ["Kislorod", "Karbonat angidrid", "Azot", "Vodorod"], "c": 1},
    {"q": "Yorug'lik tezligi sekundiga necha kilometrga teng?", "o": ["150 000 km/s", "200 000 km/s", "300 000 km/s", "1 000 000 km/s"], "c": 2},
    {"q": "Inson tanasidagi eng kichik suyak qayerda joylashgan?", "o": ["Burunda", "Quloqda", "Barmoqda", "Tomoqda"], "c": 1},
    {"q": "Qur'oni Karimdagi eng uzun sura qaysi?", "o": ["Baqara", "Oli Imron", "Niso", "Moida"], "c": 0},
    {"q": "Renessans (Uyg'onish) davri ilk bor qaysi davlatda boshlangan?", "o": ["Ispaniya", "Fransiya", "Italiya", "Germaniya"], "c": 2},
    {"q": "Kompyuterning 'miyasi' qanday ataladi?", "o": ["Operativ xotira (RAM)", "Qattiq disk (HDD)", "Protsessor (CPU)", "Videokarta"], "c": 2},
    {"q": "Qaysi qush umuman ucha almaydi, lekin juda tez yuguradi?", "o": ["Tuyaqush", "Kivi", "Kazuari", "Pingvin"], "c": 0},
    {"q": "G'aznavilar davlatining eng kuchli hukmdori kim bo'lgan?", "o": ["Alptegin", "Sabuktegin", "Mahmud G'aznaviy", "Mas'ud G'aznaviy"], "c": 2},
    {"q": "DNK molekulasining tuzilishini kim kashf etgan?", "o": ["Mendel", "Darvin", "Uotson va Krik", "Paster"], "c": 2},
    {"q": "Islomning uchinchi ustuni (farzi) nima?", "o": ["Namoz o'qish", "Zakot berish", "Ro'za tutish", "Haj qilish"], "c": 1},
    {"q": "Koinotga birinchi bo'lib qaysi hayvon uchirilgan?", "o": ["Maymun", "It", "Mushuk", "Sichqon"], "c": 1},
    {"q": "O'zbekistonning poytaxti qachon Samarqanddan Toshkentga ko'chirilgan?", "o": ["1924 yil", "1930 yil", "1991 yil", "1918 yil"], "c": 1}
]

# Siz bu ro'yxatni minglab savollar bilan kengaytirishingiz mumkin.
# Yoki 'import_excel.py' orqali Excel'dan yuklashingiz mumkin.

def seed():
    db.init_db()
    added = 0
    for q in questions_data:
        success = db.add_question(q['q'], q['o'], q['c'])
        if success:
            added += 1
            
    print(f"{added} ta boshlang'ich savol bazaga yuklandi!")
    stats = db.get_stats()
    print(f"Hozirgi holat: {stats['total']} ta savol mavjud.")

if __name__ == '__main__':
    seed()
