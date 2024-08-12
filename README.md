# GestArg

GestArg es una aplicación web para gestionar los ingresos y gastos de tu emprendimiento.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Vverty/gestarg.git
   cd gestarg

2. Crea un entorno virtual y actívalo:
    
    ```bash
    python -m venv env
    source env/bin/activate  # En Windows: env\Scripts\activate

3. Instala las dependencias:

    ```bash
    pip install -r requirements.txt

4. Realiza las migraciones de la base de datos:

    ```bash
    python manage.py makemigrations
    python manage.py migrate

5. Crea un superusuario para acceder al panel de administración:

    ```bash
    python manage.py createsuperuser

6. Ejecuta el servidor de desarrollo:

    ```bash
    python manage.py runserver

# AppFinanzas

AppFinanzas: Unica aplicación que se encarga de manejar los ingresos, gastos y clientes.

## Modelos

- **Cliente:** Modela los datos de los clientes, incluyendo razón social, email y teléfono.
- **Ingreso:** Representa un ingreso, con atributos como fecha, descripción, monto y cliente.
- **Gasto:** Representa un gasto, con atributos similares a los de Ingreso.

## Vistas

- **agregar_cliente:** Vista para agregar un nuevo cliente.
- **mostrar_clientes:** Vista para mostrar la lista de clientes.
- **editar_cliente:** Vista para editar los datos de un cliente existente.
- **eliminar_cliente:** Vista para eliminar un cliente.
- **agregar_ingreso:** Vista para agregar un nuevo ingreso.
- **mostrar_ingresos:** Vista para mostrar la lista de ingresos.
- **editar_ingreso:** Vista para editar los datos de un ingreso existente.
- **eliminar_ingreso:** Vista para eliminar un ingreso.
- **agregar_gasto:** Vista para agregar un nuevo gasto.
- **mostrar_gastos:** Vista para mostrar la lista de gastos.
- **editar_gasto:** Vista para editar los datos de un gasto existente.
- **eliminar_gasto:** Vista para eliminar un gasto.

## Plantillas

- **base.html:** Plantilla base para la estructura general del sitio.
- **index.html:** Página de inicio con tarjetas que muestran el total de ingresos, gastos y cantidad de clientes.
- **mostrar_clientes.html:** Plantilla para mostrar la lista de clientes con opciones para buscar, agregar, editar y eliminar.
- **mostrar_ingresos.html:** Plantilla para mostrar la lista de ingresos con opciones para buscar, agregar, editar y eliminar.
- **mostrar_gastos.html:** Plantilla para mostrar la lista de gastos con opciones para buscar, agregar, editar y eliminar.
- **agregar_cliente.html:** Formulario para agregar un nuevo cliente.
- **agregar_ingreso.html:** Formulario para agregar un nuevo ingreso.
- **agregar_gasto.html:** Formulario para agregar un nuevo gasto.
- **editar_cliente.html:** Formulario para editar un cliente existente.
- **editar_ingreso.html:** Formulario para editar un ingreso existente.
- **editar_gasto.html:** Formulario para editar un gasto existente.

## Formularios

- **ClienteForm:** Formulario para crear y actualizar instancias de Cliente.
- **IngresoForm:** Formulario para crear y actualizar instancias de Ingreso.
- **GastoForm:** Formulario para crear y actualizar instancias de Gasto.
- **BuscarClienteForm:** Formulario para buscar clientes por razon social o email.

## <> ##

## Uso de la Página Web

La aplicación **AppFinanzas** proporciona una interfaz web para gestionar ingresos, gastos y clientes.

1. **Navegación**: Utiliza el menú navegable en el margen izquierdo para moverte entre las secciones de **Ingresos**, **Gastos** y **Clientes**.

2. **Gestión de Ingresos**:
   - **Agregar Ingreso**: Accede a la vista de agregar un nuevo ingreso desde la sección de ingresos.
   - **Mostrar Ingresos**: Visualiza la lista de ingresos, con opciones para buscar, editar o eliminar ingresos existentes.

3. **Gestión de Gastos**:
   - **Agregar Gasto**: Accede a la vista de agregar un nuevo gasto desde la sección de gastos.
   - **Mostrar Gastos**: Visualiza la lista de gastos, con opciones para buscar, editar o eliminar gastos existentes.

4. **Gestión de Clientes**:
   - **Agregar Cliente**: Accede a la vista de agregar un nuevo cliente desde la sección de clientes.
   - **Mostrar Clientes**: Visualiza la lista de clientes, con opciones para buscar, editar o eliminar clientes existentes.

Cada sección permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre los modelos correspondientes, facilitando la gestión completa de tus datos financieros y de clientes.

Bootstrap: https://startbootstrap.com/template/simple-sidebar
