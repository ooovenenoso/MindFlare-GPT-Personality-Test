import numpy as np
import matplotlib.pyplot as plt
import csv
from tkinter import Tk, Label, Button, Scale, messagebox
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF
import openai

openai.api_key = "sk-vAMH..."

# Preguntas y respuestas
questions = {
    "Apertura a la experiencia": [
        "Me gusta probar cosas nuevas y diferentes.",
        "Me interesa aprender sobre diferentes culturas y formas de vida.",
        "Me gusta explorar nuevas ideas y perspectivas.",
        "Me siento atraído por el arte y la creatividad.",
        "Me gusta discutir ideas abstractas y conceptos teóricos.",
        "Me gusta leer sobre temas diversos y variados.",
        "Me gusta visitar museos y exposiciones de arte.",
        "Me interesa la filosofía y las ideas abstractas.",
        "Me gusta experimentar con diferentes formas de expresión artística.",
        "Me gusta pensar en formas alternativas de resolver problemas.",
        "Me gusta cuestionar las normas y las reglas establecidas.",
        "Me interesa la exploración del potencial humano."
    ],
    "Conciencia": [
        "Soy una persona organizada y disciplinada.",
        "Me gusta hacer planes y establecer metas.",
        "Soy puntual y cumplo con mis compromisos.",
        "Me preocupo por la calidad del trabajo que realizo.",
        "Me gusta seguir las reglas y las normas establecidas.",
        "Me gusta tener todo bajo control.",
        "Me siento incómodo cuando las cosas están desorganizadas o no planeadas.",
        "Me gusta hacer listas y mantener un registro de mis tareas.",
        "Me esfuerzo por hacer siempre lo mejor posible.",
        "Me molesta cuando otras personas no cumplen con sus compromisos.",
        "Me gusta ser responsable de mis acciones y decisiones.",
        "Me gusta establecer metas ambiciosas y trabajar duro para alcanzarlas."
    ],
    "Extraversión": [
        "Me siento cómodo en situaciones sociales y me gusta conocer gente nueva.",
        "Me gusta ser el centro de atención.",
        "Me gusta hablar en público y dar presentaciones.",
        "Me siento energizado y emocionado en situaciones sociales.",
        "Me gusta salir con amigos y tener una vida social activa.",
        "Me gusta trabajar en equipo y colaborar con otros.",
        "Me gusta ser el líder en un grupo o equipo.",
        "Me gusta llamar la atención con mi estilo y apariencia personal.",
        "Me siento cómodo hablando con personas desconocidas.",
        "Me gusta participar en eventos sociales y actividades grupales.",
        "Me gusta estar rodeado de gente y ruido.",
        "Me siento aburrido o inquieto cuando estoy solo por mucho tiempo."
    ],
    "Afabilidad": [
        "Me preocupo por los sentimientos de los demás.",
        "Me gusta ayudar a las personas cuando necesitan apoyo emocional.",
        "Me siento incómodo/a al ver a otros en situaciones difíciles.",
        "Me considero alguien compasivo/a y empático/a.",
        "Disfruto al trabajar en equipo y colaborar con otros para lograr objetivos.",
        "No me gusta confrontar a los demás y trato de evitar los conflictos.",
        "Me gusta hacer favores a los demás y cuidar de ellos.",
        "Disfruto de las interacciones sociales y de hacer nuevos amigos.",
        "Me esfuerzo por mantener buenas relaciones con los demás.",
        "Me preocupo por el bienestar de los demás y trato de ayudar en lo que puedo.",
        "Me gusta dar consejos y apoyo a los demás.",
        "Me gusta pasar tiempo con mis seres queridos y cuidar de ellos.",
        "Disfruto haciendo cosas que hacen felices a los demás."
    ],
    "Neuroticismo": [
        "Me siento fácilmente estresado/a y preocupado/a.",
        "Tiendo a sentirme abrumado/a con frecuencia.",
        "A menudo me siento triste o deprimido/a.",
        "Me preocupo mucho por las cosas.",
        "Me siento ansioso/a en situaciones nuevas o desconocidas.",
        "Suelo preocuparme por cosas que están fuera de mi control.",
        "Me cuesta relajarme y dejar de pensar en los problemas.",
        "Soy propenso/a a experimentar cambios de humor.",
        "Me preocupo mucho por lo que piensan los demás de mí.",
        "Me afectan más las críticas y los comentarios negativos que los positivos.",
        "Me siento inseguro/a acerca de mis habilidades y capacidades.",
        "Tengo miedo de cometer errores y fracasar en lo que hago."
    ]
}

answers = {}
current_question = 0

def next_question():
    global current_question
    if current_question < len(list(questions.keys())) * 12:
        category_index = current_question // 12
        category = list(questions.keys())[category_index]
        question = questions[category][current_question % 12]
        question_label.config(text=question)
        current_question += 1
    else:
        messagebox.showinfo("Test de Personalidad", "¡Has completado todas las preguntas!")

def previous_question():
    global current_question
    current_question -= 1
    if current_question >= 0:
        category_index = current_question // 12
        category = list(questions.keys())[category_index]
        question = questions[category][current_question % 12]
        question_label.config(text=question)

def finish_test():
    if len(answers) == 0:
        messagebox.showerror("Test de Personalidad", "No has respondido ninguna pregunta.")
        return
    summary = generate_summary()
    generate_pdf_with_summary(summary)

def reset_test():
    global current_question, answers
    current_question = 0
    answers = {}
    question_label.config(text="Presiona Siguiente para comenzar el test.")

def save_answer():
    global current_question, answers
    category_index = (current_question - 1) // 12
    category = list(questions.keys())[category_index]
    answer = scale.get()
    if category not in answers:
        answers[category] = []
    answers[category].append(answer)
    next_question()

def generate_summary():
    all_answers = []
    for category, category_answers in answers.items():
        all_answers.append(f"{category}: {', '.join(str(answer) for answer in category_answers)}")
    prompt = "\n".join(all_answers)

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.7,
        max_tokens=100
    )
    summary = response.choices[0].text.strip()

    return summary

def generate_graph():
    labels = list(questions.keys())
    values = [np.mean(answers.get(category, [0])) for category in labels]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    values = np.concatenate((values, [values[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'polar': True})
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    ax.set_title("Resultado del Test de Personalidad")

    plt.savefig("graph.png")
    plt.close()

def generate_pdf_with_summary(summary):
    generate_graph()

    image = Image.open("graph.png")
    width, height = image.size

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, "Resultado del Test de Personalidad", ln=True, align="C")
    pdf.ln(10)

    pdf.image("graph.png", x=10, y=20, w=width, h=height)
    pdf.ln(height + 30)

    pdf.multi_cell(0, 10, summary, align="L")
    pdf.output("result_summary.pdf")

root = Tk()
root.title("Test de Personalidad")
root.geometry("500x400")

question_label = Label(root, text="Presiona Siguiente para comenzar el test.")
question_label.pack(pady=20)

scale = Scale(root, from_=1, to=7, orient="horizontal")
scale.pack(pady=20)

next_button = Button(root, text="Siguiente", command=save_answer)
next_button.pack(pady=10)

previous_button = Button(root, text="Anterior", command=previous_question)
previous_button.pack(pady=10)

finish_button = Button(root, text="Finalizar", command=finish_test)
finish_button.pack(pady=10)

reset_button = Button(root, text="Reiniciar", command=reset_test)
reset_button.pack(pady=10)

root.mainloop()
