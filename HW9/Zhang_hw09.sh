#! /bin/bash

# clear all rules in the filter table
iptables -F
iptables -X
iptables -Z

# check all rules are cleared
iptables -L

# Place no restriction on outbound packets
iptables -P OUPUT ACCEPT

# Block a list of specific ip address for all incoming connection
iptables -A INPUT -s 199.95.207.0/24 -j DROP

# Block your computer from being pinged by all other hosts
iptabls -A INPUT -p icmp --icmp-type echo-request -j DROP

# Set up port-forwarding from an unused port of your choice to port 22 on your computer
# 192.168.229.142 is the ip address of my machine in the PAL3 LAN.
iptables -t nat -A PREROUTING -p tcp -d 192.168.229.142 --dport 23 -j DNAT --to-destination 192.168.228.142:22

# Allow for SSH access (port 22) to your machine from only the ecn.purdue.edu domain
iptables -A INPUT -p tcp -s ecn.purdue.edu --destination-port 22 -j ACCEPT

# Allow only a single IP address in the internet to access your machine for the HTTP service
# 128.46.75.97 is a static ip address of sopa.ecn.purdue.edu
iptables -A INPUT -i eth0 -p tcp -s 128.46.75.97 --destination-port 80 -j ACCEPT

# Permit Auth/Ident (port 113) that is used by some services like SMTP and IRC
iptables -A INPUT -p tcp --destination-port 113 -j ACCEPT

# Check the rules
iptables -L