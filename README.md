# 🚀 SmartCita REST API

A modern, high-performance **REST API** built with [FastAPI](https://fastapi.tiangolo.com/).  

Este proyecto consiste en una plataforma web diseñada para optimizar y automatizar los procesos de reclutamiento y selección de personal en pequeñas y medianas empresas (PYMES), integrando gestión de candidatos y entrevistas virtuales.

---

## ⚡ Características
- Desarrollado con **FastAPI** para un rendimiento y escalabilidad óptimos
- **Autenticación de usuarios** con JWT y OAuth2
- **Gestión de ofertas de empleo** para empleadores
- **Seguimiento de candidatos** y gestión de datos de candidatos
- **Programación de entrevistas** con soporte para colaboración en tiempo real
- **Integración con LiveKit** para videollamadas durante las entrevistas
- Integración con la base de datos **MongoDB**
- Desplegable en **AWS** con Docker y Uvicorn

---

## ⚡ Autor
Desarrollado por Esteban Francisco Acosta Aponte

**Backend Developer | Python | FastAPI | APIs**  

---

## 🧪 Desarrollo

```bash
fastapi dev main.py
```

---

## 🚀 Producción

Using `uvicorn`:

```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```

## 📝 Generar `requirements.txt`

Después de instalar las dependencias:

```bash
pip freeze > requirements.txt
```
