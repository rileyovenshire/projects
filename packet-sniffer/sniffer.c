#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <pcap/pcap.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>
#include <netinet/ip_icmp.h>

/* ------------------------------------------------------------------------------------------
 * Packet Sniffer
 *
 * This project was completed by way of a tutorial put on by Vic Hargrave. This is my first real foray into network programming, and I am extremely grateful for his contributions to the open-source community and I am so glad I was able to complete this project thanks to him. 
 * Direct link - https://vichargrave.github.io/programming/develop-a-packet-sniffer-with-libpcap/
 *
 * This program collects raw IP packets and inspects their header and payload fields. It collects: 
 * 	- protocol type
 * 	- source address
 * 	- destination address
 *
 * -----------------------------------------------------------------------------------------*/


pcap_t* handle; // libpcap handle
int linkhdrlen; // link header size - used during packet capture to skip of datalink layer header
int packets;	// number of packets captured, inc every time one is processed

int main(int argc, char *argv[]) {
	printf("Packet sniffer starting...\n");

	char device[256];
	char filter[256];
	int count = 0;
	int opt;

	*device = 0;
	*filter = 0;

	// fetch cli options
	while ((opt = getopt(argc, argv, "hi:n:")) != -1) {
		switch (opt) {
			case 'h':
				printf("usage: %s [-h] [-i interface] [-n count] [BPF expression]\n", argv[0]);
				exit(0);
				break;
			case 'i':
				strcpy(device, optarg);
				break;
			case 'n':
				count = atoi(optarg);
				break;
		}
	}

	// get packet capture filter expression
	for (int i=optind; i < argc; i++) {
		strcat(filter, argv[i]);
		strcat(filter, " ");
	}

	signal(SIGINT, stop_capture);
	signal(SIGTERM, stop_capture);
	signal(SIGQUIT, stop_capture);

	// create packet capture handle
	// takes first network interface if none is specified
	// gets network device source ip addy and netmask
	// opens device for capture
	// converts packet filter expression into filter binary
	// binds packet filter to libpcap handle
	handle = create_pcap_handle(device, filter);
	if (handle == NULL) {
		return -1;
	}

	// get link layer type + size
	//
 	get_link_header_len(handle);
	if (linkhdrlen == 0) {
		return -1;
	}

	// start packet capture with set count, or continually if counter is 0
	if (pcap_loop(handle, count, packet_handler, (u_char*)NULL) < 0) {
		fprintf(stderr, "pcap_loop failed: %s\n", pcap_geterr(handle));
		return -1;
	}

	stop_capture(0);
}
