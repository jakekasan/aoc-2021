from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, ClassVar, Dict, List, Tuple


hex_map = {str(i): f"{i:b}".zfill(4) for i in range(10)}
hex_map.update({char: f"{(i + 10):b}".zfill(4) for i, char in enumerate("ABCDEF")})

def test_data() -> str:
    return "D2FE28"

def real_data() -> str:
    with Path("./input.txt").open() as f:
        return f.read().strip("\n")

def parse_hex(text: str) -> str:
    return "".join(hex_map[s] for s in text)

class Unparseable(Exception):
    
    def __init__(self, text: str):
        self.text = text

    def __str__(self) -> str:
        try:
            version = int(self.text[0:3], base=2)
        except:
            version = -1

        try:
            type_id = int(self.text[3:6], base=2)
        except:
            type_id = -1

        text = self.text[6:]
        return f"{version = }, {type_id = }, {text = }"

def to_bin(number: int, *, spaces: int) -> str:
    return f"{number:b}".zfill(spaces)

@dataclass
class Packet:
    type_id: int
    version: int

    @staticmethod
    def parse_bins(type_id_bin, version_bin) -> Tuple[int, int]:
        return int(type_id_bin, base=2), int(version_bin, base=2)

    @property
    def value(self) -> int:
        raise NotImplementedError
    
@dataclass
class LiteralPacket(Packet):
    _value: int

    @property
    def value(self) -> int:
        return self._value

    @classmethod
    def from_bin(cls, type_id_bin, version_bin, value_bin) -> LiteralPacket:
        type_id, version = cls.parse_bins(type_id_bin, version_bin)
        value = int(value_bin, base=2)
        return cls(type_id=type_id, version=version, _value=value)

@dataclass
class OperatorPacket(Packet):
    subpackets: List[Packet]

    @property
    def value(self) -> int:
        if self.type_id == 0:
            return sum(p.value for p in self.subpackets)
        if self.type_id == 1:
            product = 1
            for subpacket in self.subpackets:
                product *= subpacket.value
            return product
        if self.type_id == 2:
            return min(p.value for p in self.subpackets)
        if self.type_id == 3:
            return max(p.value for p in self.subpackets)
        if self.type_id == 5:
            a, b = self.subpackets
            return int(a.value > b.value)
        if self.type_id == 6:
            a, b = self.subpackets
            return int(a.value < b.value)
        if self.type_id == 7:
            a, b = self.subpackets
            return int(a.value == b.value)
        raise NotImplementedError

    @classmethod
    def from_bin(cls, type_id_bin: str, version_bin: str, packets: List[Packet]) -> OperatorPacket:
        type_id, version = cls.parse_bins(type_id_bin, version_bin)

        return cls(type_id=type_id, version=version, subpackets=packets)

class Parser(ABC):
    type_id: ClassVar[int]

    def can_parse(self, text: str) -> bool:
        return text[3:6] == to_bin(self.type_id, spaces=3)

    @abstractmethod
    def parse(self, text: str) -> Tuple[Packet, str]:
        raise NotImplementedError

class LiteralParser(Parser):
    type_id = 4

    def parse(self, text: str) -> Tuple[Packet, str]:
        version = text[0:3]
        type_id = text[3:6]
        text = text[6:]

        values = []
        start = ""
        while start != "0":
            start = text[0]
            data = text[1:5]
            text = text[5:]
            values.append(data)
        
        return LiteralPacket.from_bin(type_id, version, "".join(values)), text

class OperatorParser(Parser):
    type_id = 6

    def can_parse(self, text: str) -> bool:
        type_id = text[3:6]
        res = type_id != to_bin(4, spaces=3)
        return res

    @staticmethod
    def _get_bit_count(text: str) -> int:
        return int(text[7:24], base=2)

    def _parse_fixed_bitlength(self, text: str) -> Tuple[List[Packet], str]:
        bit_count_text = text[:15]
        bit_count = int(bit_count_text, base=2)
        remainder, text = text[15:(15 + bit_count)], text[15 + bit_count:]

        subpackets: List[Packet] = []
        pm = ParserManager()
        while remainder:
            packet, remainder = pm.parse(remainder)
            subpackets.append(packet)
        return subpackets, text
        
    def _parse_packet_count(self, text: str) -> Tuple[List[Packet], str]:
        packet_count_string = text[:11]
        packet_count = int(packet_count_string, base=2)
        remainder = text[11:]
        subpackets: List[Packet] = []
        pm = ParserManager()
        for _ in range(packet_count):
            packet, remainder = pm.parse(remainder)
            subpackets.append(packet)

        return subpackets, remainder

    def parse(self, text: str) -> Tuple[Packet, str]:
        version = text[0:3]
        type_id = text[3:6]
        length_type_id = text[6]

        subtext = text[7:]
        if length_type_id == "0":
            subpackets, remainder = self._parse_fixed_bitlength(subtext)
        elif length_type_id == "1":
            subpackets, remainder = self._parse_packet_count(subtext)
        else:
            raise Exception(f"Unknown {length_type_id = }")

        return OperatorPacket.from_bin(type_id, version, subpackets), remainder

class ParserManager:

    def __init__(self):
        self.parsers: List[Parser] = [
            OperatorParser(),
            LiteralParser()
        ]

    def parse(self, text: str) -> Tuple[Packet, str]:
        for parser in self.parsers:
            if parser.can_parse(text):
                try:
                    return parser.parse(text)
                except Exception as e:
                    print(type(e), str(e))
                    print(f"Parser {type(parser)} lied, could not parse {text}")
                    raise Unparseable(text) from e

        raise Unparseable(text)

# print(f"{LiteralParser().parse('110100101111111000101000')}")

# print(f"{OperatorParser().parse('00111000000000000110111101000101001010010001001000000000')}")

# print(f"{OperatorParser().parse('11101110000000001101010000001100100000100011000001100000')}")

def count_versions(*packets: Packet):
    total = 0

    for packet in packets:
        if isinstance(packet, LiteralPacket):
            total += packet.version
        elif isinstance(packet, OperatorPacket):
            subpackets_total = count_versions(*packet.subpackets) 
            total += subpackets_total + packet.version
        else:
            raise Exception

    return total

def run_examples():
    examples = [
        "8A004A801A8002F478",
        "620080001611562C8802118E34",
        "C0015000016115A2E0802F182340",
        "A0016C880162017C3686B18A3D4780"
    ]

    pm = ParserManager()
    for example in examples:
        binary = parse_hex(example)
        packet, _ = pm.parse(binary)
        print(f"{example = }, {count_versions(packet) = }", f"leftover = {_}")

def _parse_binary_data(binary_data: str) -> Packet:
    pm = ParserManager()

    packet, _ = pm.parse(binary_data)

    return packet

def part1(data: str) -> int:
    binary_data = parse_hex(data)
    packet = _parse_binary_data(binary_data)
    return count_versions(packet)

def part2(data: str) -> int:
    binary_data = parse_hex(data)
    packet = _parse_binary_data(binary_data)
    return packet.value

def run_examples2():
    examples: List[str] = [
        "C200B40A82",
        "04005AC33890",
        "880086C3E88112",
        "CE00C43D881120",
        "D8005AC2A8F0",
        "F600BC2D8F",
        "9C005AC2F8F0",
        "9C0141080250320F1802104A08"
    ]

    for example in examples:
        binary_data = parse_hex(example)
        packet = _parse_binary_data(binary_data)
        print(example, packet.value)

print(f"{part1(real_data()) = }, {part2(real_data())}")
