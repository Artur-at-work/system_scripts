import socket
import struct
import binascii

def eth_header(raw_data):
  dest, src, prototype = struct.unpack('! 6s 6s H', raw_data[:14])
  dest_mac = convert_mac(dest)
  src_mac = convert_mac(src)
  
  proto = socket.htons(prototype)
  data = raw_data[14:]
  return dest_mac, src_mac, proto, data


def ipv4_header(raw_data):
  version_header_length = raw_data[0]
  version = version_header_length >> 4
  header_length = (version_header_length & 15) * 4
  ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', raw_data[:20])
  data = raw_data[header_length:]
  src = convert_ip(src)
  target = convert_ip(target)
  return version, header_length, ttl, proto, src, target, data

def tcp_header( raw_data):
  src_port, dest_port, sequence, acknowledgment, offset_reserved_flags = struct.unpack('! H H L L H', raw_data[:14])
  offset = (offset_reserved_flags >> 12) * 4
  flag_urg = (offset_reserved_flags & 32) >> 5
  flag_ack = (offset_reserved_flags & 16) >> 4
  flag_psh = (offset_reserved_flags & 8) >> 3
  flag_rst = (offset_reserved_flags & 4) >> 2
  flag_syn = (offset_reserved_flags & 2) >> 1
  flag_fin = offset_reserved_flags & 1
  data = raw_data[offset:]

  return src_port, dest_port, sequence, acknowledgment, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data


def convert_mac(mac):
  #return "%x:%x:%x:%x:%x:%x" % struct.unpack("BBBBBB", mac)
  return binascii.hexlify(mac)


def convert_ip(addr):
  return '.'.join(map(str, addr))


def format_multi_line():
  pass

def main():
  tab_1 = "\t"
  tab_2 = "\t\t"
  tab_3 = "\t\t\t"
  tab_4 = "\t\t\t\t"
  s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
  while True:
    raw_data, addr = s.recvfrom(65535)
    eth = eth_header(raw_data)
    print('\nEth. Frame:')
    print('Dst.: {}, Src.: {}, Protocol: {}'.format(eth[0], eth[1], eth[2]))
    if eth[2] == 8:
      ipv4 = ipv4_header(eth[3])
      print(tab_1 + ' - ' + 'IPv4 Packet:')
      print(tab_2 + ' - ' + 'Ver.: {}, Header Length: {}, TTL: {},'.format(ipv4[1], ipv4[2], ipv4[3]))
      print(tab_2 + ' - ' + 'Src.: {}, Dst.: {}'.format(ipv4[4], ipv4[5]))
    if ipv4[3] == 6:
      tcp = tcp_header(ipv4[6])
      print(tab_1 + 'TCP Segment:')
      print(tab_2 + 'Src. Port: {}, Dest. Port: {}'.format(tcp[0], tcp[1]))
      print(tab_2 + 'Seq.: {}, Ack: {}'.format(tcp[2], tcp[3]))
      print(tab_2 + 'Flags:')
      print(tab_3 + 'URG: {}, ACK: {}, PSH:{}'.format(tcp[4], tcp[5], tcp[6]))
      print(tab_3 + 'RST: {}, SYN: {}, FIN:{}'.format(tcp[7], tcp[8], tcp[9]))
      if len(tcp[10]) > 0:
      # HTTP
        if tcp[0] == 80 or tcp[1] == 80:
          print(tab_2 + 'HTTP Data:')
        try:
          # TODO: convert tcp[10] as http, then split to http_info
          http_info = str(tcp[10]).split('\n')
          for line in http_info:
            print(tab_4 + str(line))
        except:
          print(tab_4, tcp[10])
        else:
          print(tab_2 + 'TCP Data:')
          print(tab_4, tcp[10])


main()

