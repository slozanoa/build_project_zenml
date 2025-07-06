Crear aplicacion

- instalar version de python compatible con zenmlcrear ambiente virtual
 ```bash
  brew install pyenv

# 2. Instala Python 3.10.13 (solo se hace una vez)
pyenv install 3.10.13
```
- Crear ambiente virtual
```bash
  # Usa pyenv para usar Python 3.10.13 en este proyecto
pyenv local 3.12.0  # Esto crea un archivo `.python-version`

# Crea el nuevo entorno virtual con esa versión
python -m venv venv

# Activa el entorno
source venv/bin/activate

# Verifica que estás usando la versión correcta
python --version  # Debería mostrar Python 3.10.13
```
- Instalar pip install "zenml["server"]"
- zenml login --local

cuando todo esté listo ejecutar 
python run_pipeline.py
- zenml login --local
si da error ejecuta 
```
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
zenml login --local
```
