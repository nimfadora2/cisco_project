import networkx as nx
import matplotlib.pyplot as plt
import ipaddress

neighbour = [['R1',['192.168.2.101','172.16.0.1'],['172.16.0.0/30','192.168.2.0/24']],
             ['R3',['192.168.2.103','172.16.0.2','172.16.0.6','10.0.50.6'],['172.16.0.4/30','172.16.0.0/30','10.0.50.0/30','10.0.50.4/30','192.168.2.0/24']],
             ['R2',['192.168.2.102','172.16.0.5'],['172.16.0.5/30','172.31.2.22/32','192.168.2.102/24']],
             ['R4',['192.168.2.104','10.0.50.1'],['192.168.2.104/24','10.0.50.1/30']],
             ['R5',['192.168.2.105','10.0.50.5'],['192.168.2.105/24','10.0.50.5/30']]
             ]



def graph(neighbour):
    ### Dictionary for keeping data to create graph ###
    neighborship_dict = {}

    ### Calculatiing and adding nodes and edges to network ###
    for router in neighbour:
        for ip in router[1]:
            times = 0
            for router_second in neighbour:
                if router_second == router:
                    continue
                for ip_net in router_second[2]:
                    if ipaddress.ip_address(ip) in ipaddress.ip_network(ip_net, strict=False):
                        times = times + 1
            for router_second in neighbour:
                if router_second == router:
                    continue
                for ip_net in router_second[2]:
                    if times == 0:
                        break
                    if ipaddress.ip_address(ip) in ipaddress.ip_network(ip_net, strict=False) and times == 1:
                        neighborship_dict[(router_second[0], router[0])] = ip
                        break
                    if ipaddress.ip_address(ip) in ipaddress.ip_network(ip_net, strict=False) and times > 1:
                        neighborship_dict[str(ipaddress.ip_network(ip_net, strict=False)), router[0]] = ip

    ### Creating graph ###
    G = nx.Graph()

    ### Drawing graph and saving it to file ###
    G.add_edges_from(neighborship_dict.keys())
    pos = nx.spring_layout(G, k=0.1, iterations=70)
    nx.draw_networkx_labels(G, pos, font_size=9, font_family="sans-serif", font_weight="bold")
    nx.draw_networkx_edges(G, pos, width=4, alpha=0.4, edge_color='black')
    nx.draw_networkx_edge_labels(G, pos, neighborship_dict, label_pos=0.3, font_size=6)
    nx.draw(G, pos, node_size=800, with_labels=False, node_color='b')
    plt.savefig('topology.png')

