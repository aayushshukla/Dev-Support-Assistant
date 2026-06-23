# =====================================================
# TECHNOLOGY DETECTOR
# =====================================================

def detect_technology(
    title,
    content
):

    text = f"{title} {content}".lower()

    technology_map = {

        "spring boot": "Spring",
        "spring": "Spring",

        "fastapi": "FastAPI",

        "django": "Django",

        "flask": "Flask",

        "jsp": "Java",
        "servlet": "Java",
        "java": "Java",

        "react": "React",
        "angular": "Angular",
        "vue": "Vue",

        "docker": "Docker",
        "kubernetes": "Kubernetes",

        "postgresql": "PostgreSQL",
        "postgres": "PostgreSQL",
        "mysql": "MySQL",
        "mongodb": "MongoDB",

        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",

        "kafka": "Kafka",

        "terraform": "Terraform",

        "ansible": "Ansible"
    }

    for keyword, domain in technology_map.items():

        if keyword in text:

            return domain

    return "General"