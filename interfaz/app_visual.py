# interfaz/app_visual.py
import webbrowser
import time

if __name__ == "__main__":
    print("Abriendo interfaz en el navegador...")
    time.sleep(1)
    webbrowser.open("http://localhost:8000")
    print("Asegúrate de que el backend esté corriendo: uvicorn main:app --reload")