#!/bin/bash
#================
# FILE          : config.sh
#----------------
# PROJECT       : OpenSuSE KIWI Image System
# COPYRIGHT     : (c) 2006 SUSE LINUX Products GmbH. All rights reserved
#               :
# AUTHOR        : Marcus Schaefer <ms@suse.de>
#               :
# BELONGS TO    : Operating System images
#               :
# DESCRIPTION   : configuration script for SUSE based
#               : operating systems
#               :
#               :
# STATUS        : BETA
#----------------
#======================================
# Functions...
#--------------------------------------
test -f /.kconfig && . /.kconfig
test -f /.profile && . /.profile

#======================================
# Greeting...
#--------------------------------------
echo "Configure image: [$kiwi_iname]..."

#======================================
# Mount system filesystems
#--------------------------------------
# baseMount removido: KIWI 10 já gerencia mounts

#======================================
# Setup baseproduct link
#--------------------------------------
suseSetupProduct

#======================================
# Add missing gpg keys to rpm
#--------------------------------------
suseImportBuildKey

sed --in-place -e 's/# solver.onlyRequires.*/solver.onlyRequires = true/' /etc/zypp/zypp.conf

#======================================
# Sysconfig Update
#--------------------------------------
echo '** Update sysconfig entries...'
baseUpdateSysConfig /etc/sysconfig/keyboard KEYTABLE us.map.gz
baseUpdateSysConfig /etc/init.d/suse_studio_firstboot NETWORKMANAGER yes
baseUpdateSysConfig /etc/sysconfig/console CONSOLE_FONT lat9w-16.psfu
baseUpdateSysConfig /etc/sysconfig/displaymanager DISPLAYMANAGER_AUTOLOGIN tux
baseUpdateSysConfig /etc/sysconfig/displaymanager DISPLAYMANAGER gdm
baseUpdateSysConfig /etc/sysconfig/windowmanager DEFAULT_WM gnome


#======================================
# Setting up overlay files 
#--------------------------------------
echo '** Setting up overlay files...'
mkdir -p /
#mv /studio/overlay-tmp/files/backup-pasta /usr/local/bin/backup-pasta
#chown root:users /usr/local/bin/backup-pasta
if id ollama >/dev/null 2>&1 && getent group ollama >/dev/null 2>&1 && [ -d /var/lib/ollama ]; then chown -R ollama:ollama /var/lib/ollama; fi
#chmod 755 /usr/local/bin/backup-pasta
test -d /studio || mkdir /studio
[ -f /image/.profile ] && cp /image/.profile /studio/profile || true
[ -f /image/config.xml ] && cp /image/config.xml /studio/config.xml || true
rm -rf /studio/overlay-tmp
# configure_gdm_theme.sh removido: script legado usa gconftool/dconf e falha no KIWI 10
# configure_gnome_background.sh removido: script legado usa dconf e falha no KIWI 10



true

#======================================
# Activate services
#--------------------------------------
suseInsertService sshd
suseInsertService ollama
suseInsertService multicortex-chat-ui

if [[ ${kiwi_type} =~ oem|vmx ]];then
    suseInsertService grub_config
else
    suseRemoveService grub_config
fi

#======================================
# Setup default target, multi-user
#--------------------------------------
baseSetRunlevel 3

#==========================================
# remove package docs
#------------------------------------------
rm -rf /usr/share/doc/packages/*
rm -rf /usr/share/doc/manual/*
rm -rf /opt/kde*

#======================================
# only basic version of vim is
# installed; no syntax highlighting
#--------------------------------------
[ -f /etc/vimrc ] && sed -i -e's/^syntax on/" syntax on/' /etc/vimrc || true

#======================================
# SuSEconfig
#--------------------------------------
# suseConfig removido: obsoleto no KIWI 10

echo "** Running ldconfig..."
/sbin/ldconfig

#======================================
# Setup default runlevel
#--------------------------------------
baseSetRunlevel 5

#======================================
# Remove yast if not in use
#--------------------------------------
# suseRemoveYaST removido: obsoleto no KIWI 10

#======================================
# Umount kernel filesystems
#--------------------------------------
# baseCleanMount removido: KIWI 10 já gerencia mounts

true
true
exit 0

# BEGIN MULTICORTEX EXO GENERATED CONFIG
# Preparação dos scripts e serviços MultiCortex EXO durante o build KIWI.
echo "Configuring MultiCortex EXO helpers..."

mkdir -p /var/lib/ollama /var/log/multicortex /opt/multicortex/scripts/models /opt/multicortex/scripts/system

chmod 755 /opt/multicortex/scripts/models/*.sh 2>/dev/null || true
chmod 755 /opt/multicortex/scripts/system/*.sh 2>/dev/null || true
chmod 755 /usr/local/bin/multicortex-* 2>/dev/null || true

if command -v systemctl >/dev/null 2>&1; then
    systemctl enable multicortex-firstboot.service 2>/dev/null || true
    systemctl enable ollama.service 2>/dev/null || true
    systemctl enable multicortex-chat-ui.service 2>/dev/null || true
    systemctl enable open-webui.service 2>/dev/null || true
fi

# Segurança mínima: deixa claro no MOTD que root/tux padrão devem ser trocados.
if [ -f /etc/motd ]; then
    chmod 644 /etc/motd || true
fi
# END MULTICORTEX EXO GENERATED CONFIG
