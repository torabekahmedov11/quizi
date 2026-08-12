import random
import database as db

# 1. Mamlakatlar va poytaxtlar (80 ta)
countries = {
    "O'zbekiston": "Toshkent", "Qozog'iston": "Ostona", "Qirg'iziston": "Bishkek", "Tojikiston": "Dushanbe", "Turkmaniston": "Ashxobod",
    "Afg'oniston": "Qobul", "Pokiston": "Islomobod", "Hindiston": "Nyu-Dehli", "Xitoy": "Pekin", "Yaponiya": "Tokio",
    "Janubiy Koreya": "Seul", "Turkiya": "Anqara", "Eron": "Tehron", "Saudiya Arabistoni": "Ar-Riyod", "Birlashgan Arab Amirliklari": "Abu-Dabi",
    "Misr": "Qohira", "Rossiya": "Moskva", "Ukraina": "Kiyev", "Belarussiya": "Minsk", "AQSh": "Vashington",
    "Kanada": "Ottava", "Meksika": "Mexiko", "Braziliya": "Brazilia", "Argentina": "Buenos-Ayres", "Buyuk Britaniya": "London",
    "Fransiya": "Parij", "Germaniya": "Berlin", "Italiya": "Rim", "Ispaniya": "Madrid", "Portugaliya": "Lissabon",
    "Niderlandiya": "Amsterdam", "Belgiya": "Bryussel", "Shveysariya": "Bern", "Avstriya": "Vena", "Shvetsiya": "Stokgolm",
    "Norvegiya": "Oslo", "Daniya": "Kopengagen", "Finlyandiya": "Xelsinki", "Polsha": "Varshava", "Gretsiya": "Afina",
    "Avstraliya": "Kanberra", "Yangi Zelandiya": "Vellington", "Indoneziya": "Jakarta", "Malayziya": "Kuala-Lumpur", "Singapur": "Singapur",
    "Tailand": "Bangkok", "Vyetnam": "Xanoy", "Filippin": "Manila", "Iroq": "Bag'dod", "Suriya": "Damashq",
    "Iordaniya": "Amman", "Livan": "Bayrut", "Isroil": "Quddus (Yerusalaem)", "Marokash": "Rabot", "Jazoir": "Jazoir",
    "Tunis": "Tunis", "Liviya": "Tripoli", "Sudan": "Xartum", "Efiopiya": "Addis-Abeba", "Keniya": "Nayrobi",
    "Tanzaniya": "Dodoma", "JAR (Janubiy Afrika)": "Pretoriya", "Nigeriya": "Abuja", "Kuba": "Gavana", "Peru": "Lima",
    "Chili": "Santyago", "Kolumbiya": "Bogota", "Venesuela": "Karakas", "Shri-Lanka": "Kolombo", "Bangladesh": "Dakka",
    "Nepal": "Katmandu", "Mo'g'uliston": "Ulan-Bator", "Ozarbayjon": "Boku", "Armaniston": "Yerevan", "Gruziya": "Tbilisi",
    "Ruminiya": "Buxarest", "Bolgariya": "Sofiya", "Vengriya": "Budapesht", "Chexiya": "Praga", "Slovakiya": "Bratislava"
}

# 2. Kimyoviy elementlar (40 ta)
elements = {
    "Vodorod": "H", "Geli": "He", "Litiy": "Li", "Berilliy": "Be", "Bor": "B",
    "Uglerod": "C", "Azot": "N", "Kislorod": "O", "Ftor": "F", "Neon": "Ne",
    "Natriy": "Na", "Magniy": "Mg", "Alyuminiy": "Al", "Kremniy": "Si", "Fosfor": "P",
    "Oltingugurt": "S", "Xlor": "Cl", "Argon": "Ar", "Kaliy": "K", "Kaltsiy": "Ca",
    "Temir": "Fe", "Mis": "Cu", "Rux": "Zn", "Oltin": "Au", "Kumush": "Ag",
    "Platina": "Pt", "Simob": "Hg", "Qo'rg'oshin": "Pb", "Uran": "U", "Plutoniy": "Pu",
    "Yod": "I", "Kripton": "Kr", "Ksenon": "Xe", "Radon": "Rn", "Titan": "Ti",
    "Volfram": "W", "Nikel": "Ni", "Kobalt": "Co", "Qalay": "Sn", "Bariy": "Ba"
}

# 3. Tarixiy sanalar (20 ta)
history_dates = {
    "Amir Temur tavallud topgan yil": "1336-yil", "Alisher Navoiy tavallud topgan yil": "1441-yil",
    "Zahiriddin Muhammad Bobur tavallud topgan yil": "1483-yil", "O'zbekiston Respublikasi Mustaqilligi e'lon qilingan yil": "1991-yil",
    "O'zbekiston Respublikasi Konstitutsiyasi qabul qilingan yil": "1992-yil", "Ikkinchi jahon urushi boshlangan yil": "1939-yil",
    "Ikkinchi jahon urushi tugagan yil": "1945-yil", "Inson birinchi marta koinotga uchgan yil": "1961-yil",
    "Birinchi jahon urushi boshlangan yil": "1914-yil", "Amerika qit'asi Xristofor Kolumb tomonidan kashf etilgan yil": "1492-yil",
    "Fransuz inqilobi boshlangan yil": "1789-yil", "Toshkent zilzilasi sodir bo'lgan yil": "1966-yil",
    "Al-Xorazmiy tavallud topgan asr": "VIII asr", "O'zbek so'mi muomalaga kiritilgan yil": "1994-yil",
    "BMT (Birlashgan Millatlar Tashkiloti) tashkil topgan yil": "1945-yil", "Internet (WWW) ommaviy ishga tushgan yil": "1991-yil",
    "Inson birinchi marta oyga qadam qo'ygan yil": "1969-yil", "Temuriylar davlati tashkil topgan asr": "XIV asr",
    "Islom dini qachon vujudga kelgan?": "VII asr", "Qoraxoniylar davlati qachon tashkil topgan?": "X asr"
}

# 4. Umumiy va Aralash savollar (100+)
general_questions = [
    {"q": "Qur'oni Karimda nomi kelgan yagona sahoba kim?", "c": "Zayd ibn Horisa (r.a)", "w": ["Abu Bakr (r.a)", "Umar (r.a)", "Ali (r.a)"]},
    {"q": "Qur'oni Karimdagi eng uzun sura qaysi?", "c": "Baqara", "w": ["Oli Imron", "Niso", "Moida"]},
    {"q": "Islomning uchinchi ustuni (farzi) nima?", "c": "Ro'za tutish", "w": ["Namoz o'qish", "Zakot berish", "Haj qilish"]},
    {"q": "Qon bosimini o'lchaydigan tibbiy asbob qanday ataladi?", "c": "Tonometr", "w": ["Termometr", "Barometr", "Gidrometr"]},
    {"q": "Atomning yadrosini nimalar tashkil etadi?", "c": "Protonlar va Neytronlar", "w": ["Protonlar va Elektronlar", "Neytronlar va Elektronlar", "Faqat protonlar"]},
    {"q": "Qaysi qon guruhi 'Universal donor' hisoblanadi?", "c": "I (O)", "w": ["II (A)", "III (B)", "IV (AB)"]},
    {"q": "Suv qachon eng yuqori zichlikka ega bo'ladi?", "c": "+4°C da", "w": ["0°C da", "+100°C da", "-4°C da"]},
    {"q": "G'arbda 'Avitsenna' nomi bilan mashhur bo'lgan alloma kim?", "c": "Abu Ali ibn Sino", "w": ["Al-Xorazmiy", "Abu Nasr Forobiy", "Beruniy"]},
    {"q": "Islom tarixida birinchi bo'lib muazzinlik (azon aytish) qilgan sahoba kim?", "c": "Bilol ibn Raboh", "w": ["Salmon Forsiy", "Umar ibn Xattob", "Ammor ibn Yosir"]},
    {"q": "Dunyodagi eng uzun daryo qaysi?", "c": "Amazonka", "w": ["Nil", "Yanszi", "Missisipi"]},
    {"q": "Fotosintez jarayonida o'simlik qanday gazni yutadi?", "c": "Karbonat angidrid", "w": ["Kislorod", "Azot", "Vodorod"]},
    {"q": "Yorug'lik tezligi sekundiga necha kilometrga teng?", "c": "300 000 km/s", "w": ["150 000 km/s", "200 000 km/s", "1 000 000 km/s"]},
    {"q": "Inson tanasidagi eng kichik suyak qayerda joylashgan?", "c": "Quloqda", "w": ["Burunda", "Barmoqda", "Tomoqda"]},
    {"q": "Renessans (Uyg'onish) davri ilk bor qaysi davlatda boshlangan?", "c": "Italiya", "w": ["Ispaniya", "Fransiya", "Germaniya"]},
    {"q": "Kompyuterning 'miyasi' qanday ataladi?", "c": "Protsessor (CPU)", "w": ["Operativ xotira (RAM)", "Qattiq disk (HDD)", "Videokarta"]},
    {"q": "Qaysi qush umuman ucha almaydi, lekin juda tez yuguradi?", "c": "Tuyaqush", "w": ["Kivi", "Kazuari", "Pingvin"]},
    {"q": "DNK molekulasining tuzilishini kim kashf etgan?", "c": "Uotson va Krik", "w": ["Mendel", "Darvin", "Paster"]},
    {"q": "Dunyodagi eng katta ummon qaysi?", "c": "Tinch okeani", "w": ["Atlantika okeani", "Hind okeani", "Shimoliy Muz okeani"]},
    {"q": "Gepardning maksimal yugurish tezligi qariyb qanchaga yetadi?", "c": "110-120 km/soat", "w": ["80-90 km/soat", "150-160 km/soat", "60-70 km/soat"]},
    {"q": "O'zbekistonda nechta viloyat bor?", "c": "12 ta", "w": ["11 ta", "13 ta", "14 ta"]},
    {"q": "Shaxmat taxtasida jami nechta katak bor?", "c": "64", "w": ["81", "100", "49"]},
    {"q": "Qaysi sayyora Qizil sayyora deb ataladi?", "c": "Mars", "w": ["Yupiter", "Venera", "Merkuriy"]},
    {"q": "Dunyodagi eng chuqur ko'l qaysi?", "c": "Baykal", "w": ["Viktoriya", "Tanganika", "Kaspiy"]},
    {"q": "Xitoy devori qanday maqsadda qurilgan?", "c": "Himoya (mudofaa)", "w": ["Go'zallik uchun", "Chegarani ko'rsatish", "Savdo yo'li sifatida"]},
    {"q": "Arslonlarning urg'ochisi nima deb ataladi?", "c": "Modda arslon", "w": ["Qoplon", "Sirtlon", "Urg'ochi sher"]},
    {"q": "Toshkent metrosi nechanchi yilda ishga tushirilgan?", "c": "1977 yil", "w": ["1980 yil", "1966 yil", "1991 yil"]},
    {"q": "Dunyo aholisi bo'yicha qaysi davlat 1-o'rinda turadi (2024)?", "c": "Hindiston", "w": ["Xitoy", "AQSh", "Indoneziya"]},
    {"q": "Alisher Navoiyning mashhur asari qaysi?", "c": "Xamsa", "w": ["Qutadg'u bilig", "Devoni lug'otit turk", "Boburnoma"]},
    {"q": "Beshbarmog' tog'lari O'zbekistonning qaysi viloyatida joylashgan?", "c": "Navoiy", "w": ["Jizzax", "Samarqand", "Qashqadaryo"]},
    {"q": "Eng kichik qit'a qaysi?", "c": "Avstraliya", "w": ["Antarktida", "Janubiy Amerika", "Yevropa"]},
]

all_questions = []

# 1. Poytaxtlarni shakllantirish
capitals = list(countries.values())
for country, capital in countries.items():
    wrongs = random.sample([c for c in capitals if c != capital], 3)
    all_questions.append({
        "q": f"{country} davlatining poytaxti qaysi shahar?",
        "c": capital,
        "w": wrongs
    })

# 2. Elementlarni shakllantirish
symbols = list(elements.values())
for element, symbol in elements.items():
    wrongs = random.sample([s for s in symbols if s != symbol], 3)
    all_questions.append({
        "q": f"{element} kimyoviy elementining belgisi qaysi qatorda to'g'ri ko'rsatilgan?",
        "c": symbol,
        "w": wrongs
    })

# 3. Tarixiy sanalarni shakllantirish
dates = list(history_dates.values())
for event, date in history_dates.items():
    wrongs = random.sample([d for d in dates if d != date], 3)
    all_questions.append({
        "q": f"{event}",
        "c": date,
        "w": wrongs
    })

# 4. Umumiy savollarni qo'shish
for g_q in general_questions:
    all_questions.append(g_q)

# 5. Matematik mantiqiy savollar (50 ta)
for i in range(50):
    a = random.randint(11, 30)
    b = random.randint(11, 30)
    c_ans = a * b
    wrongs = [str(c_ans + random.randint(1, 10)), str(c_ans - random.randint(1, 10)), str(c_ans + random.randint(11, 20))]
    all_questions.append({
        "q": f"{a} ni {b} ga ko'paytirganda natija necha bo'ladi?",
        "c": str(c_ans),
        "w": wrongs
    })

# Barchasini aralashtirib bazaga tiqamiz
random.shuffle(all_questions)

def generate_big_db():
    db.init_db()
    added = 0
    for q_data in all_questions:
        options = q_data['w'] + [q_data['c']]
        random.shuffle(options)
        correct_idx = options.index(q_data['c'])
        
        success = db.add_question(q_data['q'], options, correct_idx)
        if success:
            added += 1
            
    stats = db.get_stats()
    print(f"Jami {len(all_questions)} ta savoldan {added} ta yangi savol bazaga yuklandi!")
    print(f"Bazada jami {stats['total']} ta savol mavjud (Bu {stats['total'] // 4} kunga yetadi).")

if __name__ == '__main__':
    generate_big_db()
