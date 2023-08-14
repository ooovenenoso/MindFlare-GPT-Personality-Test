import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, Scale, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF
import openai

openai.api_key = "API_KEY_OPENAI"

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
    save_answer()
    global current_question
    total_questions = sum(len(v) for v in questions.values())
    if current_question < total_questions - 1:  # Asegurarse de que no excedamos el total de preguntas
        category_index = current_question // 12
        category = list(questions.keys())[category_index]
        question = questions[category][current_question % 12]
        question_label.config(text=question)
        current_question += 1
    else:
        messagebox.showinfo("Test de Personalidad", "¡Has completado todas las preguntas!")

def save_answer():
    global current_question, answers
    category_index = current_question // 12
    if category_index >= len(questions):  # Asegurarse de que no excedamos el número de categorías
        return
    category = list(questions.keys())[category_index]
    answer = scale.get()
    if category not in answers:
        answers[category] = []
    answers[category].append(answer)

def previous_question():
    global current_question
    current_question -= 1
    if current_question >= 0:
        category_index = current_question // 12
        category = list(questions.keys())[category_index]
        question = questions[category][current_question % 12]
        question_label.config(text=question)


def generate_summary():
    summary_window = Tk()
    summary_window.title("Resumen del Test de Personalidad")
    
    # Calcular el resumen (promedio de las respuestas para cada categoría)
    summary_text = "Resumen de tus respuestas:\n\n"
    for category, scores in answers.items():
        avg_score = sum(scores) / len(scores)
        summary_text += f"{category}: {avg_score:.2f}/7\n"
    
    Label(summary_window, text=summary_text, font=("Arial", 12)).pack(pady=20)
    
    Button(summary_window, text="Guardar como PDF", command=lambda: generate_pdf_with_summary(summary_text)).pack(pady=10)
    Button(summary_window, text="Ver en Gráfico", command=generate_graph).pack(pady=10)
    Button(summary_window, text="Cerrar", command=summary_window.destroy).pack(pady=10)

def get_openai_summary(answers):
    # Convertir las respuestas en texto
    text = "\n".join([f"{cat}: {sum(answers[cat]) / len(answers[cat])}" for cat in answers])

    # Solicitar a OpenAI un análisis detallado en español
    prompt_text = f"""
    Basado en los siguientes resultados del Test de Personalidad, proporciona un análisis detallado para ayudar al reclutador a entender las características del candidato:
    {text}
    """

    messages = [{"role": "system", "content": "Estás analizando resultados de un Test de Personalidad."},
                {"role": "user", "content": prompt_text}]
    
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    # La respuesta del modelo estará en el último mensaje enviado por "asistente"
    return response.choices[0].message['content'].strip()

def generate_pdf_with_summary(summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Obtener el análisis de OpenAI
    openai_analysis = get_openai_summary(answers)
    pdf.multi_cell(0, 10, openai_analysis)
    
    # Guardar el PDF
    filename = "analisis_test_personalidad.pdf"
    pdf.output(filename)
    messagebox.showinfo("Análisis generado", f"El análisis ha sido guardado como {filename}")

def generate_graph():
    labels = [cat for cat in questions.keys() if cat in answers]
    scores = [sum(answers[cat]) / len(answers[cat]) for cat in labels]

    # Configuración del gráfico de radar
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    scores += scores[:1]  # Añadir la primera puntuación al final para cerrar el círculo
    angles += angles[:1]  # Añadir el primer ángulo al final para cerrar el círculo

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(angles, scores, color='skyblue', alpha=0.25)
    ax.plot(angles, scores, color='skyblue', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])  # Excluimos el último ángulo que es el repetido
    ax.set_xticklabels(labels)

    # Establecer el título y mostrar el gráfico
    ax.set_title("Resumen del Test de Personalidad", size=16, y=1.1)
    plt.tight_layout()
    plt.show()


def update_progressbar():
    total_questions = sum(len(v) for v in questions.values())
    percentage_complete = (current_question / total_questions) * 100
    progress_bar['value'] = percentage_complete


root = Tk()
root.title("Test de Personalidad")
root.geometry("500x400")
root.configure(bg="#e0e0e0")  # Color de fondo ligero

question_label = Label(root, text="Presiona Siguiente para comenzar el test.", bg="#e0e0e0", font=("Arial", 12))
question_label.pack(pady=20)

scale = Scale(root, from_=1, to=7, orient="horizontal", bg="#f5f5f5", sliderlength=20, width=15)
scale.pack(pady=20)

next_button = Button(root, text="Siguiente", command=lambda: [next_question(), update_progressbar()], bg="#4caf50", fg="white")
next_button.pack(pady=10)

previous_button = Button(root, text="Anterior", command=previous_question, bg="#4caf50", fg="white")
previous_button.pack(pady=10)

finish_button = Button(root, text="Finalizar", command=generate_summary, bg="#ff5722", fg="white")
finish_button.pack(pady=10)

reset_button = Button(root, text="Reiniciar", command=lambda: [reset_test(), update_progressbar()], bg="#ff5722", fg="white")
reset_button.pack(pady=10)

# Barra de progreso
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=20)

root.mainloop()
