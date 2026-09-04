from dataclasses import dataclass, field
from typing import List, Dict, Optional
import json, uuid

@dataclass
class Inbound:
    tag: str
    port: int
    protocol: str
    clients: List[Dict] = field(default_factory=list)
    def info(self):
        return f'{self.tag}: {self.protocol} на порту {self.port} ({len(self.clients)} клиентов)'
@dataclass
class VpnConfig:
    inbounds: List[Inbound] = field(default_factory=list)
    def add_inbound(self, inbound: Inbound):
        self.inbounds.append(inbound)
    def show_inbounds(self):
        for inbound in self.inbounds:
            print(inbound.info())
    def get_inbound_by_tag(self, tag: str)->Optional[Inbound]:
        for inbound in self.inbounds:
            if inbound.tag == tag:
                return inbound
        return None

    @classmethod
    def from_json_file(cls, filename: str) -> 'VpnConfig':
        with open(filename, "r", encoding='utf-8') as f:
            data = json.load(f)
        confing = cls()
        for inbound_data in data.get('inbounds', []):
            tag = inbound_data.get('tag', 'unnamed')
            port = inbound_data.get('port', 0)
            protocol = inbound_data.get('protocol', "Don't have")
            clients = inbound_data.get('settings', {}).get('clients', [])

            inbound = Inbound(tag, port, protocol, clients)
            confing.add_inbound(inbound)
        return confing
    def to_json_file(self, filename: str):
        all_inbounds=[]
        for inbound in self.inbounds:
            inbounds_dict= {
                "tag": inbound.tag,
                "port": inbound.port,
                "protocol": inbound.protocol,
                "settings": {"clients": inbound.clients}
            }
            all_inbounds.append(inbounds_dict)
        data = {"inbounds": all_inbounds}
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_client_to_inbound(self, tag: str, client_id: Optional[str] = None):
        
            # Найди inbound по tag
            # Сгенерируй UUID если client_id не передан
            # Добавь клиента в inbound.clients
        pass

