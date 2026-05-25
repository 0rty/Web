# HTTP Methods Challenge

This challenge is an introduction to HTTP request methods and their differences.

HTTP methods (also called HTTP verbs) define the action that a client wants to perform on a resource hosted by a web server.

Understanding the purpose of each method is essential in web development, API usage, and web security.

---

## 🎯 Objective

In this challenge, you must interact with the `/method` endpoint using different HTTP methods.

Each new method discovered and used by the server increases the progression counter.

Once all required methods have been successfully used, the flag will appear on the main page.

---

## 🌐 Available endpoints

The application exposes the following endpoints:

- `/` → Main page and challenge status
- `/method` → Endpoint accepting multiple HTTP methods

---

## 🧠 HTTP Methods Overview

Here are the methods supported by the application and their usual purpose:

### GET
Used to **retrieve information** from the server.

Example:
```http
GET /method HTTP/1.1
```

Typical usage:
- Access a webpage
- Retrieve API data

---

### POST
Used to **send data** to the server.

Example:
```http
POST /method HTTP/1.1
```

Typical usage:
- Submit a form
- Create a new resource

---

### PUT
Used to **replace or update** an existing resource.

Example:
```http
PUT /method HTTP/1.1
```

Typical usage:
- Update a user profile
- Replace a file or object

---

### PATCH
Used to **partially modify** a resource.

Example:
```http
PATCH /method HTTP/1.1
```

Difference with PUT:
- `PUT` usually replaces the whole resource
- `PATCH` modifies only specific fields

---

### DELETE
Used to **remove a resource** from the server.

Example:
```http
DELETE /method HTTP/1.1
```

Typical usage:
- Delete an account
- Remove stored data

---

### HEAD
Similar to `GET`, but the server only returns the **headers** and not the body.

Example:
```http
HEAD /method HTTP/1.1
```

Typical usage:
- Check if a resource exists
- Inspect metadata without downloading content

---

### OPTIONS
Used to ask the server which methods are allowed on a resource.

Example:
```http
OPTIONS /method HTTP/1.1
```

Typical usage:
- API discovery
- CORS preflight requests

---

## 🔍 Hint

The server keeps track of every unique HTTP method you use.

Try interacting with `/method` using all supported methods.

Useful tools:

- `curl`
- Burp Suite
- Postman
- Python requests

Example:

```bash
curl -X DELETE http://localhost:5003/method
```

---

## 📚 Learning goals

This challenge helps you understand:

- The role of HTTP methods
- The difference between common HTTP verbs
- REST API behavior
- How servers handle requests
- How to manually craft HTTP requests

---

## 🚩 Flag

The flag is revealed after successfully using all required HTTP methods.

Bonus: the application mentions additional HTTP methods such as:

- TRACE
- CONNECT

Try researching what they do and why they may be dangerous in some contexts.
