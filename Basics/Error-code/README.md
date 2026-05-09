# Error Codes Challenge

This challenge is an introduction to HTTP status codes.

There are several classes of HTTP status codes, each with a different meaning:

- **2xx** → Success responses  
- **3xx** → Redirection messages  
- **4xx** → Client error responses  
- **5xx** → Server error responses  

---

## 🎯 Objective

In this challenge, you must interact with the application and understand how different HTTP status codes work in order to retrieve the four parts of a password.

Once reconstructed, submit the full password at the `/flag` endpoint.

---

## 🌐 Available endpoints

The application exposes the following endpoints:

- `/` → Main page (2xx)
- `/login` → Authentication & redirection (3xx)
- `/admin` → Restricted access (4xx)
- `/crash` → Server error simulation (5xx)
- `/flag` → Final submission endpoint

---

## 🧠 Hint

Each endpoint is associated with a different HTTP status class.  
Understanding how the server responds is key to completing the challenge.
