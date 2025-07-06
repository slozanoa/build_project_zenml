
# Predecir cómo se sentirá un cliente sobre un producto antes de que lo ordene

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zenml)](https://pypi.org/project/zenml/)

**Planteamiento del problema**: A partir de los datos históricos de un cliente, nuestra tarea es predecir la puntuación de reseña para su próximo pedido o compra. Usaremos el [conjunto de datos públicos de comercio electrónico de Brasil por Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). Este conjunto de datos contiene información de 100,000 pedidos realizados entre 2016 y 2018 en varios marketplaces de Brasil. Sus características permiten visualizar cargos desde varias dimensiones: estado del pedido, precio, pago, rendimiento del flete, ubicación del cliente, atributos del producto y, finalmente, reseñas escritas por clientes. El objetivo aquí es predecir el nivel de satisfacción del cliente para un pedido dado con base en características como el estado del pedido, precio, pago, etc. Para lograrlo en un entorno real, usaremos [ZenML](https://zenml.io/) para construir una canalización lista para producción que prediga la puntuación de satisfacción del cliente.

Este repositorio tiene como propósito demostrar cómo [ZenML](https://github.com/zenml-io/zenml) permite a tu empresa construir y desplegar canalizaciones de aprendizaje automático de múltiples formas:

- Ofreciendo un marco y plantilla sobre los que puedes basar tu trabajo.
- Integrándose con herramientas como [MLflow](https://mlflow.org/) para despliegue, seguimiento, entre otros.
- Permitiéndote construir y desplegar fácilmente tus canalizaciones de machine learning.

## :snake: Requisitos de Python

Vamos a los paquetes de Python necesarios. Dentro del entorno de Python de tu preferencia, ejecuta:

```bash
git clone https://github.com/zenml-io/zenml-projects.git
cd zenml-projects/customer-satisfaction
pip install -r requirements.txt
```

Desde ZenML 0.20.0, viene con un panel de control basado en React. Este permite observar tus stacks, componentes y DAGs de las canalizaciones. Para acceder a esto, primero debes [lanzar el servidor y panel de control de ZenML localmente](https://docs.zenml.io/user-guide/starter-guide#explore-the-dashboard), pero antes debes instalar las dependencias opcionales del servidor ZenML:

```bash
pip install zenml["server"]
zenml up
```

Si vas a ejecutar el script `run_deployment.py`, también necesitas instalar algunas integraciones con ZenML:

```bash
zenml integration install mlflow -y
```

El proyecto solo puede ejecutarse con un stack de ZenML que tenga un rastreador de experimentos y un implementador de modelos de MLflow como componentes. Para configurarlo:

```bash
zenml integration install mlflow -y
zenml experiment-tracker register mlflow_tracker --flavor=mlflow
zenml model-deployer register mlflow --flavor=mlflow
zenml stack register mlflow_stack -a default -o default -d mlflow -e mlflow_tracker --set
```

## 📙 Recursos y Referencias

Escribimos un blog que explica este proyecto en profundidad: [Predecir cómo se sentirá un cliente sobre un producto antes de que lo ordene](https://blog.zenml.io/customer_satisfaction/).

También puedes ver el [video](https://youtu.be/L3_pFTlF9EQ) explicativo.

## :thumbsup: La Solución

Para construir un flujo de trabajo real que prediga la satisfacción del cliente, no basta con entrenar el modelo una vez. Construimos una canalización de extremo a extremo para predecir y desplegar continuamente el modelo de ML, junto con una app de datos que utiliza el modelo desplegado.

Esta canalización puede escalar en la nube y hacer seguimiento de parámetros y datos en cada ejecución. Incluye datos crudos, características, resultados, el modelo, parámetros del modelo y predicciones. ZenML facilita construir esta canalización de forma simple pero poderosa.

Usamos especialmente la [integración de MLflow](https://github.com/zenml-io/zenml/tree/main/examples) de ZenML, para:

- Seguir métricas y parámetros con MLflow tracking.
- Desplegar el modelo con MLflow deployment.
- Mostrar su uso real con [Streamlit](https://streamlit.io/).

### Canalización de Entrenamiento

Incluye los siguientes pasos:

- `ingest_data`: Ingesta los datos y crea un `DataFrame`.
- `clean_data`: Limpia los datos y elimina columnas no deseadas.
- `train_model`: Entrena el modelo y lo guarda con [MLflow autologging](https://www.mlflow.org/docs/latest/tracking.html).
- `evaluation`: Evalúa el modelo y guarda las métricas con MLflow.

### Canalización de Despliegue

El archivo `deployment_pipeline.py` extiende la canalización de entrenamiento e implementa un flujo de despliegue continuo. Usa un umbral configurable sobre el [MSE](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html) como criterio. Además de los pasos anteriores, incluye:

- `deployment_trigger`: Verifica si el nuevo modelo cumple el criterio para desplegarse.
- `model_deployer`: Despliega el modelo como servicio usando MLflow si se cumple el criterio.

MLflow registra los hiperparámetros, métricas y modelo entrenado como artefactos. Se lanza un servidor local de MLflow para servir el modelo, que se actualiza automáticamente si un nuevo modelo supera el umbral.

Una aplicación Streamlit consume este servicio modelo de forma asíncrona, usando:

```python
service = prediction_service_loader(
   pipeline_name="continuous_deployment_pipeline",
   pipeline_step_name="mlflow_model_deployer_step",
   running=False,
)
...
service.predict(...)  # Predecir con datos entrantes
```

También es posible desplegar en entornos más productivos (como Kubernetes) usando otras integraciones de ZenML, como [Seldon](https://github.com/zenml-io/zenml/tree/main/examples/seldon_deployment).

![training_and_deployment_pipeline](_assets/training_and_deployment_pipeline_updated.png)

## :notebook: Ejecutando el código

Puedes ejecutar ambas canalizaciones así:

- Canalización de entrenamiento:

```bash
python run_pipeline.py
```

- Canalización de despliegue continuo:

```bash
python run_deployment.py
```

## 🕹 Demo con Streamlit

Hay una demo en vivo con [Streamlit](https://streamlit.io/) que puedes ver [aquí](https://share.streamlit.io/ayush714/customer-satisfaction/main). Puedes ejecutarla localmente con:

```bash
streamlit run streamlit_app.py
```

## :question: Preguntas Frecuentes (FAQ)

1. Al ejecutar la canalización de despliegue me aparece: `No Step found for the name mlflow_deployer`.

   **Solución**: Tu almacén de artefactos fue sobrescrito. Debes eliminarlo y volver a ejecutar la canalización. Encuentra la ubicación con:

   ```bash
   zenml artifact-store describe
   ```

   Luego elimínalo con:

   ⚠️ **Nota**: ¡Este comando es destructivo! Escribe la ruta cuidadosamente:

   ```bash
   rm -rf RUTA
   ```

2. Me aparece el error: `No Environment component with name mlflow is currently registered.`

   **Solución**: Olvidaste instalar la integración MLflow. Instálala con:

   ```bash
   zenml integration install mlflow -y
   ```
