import random
import database as db

all_questions = []

# Qo'shimcha 150 ta matematik savollar (3 oyga to'ldirish uchun)
for i in range(100):
    a = random.randint(100, 500)
    b = random.randint(100, 500)
    c_ans = a + b
    wrongs = [str(c_ans + random.randint(1, 20)), str(c_ans - random.randint(1, 20)), str(c_ans + random.randint(21, 50))]
    all_questions.append({
        "q": f"{a} va {b} sonlarining yig'indisi necha bo'ladi?",
        "c": str(c_ans),
        "w": wrongs
    })

for i in range(50):
    a = random.randint(50, 100)
    b = random.randint(10, 40)
    c_ans = a - b
    wrongs = [str(c_ans + random.randint(1, 10)), str(c_ans - random.randint(1, 10)), str(c_ans + random.randint(11, 20))]
    all_questions.append({
        "q": f"{a} dan {b} ni ayirganda necha qoladi?",
        "c": str(c_ans),
        "w": wrongs
    })

added = 0
for q_data in all_questions:
    options = q_data['w'] + [q_data['c']]
    random.shuffle(options)
    correct_idx = options.index(q_data['c'])
    
    success = db.add_question(q_data['q'], options, correct_idx)
    if success:
        added += 1

stats = db.get_stats()
print(f"Qo'shimcha savollar qo'shildi! Bazada jami {stats['total']} ta savol mavjud (Bu {stats['total'] // 4} kunga yetadi).")
