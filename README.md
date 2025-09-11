# 🚀 FlowyHire REST API

A modern, high-performance **REST API** built with [FastAPI](https://fastapi.tiangolo.com/).  

This project powers **FlowyHire**, a recruitment platform that enables companies to **post job offers, manage applicants, schedule interviews, and conduct video calls**.  
It showcases expertise in **backend architecture, API design, authentication, database integration, and real-time communication**.

---

## ⚡ Features
- Built with **FastAPI** for performance and scalability  
- **User authentication** with JWT and OAuth2  
- **Job postings** management for employers  
- **Applicant tracking** and candidate data handling  
- **Interview scheduling** with support for real-time collaboration  
- **LiveKit integration** for video calls during interviews  
- Database integration with **MongoDB**  
- Deployable to **AWS** with Docker and Uvicorn  

---

## ⚡ Author
Developed by Esteban Francisco Acosta Aponte

**Backend Developer | Python | FastAPI | APIs**  

---

## 🧪 Development

```bash
fastapi dev main.py
```

---

## 🚀 Production

Using `uvicorn`:

```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```

## 📝 Generate `requirements.txt`

After installing your dependencies:

```bash
pip freeze > requirements.txt
```
