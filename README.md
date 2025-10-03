# 📘 Sistema de Gestión y Cobro de Cartera

Este proyecto busca construir una aplicación para que **empresas**
gestionen de forma sencilla su cartera, facturas y abonos, con soporte
multiusuario.

------------------------------------------------------------------------

## 📂 Entidades principales

### 🏢 Empresa

Representa a la organización que usará el sistema.\
- `id` → Identificador único (PK).\
- `nombre` → Nombre de la empresa.\
- `identificacion_tributaria` → NIT u otro identificador único.\
- `email_contacto` → Correo principal de contacto.\
- `fecha_registro` → Fecha de creación automática.\
- **Relaciones**:\
- 1 empresa → N clientes.\
- 1 empresa → N usuarios.

------------------------------------------------------------------------

### 👤 Usuario

Usuarios que pertenecen a una empresa. Permite tener roles y accesos
diferenciados.\
- `id` → Identificador único (PK).\
- `empresa_id` → FK → Empresa.\
- `nombre` → Nombre completo.\
- `email` → Único, usado para login.\
- `password_hash` → Contraseña encriptada.\
- `rol` → Ejemplo: `admin`, `contador`, `cobrador`.\
- `activo` → Estado de la cuenta (True/False).\
- `fecha_registro` → Fecha de alta automática.\
- **Relaciones**:\
- N usuarios → 1 empresa.

------------------------------------------------------------------------

### 👥 Cliente

Clientes de una empresa a los que se les emiten facturas.\
- `id` → Identificador único (PK).\
- `empresa_id` → FK → Empresa.\
- `nombre` → Nombre completo del cliente.\
- `email` → Email del cliente (indexado).\
- `telefono` → Opcional.\
- `identificacion_tributaria` → CC/NIT único.\
- `fecha_registro` → Fecha de creación automática.\
- `deuda_total` → Total adeudado (en centavos).\
- `abonado_total` → Total abonado (en centavos).\
- `estado_cartera` → Booleano (False = al día, True = en mora).\
- **Relaciones**:\
- 1 cliente → N facturas.\
- 1 cliente → N abonos.

------------------------------------------------------------------------

### 📑 Factura

Documento que representa una deuda emitida a un cliente.\
- `id` → Identificador único (PK).\
- `cliente_id` → FK → Cliente.\
- `monto_total` → Valor total (en centavos).\
- `fecha_emision` → Fecha automática de creación.\
- `fecha_vencimiento` → Fecha límite de pago.\
- `estado` → `pendiente`, `pagada`, `vencida`, `parcial`.\
- **Relaciones**:\
- 1 factura → N abonos.

------------------------------------------------------------------------

### 💰 Abono

Pagos parciales o totales de una factura.\
- `id` → Identificador único (PK).\
- `cliente_id` → FK → Cliente.\
- `factura_id` → FK → Factura.\
- `monto_abono` → Valor abonado (en centavos).\
- `fecha_abono` → Fecha automática.\
- `metodo_pago` → Ejemplo: efectivo, transferencia, tarjeta.\
- **Relaciones**:\
- 1 abono → 1 cliente.\
- 1 abono → 1 factura.

------------------------------------------------------------------------

## 🔄 Relaciones generales

-   **Empresa**
    -   tiene N **Usuarios**\
    -   tiene N **Clientes**
-   **Cliente**
    -   pertenece a 1 **Empresa**\
    -   tiene N **Facturas**\
    -   tiene N **Abonos**
-   **Factura**
    -   pertenece a 1 **Cliente**\
    -   tiene N **Abonos**
-   **Abono**
    -   pertenece a 1 **Cliente**\
    -   pertenece a 1 **Factura**

------------------------------------------------------------------------

**Crear migraciones iniciales con Alembic** ✅  
   - Se configuró Alembic con SQLite.  
   - Se ejecutó la primera migración que creó las tablas:  
     - `empresas`, `usuarios`, `clientes`, `facturas`, `abonos`.  
   - Verificado en SQLite con:  
     ```bash
     sqlite3 app.db
     .tables
     ```
     Resultado esperado:  
     ```
     abonos  clientes  facturas  empresas  usuarios  alembic_version
     ```