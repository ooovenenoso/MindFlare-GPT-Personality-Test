import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, Scale, messagebox, ttk, Entry, Frame, IntVar, Checkbutton, Scrollbar, Text, Toplevel, PhotoImage
from PIL import Image, ImageDraw, ImageFont, ImageTk
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

def accept_terms_and_conditions():
    def proceed():
        if var.get():
            terms_window.destroy()
            collect_name_and_age()
        else:
            messagebox.showwarning("Términos y Condiciones", "Debes aceptar los términos y condiciones para continuar.")

    terms_window = Tk()
    terms_window.title("Términos y Condiciones")
    terms_window.configure(bg="#f5f5f5")
    terms_window.attributes('-fullscreen', True)

    # Frame para contener el Text y Scrollbar
    frame = Frame(terms_window, bg="#f5f5f5")
    frame.pack(pady=20, padx=20, expand=True, fill="both")

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    terms_display = Text(frame, wrap="word", yscrollcommand=scrollbar.set, font=("Helvetica", 10), height=20, width=80)
    terms_display.pack(side="left", expand=True, fill="both")

    # Insertar texto con formato
    terms_display.tag_configure("title", font=("Arial", 16, "bold"))
    terms_display.tag_configure("bold", font=("Arial", 12, "bold"))
    terms_display.tag_configure("normal", font=("Arial", 12))

    terms_display.insert("1.0", "Términos y Condiciones del Test de Personalidad MindFlare GPT\n", "title")
    terms_display.insert("end", "\n1. Objetivo del Test: ", "bold")
    terms_display.insert("end", "El Test de Personalidad MindFlare GPT es una herramienta complementaria de evaluación diseñada para interpretar ciertas características de personalidad basadas en las respuestas proporcionadas. Es fundamental entender que los resultados son interpretativos y subjetivos, y no deben ser considerados como diagnósticos médicos, psicológicos o definitivos para la toma de decisiones.\n\n", "normal")
    terms_display.insert("end", "2. Consentimiento Voluntario: ", "bold")
    terms_display.insert("end", "Al iniciar el test, das tu consentimiento voluntario para participar. Tienes el derecho de no responder cualquier pregunta, detener el test en cualquier momento o no completarlo, sin enfrentar penalizaciones o discriminación por parte de la empresa evaluadora.\n\n", "normal")
    terms_display.insert("end", "3. Privacidad y Tratamiento de Datos: ", "bold")
    terms_display.insert("end", "Tu privacidad es esencial. Las respuestas que proporciones serán procesadas de forma anónima y la empresa garantizará la confidencialidad de tus datos. Sin tu consentimiento explícito, tus respuestas no serán conservadas más allá del tiempo necesario para el proceso de evaluación ni compartidas con terceros ajenos al proceso. Tienes el derecho de solicitar acceso a tus datos y, si es necesario, corregir o eliminar cualquier información incorrecta.\n\n", "normal")
    terms_display.insert("end", "4. Limitación de Responsabilidad: ", "bold")
    terms_display.insert("end", "Ni la empresa que proporciona este software ni la empresa que te está evaluando garantizan que los resultados del test sean un reflejo completo o preciso de tu personalidad o aptitud para un cargo. Los resultados no deben ser la única base para decisiones personales o profesionales. Ambas empresas se desligan de cualquier responsabilidad por decisiones tomadas basadas únicamente en los resultados de este test.\n\n", "normal")
    terms_display.insert("end", "5. Derechos de Propiedad: ", "bold")
    terms_display.insert("end", "Este test, incluido su contenido, diseño, gráficos y software, está protegido por derechos de propiedad intelectual. Está prohibido copiar, distribuir, modificar, revender o usar el contenido del test con fines comerciales sin el permiso adecuado.\n\n", "normal")
    terms_display.insert("end", "6. Modificaciones: ", "bold")
    terms_display.insert("end", "Nos reservamos el derecho de modificar estos términos y condiciones en cualquier momento sin previo aviso. Es responsabilidad del usuario revisar regularmente estos términos.\n\n", "normal")
    terms_display.insert("end", "7. Terminación: ", "bold")
    terms_display.insert("end", "Nos reservamos el derecho de suspender o terminar el acceso de un usuario a la herramienta por cualquier motivo, incluyendo la violación de estos términos.\n\n", "normal")
    terms_display.insert("end", "8. Contacto: ", "bold")
    terms_display.insert("end", "Si tienes preguntas o inquietudes acerca de este test o de tus resultados, debes dirigirte a la empresa que te está evaluando. Se esforzarán por responder a tus inquietudes en un plazo máximo de 15 días laborables.\n\n", "normal")
    terms_display.insert("end", "9. Ley Aplicable y Jurisdicción: ", "bold")
    terms_display.insert("end", "Estos términos se regirán según las leyes de Puerto Rico. Las partes acuerdan hacer todo lo posible para resolver cualquier disputa relacionada con estos términos, el test o sus resultados de manera amistosa antes de iniciar acciones legales. Si no se llega a un acuerdo, la disputa será resuelta en los tribunales de [Ciudad, País/Estado].\n\n", "normal")
    terms_display.insert("end", "10. Licencia Creative Commons: ", "bold")
    terms_display.insert("end", "Este test está licenciado bajo la Licencia Creative Commons Attribution-NonCommercial-NoDerivs 2.0 Generic (CC BY-NC-ND 2.0). Puedes compartir el test, pero no puedes hacer uso comercial de él ni realizar obras derivadas.\n\n", "normal")
    terms_display.insert("end", "11. No Garantía: ", "bold")
    terms_display.insert("end", "Este test se proporciona 'tal cual', sin garantías de ningún tipo, ya sean expresas o implícitas, incluyendo, pero no limitado a, garantías implícitas de comerciabilidad, idoneidad para un propósito particular o no infracción.\n\n", "normal")
    terms_display.insert("end", "12. Indemnización: ", "bold")
    terms_display.insert("end", "El usuario acepta indemnizar, defender y mantener indemne a la empresa, sus licenciantes, empleados, agentes y representantes de cualquier reclamación, pérdida, daño, coste, gasto y otra responsabilidad, incluyendo, sin limitación, honorarios legales, que surja del uso o mal uso del test, o la violación de estos términos.\n\n", "normal")
    terms_display.insert("end", "13. Terceros: ", "bold")
    terms_display.insert("end", "Estos términos no otorgan derechos a terceros beneficiarios. Sólo las partes en estos términos pueden hacer cumplir estos términos.\n\n", "normal")
    terms_display.insert("end", "\n**Al utilizar esta herramienta, el usuario acepta estar vinculado por estos términos y condiciones y cualquier otro aviso o restricción relacionado con el uso de la herramienta.**\n", "bold")

    terms_display.configure(state="disabled")
    scrollbar.config(command=terms_display.yview)

    var = IntVar()
    check_button = Checkbutton(terms_window, text="Acepto los términos y condiciones", variable=var, bg="#f5f5f5", font=("Helvetica", 10))
    check_button.pack(pady=10)

    Button(terms_window, text="Continuar", command=proceed, bg="#4caf50", fg="white", relief="flat", font=("Helvetica", 10)).pack(pady=10)

    terms_window.mainloop()


# Ventana para recopilar nombre y edad
def collect_name_and_age():
    def submit():
        global user_name, user_age
        user_name = name_entry.get().strip()  # Eliminar espacios en blanco al principio y al final
        user_age = age_entry.get().strip()

        # Validar que los campos no estén vacíos
        if not user_name or not user_age:
            messagebox.showwarning("Información faltante", "Por favor, rellena todos los campos antes de continuar.")
            return

        # Validar que la edad sea un número
        if not user_age.isdigit():
            messagebox.showwarning("Edad inválida", "Por favor, introduce una edad válida (solo números).")
            return

        user_info_window.destroy()

    user_info_window = Tk()
    user_info_window.title("Ingrese su Nombre y Edad")
    user_info_window.configure(bg="#f5f5f5")
    
    # Modo de pantalla completa
    user_info_window.attributes('-fullscreen', True)

    # Marco central para agrupar los elementos y centrarlos
    center_frame = Frame(user_info_window, bg="#f5f5f5")
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = Label(center_frame, text="Información Básica: Identifícate", bg="#f5f5f5", font=("Arial", 20, "bold"))
    title_label.pack(pady=30)

    name_frame = Frame(center_frame, bg="#f5f5f5")
    name_frame.pack(pady=15, fill="x")
    name_label = Label(name_frame, text="Nombre Completo:", bg="#f5f5f5", font=("Arial", 14))
    name_label.grid(row=0, column=0, padx=(0, 20))
    name_entry = Entry(name_frame, font=("Arial", 12), width=40)
    name_entry.grid(row=0, column=1, padx=(20, 0))

    age_frame = Frame(center_frame, bg="#f5f5f5")
    age_frame.pack(pady=15, fill="x")
    age_label = Label(age_frame, text="Edad:", bg="#f5f5f5", font=("Arial", 14), width=15)
    age_label.grid(row=0, column=0, padx=(0, 20))
    age_entry = Entry(age_frame, font=("Arial", 12), width=40)
    age_entry.grid(row=0, column=1, padx=(20, 0))

    submit_button = Button(center_frame, text="Enviar", command=submit, bg="#4caf50", fg="white", relief="flat", font=("Arial", 14, "bold"), width=20)
    submit_button.pack(pady=40)

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

def confirm_exit():
    response = messagebox.askyesno("Confirmar salida", "¿Estás seguro de que quieres cerrar el programa?")
    if response:
        summary_window.destroy()  # Cerrar la ventana de resumen
        root.destroy()  # Cerrar la ventana principal

def save_as_pdf():
    generate_graph()  # Primero genera el gráfico y lo guarda como imagen
    summary_text = "Resumen de tus respuestas:\n\n"
    for category, scores in answers.items():
        avg_score = sum(scores) / len(scores)
        summary_text += f"{category}: {avg_score:.2f}/7\n"
    generate_pdf_with_summary(summary_text)  # Luego genera el PDF con el resumen y la imagen del gráfico

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


def generate_summary():
    global summary_window
    summary_window = Tk()
    summary_window.title("Resumen del Test de Personalidad")
    
    # Calcular el resumen (promedio de las respuestas para cada categoría)
    summary_text = "Resumen de tus respuestas:\n\n"
    for category, scores in answers.items():
        avg_score = sum(scores) / len(scores)
        summary_text += f"{category}: {avg_score:.2f}/7\n"
    
    Label(summary_window, text=summary_text, font=("Arial", 12)).pack(pady=20)
    
    Button(summary_window, text="Guardar como PDF", command=save_as_pdf).pack(pady=10)
    # Button(summary_window, text="Ver en Gráfico", command=generate_graph).pack(pady=10)
    Button(summary_window, text="Cerrar", command=confirm_exit).pack(pady=10)

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
        background_image = "media/background.png"

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
    # plt.show()

def update_progressbar():
    total_questions = sum(len(v) for v in questions.values())
    percentage_complete = (current_question / total_questions) * 100
    progress_bar['value'] = percentage_complete

def reset_test():
    # Ventana emergente de confirmación
    response = messagebox.askyesno("Confirmar reinicio", "¿Estás seguro de que quieres reiniciar el test?")
    if not response:
        return  # Si el usuario selecciona 'No', no haremos nada y saldremos de la función

    global answers, current_question
    answers = {}  # Reiniciar las respuestas
    current_question = 0  # Reiniciar el contador de preguntas
    question_label.config(text="Presiona Siguiente para comenzar el test.")  # Reiniciar el texto de la etiqueta de pregunta
    scale.set(0)  # Reiniciar la escala

# Recopilar nombre y edad antes de comenzar el test
accept_terms_and_conditions()

# Ventana principal
root = Tk()
root.title("Test de Personalidad")
root.attributes('-fullscreen', True)
root.configure(bg="#f5f5f5")

# Cargar y ajustar la única imagen que se usará
original_image = Image.open("media/front.png")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
resized_image = original_image.resize((screen_width, screen_height), Image.LANCZOS)
front_image = ImageTk.PhotoImage(resized_image)

# Marco centrado
center_frame = Frame(root, bg="#f5f5f5")
center_frame.place(relx=0.5, rely=0.5, anchor='center')

question_label = Label(center_frame, text="Presiona Siguiente para comenzar el test.", bg="#f5f5f5", font=("Helvetica", 14), fg="#333333")
question_label.pack(pady=20)

# Fondo de la ventana (único layer)
front_label = Label(root, image=front_image, bg="#f5f5f5")
front_label.place(relx=0.5, rely=0.5, anchor='center')
front_label.lower()  # Enviar la etiqueta al fondo

# Escala y etiquetas
scale_frame = Frame(center_frame, bg="#f5f5f5")
scale_frame.pack(pady=10)

left_reference_label = Label(scale_frame, text="No me identifico", bg="#f5f5f5", font=("Helvetica", 10), fg="#555555")
left_reference_label.pack(side="left", padx=5)

scale = Scale(scale_frame, from_=1, to=7, orient="horizontal", bg="#e0e0e0", sliderlength=30, width=15, highlightthickness=0)
scale.pack(side="left", pady=20)

right_reference_label = Label(scale_frame, text="Me identifico totalmente", bg="#f5f5f5", font=("Helvetica", 10), fg="#555555")
right_reference_label.pack(side="left", padx=5)

# Botones
button_frame = Frame(center_frame, bg="#f5f5f5")
button_frame.pack(pady=10)

next_button = Button(button_frame, text="Siguiente", command=lambda: [next_question(), update_progressbar()], bg="#4caf50", fg="white", relief="flat", font=("Helvetica", 10))
next_button.pack(side="left", padx=5)

finish_button = Button(button_frame, text="Finalizar", command=generate_summary, bg="#ff5722", fg="white", relief="flat", font=("Helvetica", 10))
finish_button.pack(side="left", padx=5)

reset_button = Button(button_frame, text="Reiniciar", command=lambda: [reset_test(), update_progressbar()], bg="#607d8b", fg="white", relief="flat", font=("Helvetica", 10))
reset_button.pack(side="left", padx=5)

# Barra de progreso
progress_bar = ttk.Progressbar(center_frame, orient="horizontal", length=600, mode="determinate", style="TProgressbar")
progress_bar.pack(pady=20)

root.mainloop()
