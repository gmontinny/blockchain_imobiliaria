# Artigo Técnico-Científico: Aplicação de Blockchain e Smart Contracts na Gestão e Rastreabilidade de Transações Imobiliárias

---

## Resumo

A digitalização do setor imobiliário enfrenta desafios históricos relacionados à transparência, integridade dos registros e prevenção a fraudes cadastrais. Este artigo apresenta o desenvolvimento e a fundamentação teórica de uma arquitetura baseada em conceitos de **Blockchain** e **Smart Contracts** integrada a uma API REST moderna desenvolvida em `Python` e `FastAPI`, suportada pelo banco de dados relacional `PostgreSQL` em ambiente containerizado com `Docker`. O sistema implementa uma cadeia de blocos com encadeamento criptográfico via algoritmo `SHA-256`, integrando um motor de validação automatizada de regras de negócio (*Smart Contract*) que audita anúncios provenientes de conjuntos de dados reais antes de sua gravação no livro-razão (*ledger*). O trabalho destina-se a servir como referência didática e técnica para estudantes universitários de Ciência da Computação, Engenharia de Software e Sistemas de Informação, detalhando os princípios matemáticos, arquiteturais e práticos da tecnologia de registros distribuídos.

**Palavras-chave:** Blockchain, Smart Contracts, Criptografia, SHA-256, FastAPI, Integridade de Dados, Mercado Imobiliário.

---

## 1. Introdução

O mercado imobiliário tradicional depende extensivamente de intermediários cartorários, plataformas centralizadas e processos manuais de checagem. Essa estrutura centralizada acarreta riscos como assimetria de informações, possibilidade de adulteração retroativa de históricos de preços e duplicidade de ofertas fraudulentas.

Com a evolução da Ciência da Computação e a consolidação das tecnologias de registro distribuído (*Distributed Ledger Technology* - DLT), propostas baseadas em cadeias de blocos (*blockchains*) surgiram como uma alternativa robusta para garantir a **imutabilidade**, a **rastreabilidade** e a **auditabilidade** pública ou corporativa de transações.

O presente projeto propõe uma abordagem arquitetural em que anúncios de imóveis são processados sob a ótica de transações criptográficas. Cada operação — seja criação (`REGISTER`) ou atualização (`UPDATE`) — passa por um contrato inteligente de validação e é selada em um bloco encadeado deterministicamente ao bloco anterior. O objetivo deste artigo é desmistificar esses conceitos para o público acadêmico, correlacionando a teoria criptográfica à sua implementação prática em software.

---

## 2. Fundamentação Teórica

### 2.1. Conceito e Estrutura de uma Blockchain

Uma *blockchain* é uma estrutura de dados sequencial composta por blocos encadeados linearmente no tempo. Cada bloco $B_i$ contém um conjunto de dados ou transações, metadados (como carimbo temporal ou `timestamp` e índice sequencial) e, crucialmente, o valor de resumo criptográfico (*hash*) do bloco imediatamente anterior ($H(B_{i-1})$).

```
┌─────────────────────────┐         ┌─────────────────────────┐
│     Bloco i-1           │         │        Bloco i          │
├─────────────────────────┤         ├─────────────────────────┤
│ Index: i-1              │         │ Index: i                │
│ Timestamp: t_{i-1}      │         │ Timestamp: t_i          │
│ Previous Hash: H(B_{i-2})│◄────────┤ Previous Hash: H(B_{i-1})│
│ Data: { ... }           │         │ Data: { ... }           │
│ Hash: H(B_{i-1})        │         │ Hash: H(B_i)            │
└─────────────────────────┘         └─────────────────────────┘
```

Essa amarração encadeada gera a propriedade de **resistência à adulteração**: caso um agente malicioso altere qualquer dado no bloco $B_{i-1}$, o seu *hash* recalculado resultará em um valor completamente divergente ($H'(B_{i-1}) \neq H(B_{i-1})$). Consequentemente, o apontamento armazenado em $B_i$ (`previous_hash`) torna-se inválido, quebrando a integridade de toda a cadeia subsequente.

### 2.2. Funções Hash Criptográficas e o Algoritmo SHA-256

No centro da integridade de uma *blockchain* está a **função hash criptográfica**. Trata-se de uma função matemática determinística $H: \{0,1\}^* \to \{0,1\}^n$ que mapeia uma entrada de tamanho arbitrário em uma cadeia de bits de tamanho fixo ($n = 256$ bits no caso do `SHA-256`).

Para ser considerada segura, a função hash deve atender a quatro propriedades fundamentais:

1. **Determinismo:** Uma mesma entrada $x$ sempre produzirá rigorosamente o mesmo valor de saída $H(x)$.
2. **Resistência à Pré-Imagem (Unidirecionalidade):** Dado um *hash* $y$, deve ser computacionalmente inviável encontrar qualquer entrada $x$ tal que $H(x) = y$.
3. **Resistência à Segunda Pré-Imagem e Colisões:** Deve ser computacionalmente inviável encontrar duas entradas distintas $x_1 \neq x_2$ tais que $H(x_1) = H(x_2)$.
4. **Efeito Avalanche:** Qualquer modificação mínima na entrada (como a inversão de um único bit) resulta em uma saída totalmente imprevisível e estatisticamente descorrelacionada da anterior.

### 2.3. Smart Contracts (Contratos Inteligentes)

Concebidos teoricamente por Nick Szabo na década de 1990, os **Smart Contracts** são protocolos computacionais autoexecutáveis concebidos para verificar, facilitar ou fazer cumprir digitalmente a negociação ou o desempenho de um acordo.

Diferente de um código convencional, o contrato inteligente atua como uma barreira regulatória determinística:
- Não admite arbitrariedade subjetiva.
- Valida pré-condições estruturais e lógicas antes de consentir com a persistência do estado no livro-razão.
- Registra não apenas o sucesso, mas também as eventuais rejeições e violações de regras, mantendo a trilha de auditoria completa.

---

## 3. Arquitetura do Sistema

A arquitetura do projeto foi estruturada em camadas bem definidas, promovendo alta coesão, baixo acoplamento e conformidade com padrões de Engenharia de Software:

```
┌─────────────────────────────────────────────────────────────┐
│                 Camada de Exposição (REST API)              │
│       FastAPI (Endpoints: /listings, /blockchain, /import)  │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│           Camada de Lógica de Negócio e Criptografia        │
│    - SmartContract (Validação determinística de regras)     │
│    - Block / Hashing Engine (SHA-256 via hashlib)           │
│    - Importer Service (Parsing sanitizado de CSV & SSE)     │
└──────────────────────────────┬──────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────┐
│                  Camada de Persistência                     │
│    - SQLAlchemy 2.0 (ORM)                                   │
│    - PostgreSQL 16 (Tabelas: listings, blockchain_records)   │
│    - Docker / Docker Compose (Isolamento de Infraestrutura) │
└─────────────────────────────────────────────────────────────┘
```

### 3.1. Modelo de Dados

O banco relacional modela duas entidades complementares:

1. **`Listing` (Tabela `listings`):** Representa o estado atual dos imóveis no sistema (cidade, bairro, tipo de negócio, preço, área útil, quartos, etc.).
2. **`BlockchainRecord` (Tabela `blockchain_records`):** Representa a linha do tempo imutável dos eventos ocorridos, contendo:
   - `block_index`: Índice cardinal do bloco.
   - `listing_id`: Identificador do imóvel alvo da ação.
   - `action`: Operação executada (`REGISTER`, `UPDATE` ou `DEACTIVATE`).
   - `block_hash`: Resumo criptográfico SHA-256 do bloco.
   - `previous_hash`: Resumo criptográfico do bloco antecedente.
   - `block_data`: Conteúdo serializado em JSON com o estado completo do registro no instante da inclusão.
   - `contract_valid` e `contract_message`: Resultado da avaliação do contrato inteligente.
   - `timestamp`: Carimbo temporal em formato ISO 8601 com fuso horário UTC.

---

## 4. Implementação Técnica

### 4.1. Estruturação e Hashing do Bloco

A classe `Block` em `app/blockchain.py` implementa a composição dos metadados e o cálculo rigoroso do *hash*. Para assegurar determinismo durante a serialização em JSON, as chaves do dicionário são ordenadas alfabeticamente (`sort_keys=True`):

```python
import hashlib
import json
from datetime import datetime, timezone

class Block:
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
```

O primeiro bloco da cadeia é instanciado como **Bloco Gênesis** (`Genesis Block`), possuindo índice `0` e `previous_hash` formado por 64 caracteres de zeros hexadecimais:

```python
def create_genesis_block() -> Block:
    return Block(
        index=0,
        data={"message": "Genesis Block - Blockchain Imobiliária"},
        previous_hash="0" * 64,
    )
```

### 4.2. Implementação do Smart Contract

Antes da aceitação de qualquer registro na cadeia de custódia, o `SmartContract` executa uma rotina de verificação estática que atesta a sanidade dos dados financeiros e cadastrais:

```python
class SmartContract:
    @staticmethod
    def validate_listing(data: dict) -> tuple[bool, str]:
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
        if (data.get("usable_area", 0) or 0) <= 0:
            return False, "Área útil deve ser maior que zero."

        return True, "Contrato validado com sucesso."

    @staticmethod
    def validate_transaction(listing_id: int, action: str) -> tuple[bool, str]:
        allowed_actions = {"REGISTER", "UPDATE", "DEACTIVATE"}
        if action not in allowed_actions:
            return False, f"Ação '{action}' não permitida. Use: {allowed_actions}"
        return True, f"Transação '{action}' autorizada para imóvel #{listing_id}."
```

### 4.3. Algoritmo de Validação de Integridade da Cadeia

Para auditar se os registros armazenados no banco de dados sofreram qualquer alteração não autorizada diretamente no SGBD, o endpoint `GET /blockchain/validate` executa uma rotina iterativa de verificação:

$$\forall i \in \{1, \dots, N\}, \quad \text{PreviousHash}(B_i) \stackrel{?}{=} \text{Hash}(B_{i-1})$$

Caso haja divergência em qualquer índice $i$, a cadeia é categorizada como violada, e a listagem dos blocos corrompidos é imediatamente sinalizada.

---

## 5. Análise de Resultados e Aplicações Acadêmicas

A arquitetura desenvolvida apresenta vantagens claras quando contrastada com sistemas imobiliários convencionais:

| Critério de Análise | Sistema Centralizado Tradicional | Sistema Proposto com Blockchain |
|---|---|---|
| **Rastreabilidade de Preços** | Histórico sobregravado ou volátil | Histórico perene imutável em blocos |
| **Integridade de Registros** | Vulnerável a manipulações diretas no banco | Detectável por recálculo de *hash* SHA-256 |
| **Validação de Regras** | Dispersa no frontend/backend | Centralizada e auditável via *Smart Contract* |
| **Auditoria Externa** | Complexa, requer logs de banco | Simples, acessível via rota `/blockchain/validate` |

### Relevância para Ensino e Pesquisa
Para os estudantes universitários, o projeto serve como um laboratório prático para consolidar tópicos essenciais de:
- **Criptografia Aplicada:** Compreensão prática de funções de espalhamento unidirecional (*hashing*) e concatenação de estados.
- **Sistemas Distribuídos e DLT:** Transição de arquiteturas centralizadas clássicas para modelos baseados em registros imutáveis.
- **Engenharia de Software e APIs Modernas:** Utilização de digitação estática em `Python`, validação de *payloads* via `Pydantic`, arquitetura assíncrona com `FastAPI` e orquestração de microsserviços com `Docker Compose`.

---

## 6. Conclusão

A integração entre tecnologias de *Blockchain*, *Smart Contracts* e sistemas web convencionais viabiliza a criação de plataformas imobiliárias significativamente mais transparentes e seguras. O sistema construído comprova que os princípios fundamentais que regem as redes descentralizadas podem ser aplicados com eficácia no nível de aplicação para garantir a inviolabilidade dos dados cadastrais e a rastreabilidade temporal das transações.

Como trabalhos futuros e tópicos de pesquisa para projetos de graduação e pós-graduação, sugere-se a expansão desta arquitetura com:
1. **Mecanismos de Consenso Distribuído:** Implementação de consenso entre múltiplos nós executando instâncias independentes (como *Raft* ou *PBFT*).
2. **Assinaturas Digitais Assimétricas:** Inclusão de criptografia de chave pública (algoritmos `ECDSA` ou `Ed25519`) para autenticar a assinatura digital de proprietários e corretores em cada bloco.
3. **Oráculos e Tokenização:** Integração com contratos inteligentes em redes públicas (como Ethereum/Polygon) para emissão de tokens não-fungíveis (NFTs) representando títulos de posse digital e integração com oráculos de dados cartorários.

---

## 7. Referências Bibliográficas

- ANTONOPOULOS, Andreas M. **Mastering Bitcoin: Programming the Open Blockchain**. 2. ed. Sebastopol: O'Reilly Media, 2017.
- BUTERIN, Vitalik. **Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform**. White Paper, 2014. Disponível em: <https://ethereum.org/en/whitepaper/>.
- FOROUZAN, Behrouz A.; MUKHOPADHYAY, Debdeep. **Cryptography and Network Security**. 3. ed. Nova York: McGraw-Hill Education, 2015.
- NAKAMOTO, Satoshi. **Bitcoin: A Peer-to-Peer Electronic Cash System**. 2008. Disponível em: <https://bitcoin.org/bitcoin.pdf>.
- NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY (NIST). **FIPS PUB 180-4: Secure Hash Standard (SHS)**. Gaithersburg: U.S. Department of Commerce, 2015.
- RAMÍREZ, Sebastián. **FastAPI: Modern, Fast (High-Performance) Web Framework for Building APIs with Python**. Documentação Oficial, 2024. Disponível em: <https://fastapi.tiangolo.com/>.
- SZABO, Nick. **Formalizing and Securing Relationships on Public Networks**. First Monday, v. 2, n. 9, 1997. DOI: 10.5210/fm.v2i9.548.
- TAPSCOTT, Don; TAPSCOTT, Alex. **Blockchain Revolution: How the Technology Behind Bitcoin and Other Cryptocurrencies is Changing the World**. Nova York: Portfolio/Penguin, 2016.
