import os

def install_tunnel(iran_ip, foreign_ip, server_type):
    try:
        if server_type == "iran":
            commands = [
                "sudo nano /etc/rc.local && sudo chmod +x /etc/rc.local",
                f"#! /bin/bash\nip tunnel add 6to4_iran mode sit remote {foreign_ip} local {iran_ip}",
                f"ip -6 addr add 2002:a00:100::1/64 dev 6to4_iran",
                "ip link set 6to4_iran mtu 1480",
                "ip link set 6to4_iran up",
                "ip -6 tunnel add GRE6Tun_iran mode ip6gre remote 2002:a00:100::2 local 2002:a00:100::1",
                "ip addr add 192.168.168.1/30 dev GRE6Tun_iran",
                "ip link set GRE6Tun_iran mtu 1436",
                "ip link set GRE6Tun_iran up",
                "sysctl net.ipv4.ip_forward=1",
                "iptables -t nat -A PREROUTING -p tcp --dport 22 -j DNAT --to-destination 192.168.168.1",
                "iptables -t nat -A PREROUTING -j DNAT --to-destination 192.168.168.2",
                "iptables -t nat -A POSTROUTING -j MASQUERADE",
                "exit 0"
            ]
        elif server_type == "foreign":
            commands = [
                "sudo nano /etc/rc.local && sudo chmod +x /etc/rc.local",
                f"#! /bin/bash\nip tunnel add 6to4_Forign mode sit remote {iran_ip} local {foreign_ip}",
                f"ip -6 addr add 2002:a00:100::2/64 dev 6to4_Forign",
                "ip link set 6to4_Forign mtu 1480",
                "ip link set 6to4_Forign up",
                "ip -6 tunnel add GRE6Tun_Forign mode ip6gre remote 2002:a00:100::1 local 2002:a00:100::2",
                "ip addr add 192.168.168.2/30 dev GRE6Tun_Forign",
                "ip link set GRE6Tun_Forign mtu 1436",
                "ip link set GRE6Tun_Forign up",
                "exit 0"
            ]

        for command in commands:
            os.system(command)
        print("Successful")
    except Exception as e:
        print(f"Error: {e}")

def uninstall_tunnel(server_type):
    try:
        if server_type == "iran":
            commands = [
                "rm -r /etc/rc.local",
                "iptables -F",
                "iptables -X",
                "iptables -P INPUT ACCEPT",
                "iptables -P FORWARD ACCEPT",
                "iptables -P OUTPUT ACCEPT",
                "ip tunnel del 6to4_iran",
                "ip tunnel del GRE6Tun_iran"
            ]
        elif server_type == "foreign":
            commands = [
                "rm -r /etc/rc.local",
                "ip tunnel del 6to4_Forign",
                "ip tunnel del GRE6Tun_Forign"
            ]

        for command in commands:
            os.system(command)
        print("Successful")
    except Exception as e:
        print(f"Error: {e}")

def main():
    try:
        server_type = input("Is your server in Iran or Foreign? (iran/foreign): ")
        if server_type not in ["iran", "foreign"]:
            raise ValueError("Invalid server type. Please enter 'iran' or 'foreign'.")

        action = input("Do you want to install or uninstall the tunnel system? (install/uninstall): ")
        if action not in ["install", "uninstall"]:
            raise ValueError("Invalid action. Please enter 'install' or 'uninstall'.")

        if action == "install":
            iran_ip = input("Enter Iran server IP address: ")
            foreign_ip = input("Enter Foreign server IP address: ")
            install_tunnel(iran_ip, foreign_ip, server_type)
        elif action == "uninstall":
            uninstall_tunnel(server_type)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
