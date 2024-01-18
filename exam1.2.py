# Кирик Володимир:

#Простий чат-бот для обслуговування клієнтів
#Розробіть простий чат-бот, який може відповідати на типові питання клієнтів (наприклад, про години роботи, послуги, ціни).
#Використовуйте умовні конструкції для розгалуження діалогу залежно від запитів користувача. 
#Чат-бот має зберігати історію запитань та відповідей.




from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

class ChatBot:
    def __init__(self):
        self.rules = {
            "години роботи": "Ми працюємо з понеділка по п'ятницю з 9:00 до 18:00.",
            "послуги": "Наші послуги включають продаж і обслуговування техніки, консультації та інші.",
            "ціни": "Ціни на наші послуги можна знайти на нашому веб-сайті або звернутися до нашого відділу продажів."
        }
        self.history = []

    def add_rule(self, question, response):
        self.rules[question] = response

    def respond_to_question(self, question):
        response = self.rules.get(question, "Вибачте, я не розумію вашого запитання. Якщо у вас є інші питання, будь ласка, задавайте.")
        self.history.append({"питання": question, "відповідь": response})
        return response
    
    def print_history(self):
        return [{"питання": entry['питання'], "відповідь": entry['відповідь']} for entry in self.history]

chat_bot = ChatBot()

chat_bot.add_rule("розклад роботи вихідного дня", "У вихідні ми працюємо з 10:00 до 16:00.")
chat_bot.add_rule("послуги вихідного дня", "У вихідний день ми пропонуємо обслуговування клієнтів та консультації. Продажі та інші послуги недоступні.")
chat_bot.add_rule("графік роботи_1", "Графік роботи з понеділка по п'ятницю з 9:00 до 18:00.")
chat_bot.add_rule("графік роботи_2", "Графік роботи у вихідні з 10:00 до 16:00.")
chat_bot.add_rule("товари_1", "Дякую за вибір товару Лаптопи.")
chat_bot.add_rule("товари_2", "Дякую за вибір товару Смартфони.")
chat_bot.add_rule("товари_3", "Дякую за вибір товару Планшети.")

def execute_python_code():
    python_code = """
print("Виконання Python-коду")
result = 2 + 2
print("Результат:", result)
"""

    try:
        with open('temp_script.py', 'w') as temp_script:
            temp_script.write(python_code)
        result = subprocess.run(['python', 'temp_script.py'], capture_output=True, text=True)
        
        return result.stdout, result.stderr
    except Exception as e:
        return f'Помилка виконання Python-коду: {str(e)}', None
    finally:
        os.remove('temp_script.py')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask_question', methods=['POST'])
def ask_question():
    question = request.form.get('question')
    response = chat_bot.respond_to_question(question)
    return jsonify({'response': response})

@app.route('/execute_python_code')
def execute_python_code_route():
    stdout, stderr = execute_python_code()
    return jsonify({'response': stdout, 'error': stderr})

if __name__ == '__main__':
    app.run(debug=True)

