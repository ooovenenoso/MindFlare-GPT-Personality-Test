import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, Scale, messagebox, ttk, Entry, Frame
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF
from datetime import datetime
import openai

openai.api_key = "API_KEY_OPENAI"

# Preguntas
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

user_name = ""
user_age = ""

# Preguntas y respuestas y demás funciones se mantienen igual...

# Ventana para recopilar nombre y edad
def collect_name_and_age():
    def submit():
        global user_name, user_age
        user_name = name_entry.get()
        user_age = age_entry.get()
        user_info_window.destroy()

    user_info_window = Tk()
    user_info_window.title("Ingrese su Nombre y Edad")
    user_info_window.configure(bg="#f5f5f5")

    name_label = Label(user_info_window, text="Nombre Completo:", bg="#f5f5f5", font=("Helvetica", 10))
    name_label.pack(pady=10)
    name_entry = Entry(user_info_window, font=("Helvetica", 10))
    name_entry.pack(pady=10)

    age_label = Label(user_info_window, text="Edad:", bg="#f5f5f5", font=("Helvetica", 10))
    age_label.pack(pady=10)
    age_entry = Entry(user_info_window, font=("Helvetica", 10))
    age_entry.pack(pady=10)

    submit_button = Button(user_info_window, text="Enviar", command=submit, bg="#4caf50", fg="white", relief="flat", font=("Helvetica", 10))
    submit_button.pack(pady=10)

    user_info_window.mainloop()

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
    if current_question > 0:
        current_question -= 1
        category_index = current_question // 12
        category = list(questions.keys())[category_index]
        question = questions[category][current_question % 12]
        question_label.config(text=question)
        
        # Restaurar la respuesta previamente guardada en la escala
        previous_answer = answers[category][current_question % 12]
        scale.set(previous_answer)
    else:
        messagebox.showinfo("Test de Personalidad", "Ya estás en la primera pregunta.")

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

class MyPDF(FPDF):
    def header(self):
        # Ruta de la imagen de fondo
        background_image = "background.png"

        # Obtener las dimensiones de la imagen (en mm)
        image_width, image_height = self.get_image_dimensions(background_image)

        # Calcular las coordenadas x e y para centrar la imagen
        x_centered = (self.w - image_width) * 0.5
        y_centered = (self.h - image_height) * 0.5

        # Agregar la imagen de fondo en cada página, centrada
        self.image(background_image, x=x_centered, y=y_centered, w=image_width)

    def get_image_dimensions(self, image_path):
        # Usar la librería PIL para obtener las dimensiones de la imagen en píxeles
        with Image.open(image_path) as img:
            width_px, height_px = img.size

        # Convertir las dimensiones de píxeles a milímetros (asumiendo 96 DPI)
        width_mm = width_px * 25.4 / 96
        height_mm = height_px * 25.4 / 96

        return width_mm, height_mm

def generate_pdf_with_summary(summary):
    pdf = MyPDF()
    pdf.add_page()

    pdf.set_font("Arial", 'B', size=16)  # Fuente en negrita y tamaño 16

    # Título del PDF
    pdf.cell(0, 10, "Análisis del Test de Personalidad", ln=True, align="C")

    # Escribir el nombre y la edad en el PDF
    pdf.set_font("Arial", size=12)  # Cambiar la fuente a tamaño 12
    pdf.cell(0, 10, f"Nombre: {user_name}", ln=True)
    pdf.cell(0, 10, f"Edad: {user_age}", ln=True)
    # Obtener la fecha y hora actual
    current_date_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    pdf.cell(0, 10, f"Fecha y Hora: {current_date_time}", ln=True)  # Añadir al PDF

    pdf.ln(10)

    # Obtener el análisis de OpenAI
    openai_analysis = get_openai_summary(answers)
    pdf.multi_cell(0, 10, openai_analysis)

    # Agregar la imagen del gráfico
    image_path = "personalidad.png"  # Ruta de la imagen del gráfico
    pdf.image(image_path, x=10, y=None, w=190)  # Ajusta el tamaño (w) según tus necesidades

    # Guardar el PDF
    filename = "analisis_test_personalidad.pdf"
    pdf.output(filename)
    messagebox.showinfo("Análisis generado", f"El análisis ha sido guardado como {filename}")

def generate_graph():
    labels = [cat for cat in questions.keys() if cat in answers]
    scores = [sum(answers[cat]) / len(answers[cat]) for cat in labels]
    num_vars = len(labels)
    
    # Configuración del gráfico de radar
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    scores += scores[:1]  # Añadir la primera puntuación al final para cerrar el círculo
    angles += angles[:1]  # Añadir el primer ángulo al final para cerrar el círculo

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    # Colores personalizados
    fill_color = '#2899c0'
    line_color = '#ca4124'
    label_color = '#c09660'
    
    # Gráfico principal
    ax.fill(angles, scores, color=fill_color, alpha=0.6)  # Color de relleno
    ax.plot(angles, scores, color=line_color, linewidth=3)  # Color de la línea
    
    # Configuración de etiquetas y títulos
    ax.set_yticks(range(1, 8))
    ax.set_yticklabels(range(1, 8), fontsize=12, color=label_color)  # Color de las etiquetas de puntuación
    ax.set_xticks(angles[:-1])  # Excluimos el último ángulo que es el repetido
    ax.set_xticklabels(labels, fontsize=14, fontweight='bold', color=label_color)  # Color de las etiquetas de categoría
    
    # Añadir líneas de cuadrícula y configurar el fondo
    ax.grid(color='grey', linestyle='--', linewidth=0.5, alpha=0.6)
    ax.set_facecolor('whitesmoke')  # Color de fondo del gráfico
    
    # Establecer el título
    ax.set_title("Resumen del Test de Personalidad", size=20, y=1.1, color=line_color, fontweight='bold')  # Color y tamaño del título
    
    plt.tight_layout()
    
    # Guardar la imagen del gráfico
    image_path = "personalidad.png"
    fig.savefig(image_path, dpi=300, bbox_inches='tight')  # Aumentar la resolución y ajustar el tamaño
    
    # Mostrar el gráfico
    plt.show()

def update_progressbar():
    total_questions = sum(len(v) for v in questions.values())
    percentage_complete = (current_question / total_questions) * 100
    progress_bar['value'] = percentage_complete

def reset_test():
    global answers, current_question
    answers = {}  # Reiniciar las respuestas
    current_question = 0  # Reiniciar el contador de preguntas
    question_label.config(text="Presiona Siguiente para comenzar el test.")  # Reiniciar el texto de la etiqueta de pregunta
    scale.set(0)  # Reiniciar la escala

# Recopilar nombre y edad antes de comenzar el test
collect_name_and_age()

# Ventana principal
root = Tk()
root.title("Test de Personalidad")
root.geometry("700x500")
root.configure(bg="#f5f5f5")  # Fondo moderno

question_label = Label(root, text="Presiona Siguiente para comenzar el test.", bg="#f5f5f5", font=("Helvetica", 14), fg="#333333")
question_label.pack(pady=20)

# Escala y etiquetas
scale_frame = Frame(root, bg="#f5f5f5")
scale_frame.pack(pady=10)

left_reference_label = Label(scale_frame, text="No me identifico", bg="#f5f5f5", font=("Helvetica", 10), fg="#555555")
left_reference_label.pack(side="left", padx=5)

scale = Scale(scale_frame, from_=1, to=7, orient="horizontal", bg="#e0e0e0", sliderlength=30, width=15, highlightthickness=0)
scale.pack(side="left", pady=20)

right_reference_label = Label(scale_frame, text="Me identifico totalmente", bg="#f5f5f5", font=("Helvetica", 10), fg="#555555")
right_reference_label.pack(side="left", padx=5)

# Botones
button_frame = Frame(root, bg="#f5f5f5")
button_frame.pack(pady=10)

next_button = Button(button_frame, text="Siguiente", command=lambda: [next_question(), update_progressbar()], bg="#4caf50", fg="white", relief="flat", font=("Helvetica", 10))
next_button.pack(side="left", padx=5)

previous_button = Button(button_frame, text="Anterior", command=previous_question, bg="#9e9e9e", fg="white", relief="flat", font=("Helvetica", 10))
previous_button.pack(side="left", padx=5)

finish_button = Button(button_frame, text="Finalizar", command=generate_summary, bg="#ff5722", fg="white", relief="flat", font=("Helvetica", 10))
finish_button.pack(side="left", padx=5)

reset_button = Button(button_frame, text="Reiniciar", command=lambda: [reset_test(), update_progressbar()], bg="#607d8b", fg="white", relief="flat", font=("Helvetica", 10))
reset_button.pack(side="left", padx=5)

# Barra de progreso
progress_bar = ttk.Progressbar(root, orient="horizontal", length=600, mode="determinate", style="TProgressbar")
progress_bar.pack(pady=20)

root.mainloop()

