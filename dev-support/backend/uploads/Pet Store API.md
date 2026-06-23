# Pet Store API

## Get Pet By ID

### Endpoint

GET /pets/{petId}

### Purpose

Retrieve details of a specific pet.

### Path Parameters

| Name  | Type    | Required | Description           |
| ----- | ------- | -------- | --------------------- |
| petId | integer | Yes      | Unique pet identifier |

### Request Example

GET /pets/100

### Response Example

```json
{
  "id": 100,
  "name": "Buddy",
  "type": "Dog",
  "status": "Available"
}
```

### Authentication

Bearer Token required.

Authorization: Bearer <token>

---

## Create Pet

### Endpoint

POST /pets

### Purpose

Create a new pet record.

### Request Body

```json
{
  "name": "Max",
  "type": "Dog",
  "status": "Available"
}
```

### Response Example

```json
{
  "id": 101,
  "name": "Max",
  "type": "Dog",
  "status": "Available"
}
```

### Authentication

Bearer Token required.

---

## Delete Pet

### Endpoint

DELETE /pets/{petId}

### Purpose

Delete an existing pet.

### Path Parameters

| Name  | Type    | Required |
| ----- | ------- | -------- |
| petId | integer | Yes      |

### Request Example

DELETE /pets/101

### Response Example

```json
{
  "message": "Pet deleted successfully"
}
```

### Authentication

Bearer Token required.
