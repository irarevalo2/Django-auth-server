# Restaurant API - Django REST Server

API REST desarrollada con Django para la gestión de pedidos de un restaurante.

## Requisitos
- Docker
- Docker Compose

## Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone <repositorio>
cd Django-auth-server
```

### 2. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```bash
DEBUG=1
MYSQL_DATABASE=restaurant_db
MYSQL_USER=restaurant_user
MYSQL_PASSWORD=restaurant_pass
MYSQL_ROOT_PASSWORD=rootpass
MYSQL_HOST=db
MYSQL_PORT=3306
SECRET_KEY=clave-secreta
```

### 3. Ejecutar con Docker Compose

```bash
docker-compose up --build
```

La API estará disponible en `http://localhost:8000`

### 4. Crear superusuario

```bash
docker-compose exec web python manage.py createsuperuser
```

## Endpoints de la API

### Autenticación

| Método | Endpoint | Descripción | Acceso |
|--------|----------|-------------|--------|
| POST | `/api/users/register/` | Registro de usuario | Público |
| POST | `/api/users/login/` | Iniciar sesión | Público |
| POST | `/api/users/logout/` | Cerrar sesión | Autenticado |

### Usuarios

| Método | Endpoint | Descripción | Acceso |
|--------|----------|-------------|--------|
| GET | `/api/users/` | Listar usuarios | Solo Admin |
| GET | `/api/users/me/` | Perfil actual | Autenticado |
| GET | `/api/users/{id}/` | Detalle usuario | Admin o propio |
| PUT | `/api/users/{id}/` | Actualizar usuario | Admin o propio |
| DELETE | `/api/users/{id}/` | Eliminar usuario | Solo Admin |
| POST | `/api/users/{id}/assign-group/` | Asignar grupo | Solo Admin |
| GET | `/api/users/groups/` | Listar grupos | Autenticado |
| POST | `/api/users/change-password/` | Cambiar contraseña | Autenticado |

### Mesas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/mesas/` | Listar mesas |
| POST | `/api/mesas/create/` | Crear mesa |
| GET | `/api/mesas/{id}/` | Detalle mesa |
| PUT | `/api/mesas/{id}/update/` | Actualizar mesa |
| DELETE | `/api/mesas/{id}/delete/` | Eliminar mesa (solo admin) |
| GET | `/api/mesas/{id}/pedidos/` | Pedidos de una mesa (API personalizada) |

### Pedidos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/pedidos/` | Listar pedidos |
| POST | `/api/pedidos/create/` | Crear pedido |
| GET | `/api/pedidos/{id}/` | Detalle pedido |
| PUT | `/api/pedidos/{id}/` | Actualizar pedido |
| DELETE | `/api/pedidos/{id}/delete/` | Eliminar pedido (solo admin) |

### ViewSet de Pedidos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/pedidos-viewset/` | Listar pedidos |
| POST | `/api/pedidos-viewset/` | Crear pedido |
| GET | `/api/pedidos-viewset/{id}/` | Detalle pedido |
| PUT | `/api/pedidos-viewset/{id}/` | Actualizar pedido |
| DELETE | `/api/pedidos-viewset/{id}/` | Eliminar pedido (solo admin) |

## Grupos de Usuarios

### Administradores
- Acceso completo (CRUD) a todos los modelos
- Pueden eliminar mesas, pedidos y usuarios
- Pueden asignar grupos a usuarios

### Empleados
- Pueden crear, leer y actualizar mesas y pedidos
- **NO pueden eliminar** registros
- No pueden gestionar usuarios

## Estructura del Proyecto

```
Django-auth-server/
├── docker-compose.yml      # Configuración de Docker Compose
├── Dockerfile              # Imagen Docker para Django
├── requirements.txt        # Dependencias Python
├── manage.py
├── config/
│   ├── settings.py         # Configuración de Django
│   ├── urls.py             # URLs principales
│   └── wsgi.py
├── users/
│   ├── serializers.py      # Serializadores de Usuario
│   ├── views.py            # Vistas de autenticación
│   └── urls.py
└── restaurant/
    ├── models.py           # Modelos Mesa y Pedido
    ├── serializers.py      # Serializadores
    ├── views.py            # Vistas genéricas y ViewSet
    ├── permissions.py      # Permisos personalizados
    ├── urls.py
    └── admin.py
```

## Ejemplos de Uso

### Registro de usuario

```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "empleado1", "email": "empleado1@test.com", "password": "Password123!", "password_confirm": "Password123!", "first_name": "Juan", "last_name": "Pérez"}'
```

### Login

```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "empleado1", "password": "Password123!"}'
```

### Crear mesa

```bash
curl -X POST http://localhost:8000/api/mesas/create/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=<tu_session_id>" \
  -d '{"numero": 1, "capacidad": 4, "estado": "disponible"}'
```

### Crear pedido

```bash
curl -X POST http://localhost:8000/api/pedidos/create/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=<tu_session_id>" \
  -d '{"mesa": 1, "descripcion": "2 pizzas margarita", "total": 25.50}'
```

