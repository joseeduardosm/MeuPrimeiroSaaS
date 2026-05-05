sudo apt update && sudo apt upgrade -y
sudo apt install -y software-properties-common
sudo apt install -y \
  git \
  curl \
  build-essential \
  default-libmysqlclient-dev \
  pkg-config \
  libssl-dev \
  libffi-dev \
  mariadb-server \
  redis-server \
  python3.11-venv \
  python3.11-dev

# Crie o ambiente virtual
python3 -m venv .venv

# Ative o ambiente virtual
source .venv/bin/activate
deactivate

pip install --upgrade pip

pip install \
  django==5.1 \
  mysqlclient \
  python-dotenv \
  whitenoise \
  pillow

# Primeiro, rode o assistente de segurança
sudo mysql_secure_installation

sudo mysql

CREATE DATABASE clinicaos_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'clinicaos'@'localhost' IDENTIFIED BY 'odraude1992';
GRANT ALL PRIVILEGES ON clinicaos_db.* TO 'clinicaos'@'localhost';
FLUSH PRIVILEGES;
EXIT;

touch .env
python -c "import secrets; print(secrets.token_urlsafe(50))"

#inserir esses dados no .env
DJANGO_SECRET_KEY=troque-por-uma-chave-segura-aqui
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=clinicaos_db
DB_USER=clinicaos
DB_PASSWORD=odraude1992
DB_HOST=127.0.0.1
DB_PORT=5432

pip freeze > requirements.txt
pip install -r requirements.txt

django-admin --version
# deve mostrar: 5.1

# No arquivo .gitignore (crie se não existir)
echo ".env" >> .gitignore