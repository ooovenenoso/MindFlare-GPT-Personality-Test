# RadarBig5
The project consists of a personality questionnaire implemented with Python and the Tkinter library for the graphical user interface. The questionnaire is based on five personality dimensions: Openness to Experience, Conscientiousness, Extraversion, Agreeableness, and Neuroticism.

The code defines the questions associated with each personality dimension in a dictionary called "questions". Each dimension has a list of questions associated with it.

The application displays one question at a time in the graphical interface and allows the user to select a response on a scale from 1 to 5 using the Tkinter Scale widget. The user can move to the next question or go back to the previous question using the corresponding buttons.

Once the user answers all the questions, a radar chart is generated showing the user's personality profile based on the provided answers. The chart is created using the Matplotlib library.

Additionally, the code allows saving the user's answers in a CSV file named "respuestas_personalidad.csv" which contains the personality dimension and the associated answers.

In summary, the project implements an interactive personality questionnaire with a graphical user interface that collects and analyzes the user's answers to generate a visual personality profile.
