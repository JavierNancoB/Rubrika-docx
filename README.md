# Rubrika-docx
Trabajo del ramo de taller de sistemas de información

## Archivos necesarios

Trabajaremos con Python, Flask como microframework y el framework pytest, ademas utilizaremos la libreria python-docx para la lectura de los archivos en formato .docx


# Instalación de Python, Flask y pytest

Instrucciones para configurar un entorno con Python, Flask y pytest.

## 1. Instalación de Python

### Windows:
1. Descarga el instalador desde: https://www.python.org/downloads/
2. Durante la instalación, selecciona la opción **"Add Python to PATH"**.
3. Verifica la instalación ejecutando en CMD:
   ```bash
   python --version
   ```

### macOS/Linux:
1. Instala Python (si no lo tienes ya):
   - macOS (Homebrew):
     ```bash
     brew install python
     ```
   - Debian/Ubuntu:
     ```bash
     sudo apt update && sudo apt install python3
     ```
   - Fedora:
     ```bash
     sudo dnf install python3
     ```
2. Verifica la instalación:
   ```bash
   python3 --version
   ```
### 1.1. Instalación de python-docx
    ```bash
   pip install python-docx
   ```
## 2. Entorno Virtual (Opcional)

1. Crea un entorno virtual (recomendado):
   ```bash
   python3 -m venv venv
   ```
2. Activa el entorno:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

## 3. Instalación de Flask y pytest

Con el entorno virtual activado (o globalmente), instala Flask y pytest:

```bash
pip install Flask pytest
```

## 4. Verificación de las Instalaciones

Verifica que Flask y pytest se instalaron correctamente:

- Flask:
  ```bash
  python -c "import flask; print(flask.__version__)"
  ```
- pytest:
  ```bash
  pytest --version
  ```

---

