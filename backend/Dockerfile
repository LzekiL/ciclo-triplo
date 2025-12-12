# 1️⃣ Imagen base Ubuntu con Python 3.10
FROM ubuntu:22.04

# 2️⃣ Variables de entorno para evitar interacciones durante la instalación
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# 3️⃣ Instalar dependencias de sistema necesarias
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3-pip \
    build-essential \
    wget \
    git \
    libbz2-dev \
    liblzma-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 4️⃣ Actualizar pip
RUN python3.10 -m pip install --upgrade pip

# 5️⃣ Copiar requirements.txt e instalar dependencias de Python
WORKDIR /app
COPY requirements.txt .
RUN python3.10 -m pip install --no-cache-dir -r requirements.txt

# 6️⃣ Copiar el código de la app
COPY . .

# 7️⃣ Comando para arrancar la app
CMD ["python3.10", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
