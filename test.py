import os

def install_tunnel(iran_ip, foreign_ip, server_type, tunnel_type):
    try:
        if tunnel_type == "6to4":
            if server_type == "iran":
                commands = [
                    f"ip tunnel add 6to4_iran mode sit remote {foreign_ip} local {iran_ip}",
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
                    "iptables -t nat -A POSTROUTING -j MASQUERADE"
                ]
            elif server_type == "foreign":
                commands = [
                    f"ip tunnel add 6to4_Forign mode sit remote {iran_ip} local {foreign_ip}",
                    f"ip -6 addr add 2002:a00:100::2/64 dev 6to4_Forign",
                    "ip link set 6to4_Forign mtu 1480",
                    "ip link set 6to4_Forign up",
                    "ip -6 tunnel add GRE6Tun_Forign mode ip6gre remote 2002:a00:100::1 local 2002:a00:100::2",
                    "ip addr add 192.168.168.2/30 dev GRE6Tun_Forign",
                    "ip link set GRE6Tun_Forign mtu 1436",
                    "ip link set GRE6Tun_Forign up"
                ]
        elif tunnel_type == "iptables":
            commands = [
                "sysctl net.ipv4.ip_forward=1",
                f"iptables -t nat -A PREROUTING -p tcp --dport 22 -j DNAT --to-destination {iran_ip}",
                f"iptables -t nat -A PREROUTING -j DNAT --to-destination {foreign_ip}",
                "iptables -t nat -A POSTROUTING -j MASQUERADE"
            ]

        for command in commands:
            os.system(command)

        if os.path.exists("/etc/rc.local"):
            overwrite = input("File /etc/rc.local already exists. Do you want to overwrite it? (y/n): ")
            if overwrite.lower() != "y":
                print("Stopped process.")
                os.system("sleep 5")
                return

        with open("/etc/rc.local", "w") as f:
            f.write("#! /bin/bash\n")
            for command in commands:
                f.write(command + "\n")
            f.write("exit 0\n")

        os.system("sudo chmod +x /etc/rc.local")
        print("\033[92mSuccessful\033[0m")
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m")

def uninstall_tunnel(server_type):
    try:
        os.system("sudo rm /etc/rc.local")
        print("\033[92mSuccessful\033[0m")
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m")

def main():
    try:
        print("\033[94mTunnel System Installer/Uninstaller\033[0m")
        print("\033[93m-----------------------------------------\033[0m")
        action = input("\033[93mDo you want to:\n\033[92m1. Install\033[0m\n\033[91m2. Uninstall\033[0m\nEnter the number of your choice: ")
        if action not in ["1", "2"]:
            raise ValueError("Invalid action. Please enter '1' or '2'.")

        if action == "1":
            print("\033[93mSelect your tunnel type:\n\033[92m1. 6to4\033[0m\n\033[91m2. iptables\033[0m\nEnter the number of your tunnel type: ")
            tunnel_type =input()
            if tunnel_type not in ["1", "2"]:
                raise ValueError("Invalid tunnel type. Please enter '1' or '2'.")

            if tunnel_type == "1":
                tunnel_type = "6to4"
            elif tunnel_type == "2":
                tunnel_type = "iptables"

            if tunnel_type == "6to4":
                print("\033[93mSelect your server type:\n\033[92m1. Iran\033[0m\n\033[91m2. Foreign\033[0m\nEnter the number of your server type: ")
                server_type = input()
                if server_type not in ["1", "2"]:
                    raise ValueError("Invalid server type. Please enter '1' or '2'.")

                if server_type == "1":
                    server_type = "iran"
                elif server_type == "2":
                    server_type = "foreign"

                iran_ip = input("\033[93mEnter Iran server IP address: \033[0m")
                foreign_ip = input("\033[93mEnter Foreign server IP address: \033[0m")
                install_tunnel(iran_ip, foreign_ip, server_type, tunnel_type)
            elif tunnel_type == "iptables":
                print("\033[93mEnter Iran server IP address: \033[0m")
                iran_ip = input()
                print("\033[93mEnter Foreign server IP address: \033[0m")
                foreign_ip = input()
                server_type = "iran"
                install_tunnel(iran_ip, foreign_ip, server_type, tunnel_type)
        elif action == "2":
            print("\033[93mSelect your server type:\n\033[92m1. Iran\033[0m\n\033[91m2. Foreign\033[0m\nEnter the number of your server type: ")
            server_type= input()
            if server_type not in ["1", "2"]:
                raise ValueError("Invalid server type. Please enter '1' or '2'.")

            if server_type == "1":
                server_type = "iran"
            elif server_type == "2":
                server_type = "foreign"

            uninstall_tunnel(server_type)
    except Exception as e:
        print(f"\033[91mError: {e}\033[0m")

if __name__ == "__main__":
    main()
