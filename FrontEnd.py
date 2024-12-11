from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.graphics import RoundedRectangle
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
import backend

# Fondo Rosa
Window.clearcolor = (1, 0.89, 0.89, 1)

#Abrir en pantalla completa
Window.fullscreen= 'auto'

class LoginScreen(Screen):
    pass

class RegisterScreen(Screen):
    pass

class HomeScreen(Screen):
    pass

class MainWidget(Screen):
    pass
 
class RecommendationScreen(Screen):
    pass

class TSHScreen(Screen):
    pass

class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tries= 0
        self.lista_libros= []
    
    def build(self):
        Builder.load_file('interfaz.kv')
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(MainWidget(name='mainwidget'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(RecommendationScreen(name='recommendations'))
        sm.add_widget(TSHScreen(name='The Secret History'))
        return sm

    def mensaje(self, usuario, contraseña):
        # Obtén la pantalla de inicio de sesión
        screen = self.root.get_screen('login')
        message_label = screen.ids.message_label  
        
        # Validar campos vacíos
        if not usuario.strip() or not contraseña.strip():
            self._mostrar_mensaje(
                message_label, "Por favor, completa todos los campos.", color=(1, 0, 0, 1)
            )
            return

        # Validar credenciales con el backend
        validacion, mensaje = backend.login(usuario, contraseña, self.tries)
        if validacion:
            self.tries = 0  # Reinicia intentos en caso de éxito
            self.root.current = 'home'  # Cambia a la pantalla principal
        else:
            self.tries += 1
            self._mostrar_mensaje(
                message_label, mensaje, color=(1, 0, 0, 1)
            )

    def _mostrar_mensaje(self, label, mensaje, color=(0, 0, 0, 1)):
        """
        Actualiza el texto y color de un Label para mostrar mensajes.
        """
        label.text = mensaje
        label.color = color
    
    def registrar_usuario(self, name, lastname, username, mail, pwd1, pwd2):
        """
        Llama a la función del backend para registrar un usuario.
        """
        screen = self.root.get_screen('register')
        message_label = screen.ids.register_message  # Referencia al Label para mensajes

        # Llamar al backend
        exito, mensaje = backend.register( name, lastname, username, mail, pwd1, pwd2)

        if exito:
            # Mostrar éxito y redirigir
            message_label.text = "¡Registro exitoso!"
            message_label.color = (0, 1, 0, 1)  # Verde
            self.root.current = 'login'  # Cambia a la pantalla de inicio de sesión
        else:
            # Mostrar el mensaje de error
            message_label.text = mensaje
            message_label.color = (1, 0, 0, 1)  # Rojo
            
    def book(self):
        # Acceder a la pantalla mainwidget y obtener los valores de entrada
        main_widget = self.root.get_screen('mainwidget')

        titulo = main_widget.ids.titulo_input.text.strip()
        autor = main_widget.ids.autor_input.text.strip()
        tiempo = main_widget.ids.tiempo_input.text.strip()
        print(tiempo)
        print(autor)
     
        # Validar que al menos uno de los campos (título o autor) esté lleno
        if not titulo and not autor:
        # Mostrar mensaje de error si ambos campos están vacíos
         main_widget.ids.error_label.text = "Por favor, completa al menos un campo."
         main_widget.ids.error_label.color = (1, 0, 0, 1)  # Color rojo
         return

        if tiempo == "Elegí una opción":
            main_widget.ids.error_label.text = "Error: Completa cuánto tiempo quieres alquilar."
            main_widget.ids.error_label.color = (1, 0, 0, 1)  # Rojo para error
            return

        # Llamar a la función del backend para buscar libros
        backend.alquiler(titulo, autor, tiempo, main_widget)
    def show_book_selection_popup(self, libros):
        # Crear un Spinner para las opciones de libros
        spinner = Spinner(text="Selecciona el libro", values=[libro['titulo'] for libro in libros])
        
        # Función que se llama cuando se selecciona un libro
        def on_book_selected(spinner, text):
            print(f"Libro seleccionado: {text}")
            popup.dismiss()  
            
            # Cambiar a la pantalla deseada
            self.root.current = 'The Secret History'  # o la pantalla que quieras
            
        spinner.bind(text=on_book_selected)
        
        # Crear el Popup con el Spinner
        popup = Popup(
            title="Selecciona un libro",
            content=spinner,
            size_hint=(None, None),
            size=(400, 400)
        )
        popup.open()

if __name__ == "__main__":
    MyApp().run()
    