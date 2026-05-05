#!/usr/bin/env bash

set -e

echo "======================================="
echo "Instalação automatizada do Zabbix Agent 7"
echo "======================================="

# ================================
# ENTRADAS
# ================================

read -p "IP do servidor Zabbix: " ZBX_SERVER
read -p "Hostname da máquina (ex: srv-app-01): " HOSTNAME
read -p "HostMetadata (ex: linux-server): " HOST_METADATA

echo ""
echo "Resumo:"
echo "Servidor Zabbix: $ZBX_SERVER"
echo "Hostname: $HOSTNAME"
echo "HostMetadata: $HOST_METADATA"
echo ""

read -p "Confirmar instalação? (s/n): " CONFIRM
[[ "$CONFIRM" != "s" ]] && exit 1

# ================================
# ATUALIZAÇÃO
# ================================

echo "[1/5] Atualizando sistema..."
apt update

# ================================
# REPOSITÓRIO ZABBIX
# ================================

echo "[2/5] Instalando repositório Zabbix..."

wget -q https://repo.zabbix.com/zabbix/7.0/debian/pool/main/z/zabbix-release/zabbix-release_latest_7.0+debian12_all.deb
dpkg -i zabbix-release_latest_7.0+debian12_all.deb
apt update

# ================================
# INSTALAÇÃO AGENTE
# ================================

echo "[3/5] Instalando Zabbix Agent 2..."

apt install -y zabbix-agent2

# ================================
# CONFIGURAÇÃO
# ================================

echo "[4/5] Configurando agente..."

CONF_FILE="/etc/zabbix/zabbix_agent2.conf"

# Backup
cp $CONF_FILE ${CONF_FILE}.bkp

# Server
sed -i "s/^Server=.*/Server=${ZBX_SERVER}/" $CONF_FILE

# ServerActive
sed -i "s/^ServerActive=.*/ServerActive=${ZBX_SERVER}/" $CONF_FILE

# Hostname
sed -i "s/^Hostname=.*/Hostname=${HOSTNAME}/" $CONF_FILE

# HostMetadata (garante que exista)
grep -q "^HostMetadata=" $CONF_FILE \
    && sed -i "s/^HostMetadata=.*/HostMetadata=${HOST_METADATA}/" $CONF_FILE \
    || echo "HostMetadata=${HOST_METADATA}" >> $CONF_FILE

# ================================
# AJUSTAR HOSTNAME DO SISTEMA
# ================================

echo "[4/5] Ajustando hostname do sistema..."

hostnamectl set-hostname $HOSTNAME

# ================================
# SERVIÇO
# ================================

echo "[5/5] Iniciando serviço..."

systemctl restart zabbix-agent2
systemctl enable zabbix-agent2

# ================================
# VALIDAÇÃO
# ================================


echo "[Extra] Ajustando /etc/hosts..."

# Remove entradas antigas do hostname
sed -i "/127.0.1.1/d" /etc/hosts

# Adiciona nova entrada
echo "127.0.1.1   $HOSTNAME" >> /etc/hosts

echo ""
echo "======================================="
echo "Instalação concluída com sucesso!"
echo "======================================="

echo ""
echo "Validações recomendadas:"
echo "systemctl status zabbix-agent2"
echo "ss -tulnp | grep 10050"

echo ""
echo "Configuração aplicada:"
echo "Server=$ZBX_SERVER"
echo "ServerActive=$ZBX_SERVER"
echo "Hostname=$HOSTNAME"
echo "HostMetadata=$HOST_METADATA"
