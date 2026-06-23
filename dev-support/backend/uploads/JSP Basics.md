# JSP Basics

JavaServer Pages (JSP) is a technology used to create dynamic web pages using Java.

## What is JSP?

JSP allows developers to embed Java code inside HTML pages.

A JSP file typically has the extension .jsp.

Example:

```jsp
<html>
<body>
<h1>Hello JSP</h1>
</body>
</html>
```

## JSP Lifecycle

The JSP lifecycle consists of:

1. Translation Phase
2. Compilation Phase
3. Class Loading
4. Instantiation
5. Initialization
6. Request Processing
7. Destruction

## JSP Directives

JSP provides directives to give instructions to the container.

Common directives:

- page
- include
- taglib

Example:

```jsp
<%@ page language="java" %>
```

## JSP Scriptlets

Scriptlets allow Java code inside JSP pages.

Example:

```jsp
<%
String name = "John";
out.println(name);
%>
```

## JSP Expression

Expressions are used to display values.

Example:

```jsp
<%= "Welcome to JSP" %>
```

## JSP Implicit Objects

JSP provides several implicit objects:

- request
- response
- session
- application
- pageContext
- out

## Summary

JSP is a server-side technology used to create dynamic web applications using Java.