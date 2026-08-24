# 🚀 Introduction
This space is dedicated to **SQL injections**. I'll gradually add more exercises to help anyone who wants to improve their skills on this topic.  

After each challenge, you will retrieve a flag like `HackUTT{README}` that confirms you have solved it.  

---

# 📖 Principle  
First of all, **what is a SQL injection?**  
It occurs when a user's input is not properly prepared, allowing us to inject arbitrary SQL queries that will be executed by the server. Using these queries, you might be able to:  
- Bypass authentication without a password  
- Leak information from databases  
- Read and write files on the server  

---

# ✏️ Exercises  

| Exercise | Description | Link |
|----------|-------------|------|
| Intro    | Basic SQL queries and simple login/register simulation | [./exercises/intro](exercises/intro)|
| Ex n°1     | Your first bypass: log in without a password | [./exercises/ex_1](exercises/ex_1) |
| Ex n°2     | Data leak using UNION-based SQL injection | [./exercises/ex_2](exercises/ex_2) |
| Ex n°3     | Exploit SQL errors to find hidden clues | [./exercises/ex_3](exercises/ex_3) |
| Ex n°4     | Second-order SQL injection to access `/admin` | [./exercises/ex_4](exercises/ex_4) |
| Ex n°5     | Read files from the server (`/` directory) | [./exercises/ex_5](exercises/ex_5) |

---
<br> 


