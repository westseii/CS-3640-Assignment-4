from scapy.all import sr1
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, UDP

from scapy.packet import ls


class DNSProber:
    """
    This class contains functions needed to:
     (1) craft and send DNS queries of a specific type for a specific domain to a specific resolver.
     (2) parse and save the IP addresses from the DNS responses.

    You will find the DNS and DNSQR classes from scapy.layers.dns helpful for crafting a DNS query packet.
    You will find the sr1 method from scapy.all helpful for sending and receiving packets.
    You will find the `dir()` method helpful to explore the structure and attributes of the packets received.
        Read more about `dir()` here: https://docs.python.org/3/library/functions.html#dir
    """

    def __init__(self, resolver, domain, query_type):
        self.resolver = resolver
        self.query_type = query_type
        self.domain = domain
        self.dns_query, self.dns_response = None, None
        self.returned_ips = []
        self.__send_dns_query()
        self.__parse_dns_response()

    def __send_dns_query(self):
        """
        In this method, you need to construct a DNS query packet of type `self.query_type`
         to the resolver IP in `self.resolver` for the domain in `self.domain`.

        Save this query packet to `self.dns_query`.

        Once this packet is constructed, use Scapy's sr1 method to send the query and record
        the DNS response.

        Save the response packet to `self.dns_response`.
        :return:
        """

        # explore...
        # ls(IP)
        # ls(UDP)
        # ls(DNS)
        # ls(DNSQR)

        # construct a DNS query packet
        packet = IP(dst=self.resolver) / \
            UDP(dport=53) / \
            DNS(rd=1, qd=DNSQR(qname=self.domain, qtype=self.query_type))
        self.dns_query = packet

        # print(packet.src)

        # send the query
        response = sr1(packet)  # request/response
        self.dns_response = response

        # show the structure and attributes of the packet
        # self.dns_response.show()

        # sudo -E python3 DNSProbes.py
        #      -E    Indicates to the security policy that the user wishes to preserve their existing environment variables
        #            Fix for:    ModuleNotFoundError: No module named 'scapy'

    def __parse_dns_response(self):
        """
        Extract the IP addresses contained in the answers field of the DNS response.

        Save these to the `self.returned_ips` list.
        :return:
        """

        # iterate all the answers in the answers field
        for ans in range(self.dns_response[DNS].ancount):
            self.returned_ips.append(self.dns_response[DNS].an[ans].rdata)


def main():
    dnsp = DNSProber(resolver='8.8.8.8',
                     domain='toutatis.cs.uiowa.edu', query_type='A')
    print("DNS Query:", dnsp.dns_query.summary())
    print("DNS Response:", dnsp.dns_response.summary())
    print("DNS IPs returned:", dnsp.returned_ips)


if __name__ == '__main__':
    main()
