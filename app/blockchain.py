import hashlib
import json
from datetime import datetime, timezone


class SmartContract:
    """
    Smart contract imobiliário que valida regras de negócio antes de registrar
    transações na blockchain. Simula contratos inteligentes sem rede distribuída.
    """

    @staticmethod
    def validate_listing(data: dict) -> tuple[bool, str]:
        """Valida se um imóvel pode ser registrado na blockchain."""
        price_str = str(data.get("price", "0")).replace(".", "").replace(",", ".")
        try:
            price = float(price_str)
        except ValueError:
            price = 0.0

        if price <= 0:
            return False, "Preço inválido: deve ser maior que zero."

        if not data.get("city"):
            return False, "Cidade é obrigatória."

        if not data.get("neighborhood"):
            return False, "Bairro é obrigatório."

        usable_area = data.get("usable_area", 0) or 0
        if usable_area <= 0:
            return False, "Área útil deve ser maior que zero."

        return True, "Contrato validado com sucesso."

    @staticmethod
    def validate_transaction(listing_id: int, action: str) -> tuple[bool, str]:
        """Valida uma transação sobre um imóvel existente."""
        allowed_actions = {"REGISTER", "UPDATE", "DEACTIVATE"}
        if action not in allowed_actions:
            return False, f"Ação '{action}' não permitida. Use: {allowed_actions}"
        return True, f"Transação '{action}' autorizada para imóvel #{listing_id}."


class Block:
    """Representa um bloco na blockchain imobiliária."""

    def __init__(self, index: int, data: dict, previous_hash: str):
        self.index = index
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self._calculate_hash()

    def _calculate_hash(self) -> str:
        content = json.dumps(
            {
                "index": self.index,
                "timestamp": self.timestamp,
                "data": self.data,
                "previous_hash": self.previous_hash,
            },
            sort_keys=True,
            ensure_ascii=False,
        )
        return hashlib.sha256(content.encode()).hexdigest()

    def is_valid(self) -> bool:
        return self.hash == self._calculate_hash()

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
        }


def create_genesis_block() -> Block:
    return Block(
        index=0,
        data={"message": "Genesis Block - Blockchain Imobiliária"},
        previous_hash="0" * 64,
    )


def create_block_from_record(index: int, data: dict, previous_hash: str) -> Block:
    """Cria um bloco a partir de dados de um imóvel."""
    contract = SmartContract()
    valid, message = contract.validate_listing(data)
    block_data = {**data, "contract_validation": message, "contract_valid": valid}
    return Block(index=index, data=block_data, previous_hash=previous_hash)
