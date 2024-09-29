from scapy.all import sniff
def process_packet(pkt):
	print(f"Packet captured:{pkt.summary()}")
def start_sniffer(packet_limit=10):
	print(f"Starting sniffer.... Capturing{packet_limit} packets")
	sniff(count=packet_limit,prn=process_packet)
if __name__=="__main__":
	start_sniffer(10)