# GestArg

GestArg es una aplicación web para gestionar los ingresos, gastos y clientes de tu emprendimiento.
La misma fue realizada por mí (**Felipe Lorenzo**), con el objetivo de armar el proyecto final del curso de Python de Coderhouse.

## Recursos del Proyecto

- **Video de prueba de la web:** [Ver Video](https://www.youtube.com/watch?v=xNJUvNSxPxU)
- **Excel con casos de prueba:** [Ver Excel](https://docs.google.com/spreadsheets/d/14IC8aXe93HsWkp_yVPUe0yr4FKvNER_o70lpPoGyXD0/edit?usp=sharing)

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

5. Crea un **superusuario** para acceder al panel de administración y acceder a todas las funcionalidad de la página:

    ```bash
    python manage.py createsuperuser

6. Ejecuta el servidor de desarrollo:

    ```bash
    python manage.py runserver

# AppFinanzas, Users y Landing.

AppFinanzas: Unica aplicación que se encarga de manejar los ingresos, gastos y clientes.
Users: Maneja los login, registros y edición de usuarios.
Landing: Da estructura a la web sin login del proyecto.

## Modelos

- **Cliente:** Modela los datos de los clientes, incluyendo razón social, email y teléfono.
- **Ingreso:** Representa un ingreso, con atributos como fecha, descripción, monto y cliente.
- **Gasto:** Representa un gasto, con atributos similares a los de Ingreso.
- **Profile:** Maneja los IDs de las fotos de perfil de los usuarios que se almacenan en Media.

## Formularios

- **ClienteForm:** Formulario para crear y actualizar instancias de Cliente.
- **IngresoForm:** Formulario para crear y actualizar instancias de Ingreso.
- **GastoForm:** Formulario para crear y actualizar instancias de Gasto.
- **BuscarClienteForm:** Formulario para buscar clientes por razon social o email. 
- **UserRegisterForm** Maneja el registro de usuarios.
- **UserEditForm** Maneja la edición de usuarios.

## <> ##

## Uso de la Página Web

La aplicación GestArg proporciona una interfaz web para gestionar ingresos, gastos y clientes.

1. **Navegación**: Utiliza el menú navegable en el margen izquierdo para moverte entre las secciones de **Ingresos**, **Gastos**,  **Clientes** y **ManejarStaff**.

2. **Gestión de Ingresos**:
   - **Agregar Ingreso**: Accede a la vista de agregar un nuevo ingreso desde la sección de ingresos.
   - **Mostrar Ingresos**: Visualiza la lista de ingresos, con opciones para buscar, editar o eliminar ingresos existentes.

3. **Gestión de Gastos**:
   - **Agregar Gasto**: Accede a la vista de agregar un nuevo gasto desde la sección de gastos.
   - **Mostrar Gastos**: Visualiza la lista de gastos, con opciones para buscar, editar o eliminar gastos existentes.

4. **Gestión de Clientes**:
   - **Agregar Cliente**: Accede a la vista de agregar un nuevo cliente desde la sección de clientes.
   - **Mostrar Clientes**: Visualiza la lista de clientes, con opciones para buscar, editar o eliminar clientes existentes.

5. **Manejo de Staff**:
   - **Gestión de usuarios**: Accede a la vista para eliminar usuarios o darles perfil de Staff para que puedan hacer un CRUD completo.

Cada sección permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre los modelos correspondientes, facilitando la gestión completa de tus datos financieros y de clientes.

Bootstrap: https://startbootstrap.com/template/simple-sidebar

FIN