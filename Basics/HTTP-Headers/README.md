# HTTP Headers Challenge

This challenge is an introduction to HTTP request headers.

HTTP headers are used by clients and servers to exchange additional information during requests and responses.

---

## 🎯 Objective

In this challenge, you must interact with the application and understand how HTTP request headers work in order to access the protected endpoint.

The flag is available at the `/flag` endpoint, but access is restricted.

You must send the correct headers to prove your identity.

---

## 🌐 Available endpoints

The application exposes the following endpoints:

- `/` → Main page
- `/flag` → Protected endpoint containing the flag

---

## 🧠 Hint

The server validates several HTTP headers before granting access.

Carefully inspect the server responses and pay attention to:

- Custom request headers
- Header formatting
- Datetime syntax
- Client identification

Understanding how to manipulate HTTP headers is the key to solving this challenge.
