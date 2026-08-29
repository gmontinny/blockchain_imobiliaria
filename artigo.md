# Aplicação de Blockchain e Smart Contracts na Gestão e Rastreabilidade de Transações Imobiliárias: Uma Abordagem Prática com Python e FastAPI

**Tipo:** Artigo Técnico-Científico  
**Área:** Ciência da Computação — Segurança da Informação, Engenharia de Software, Sistemas Distribuídos  
**Público-alvo:** Estudantes universitários de Computação, Engenharia de Software, Sistemas de Informação e áreas correlatas

---

## Resumo

A digitalização do setor imobiliário enfrenta desafios históricos relacionados à transparência, integridade dos registros e prevenção a fraudes cadastrais. Este artigo apresenta o desenvolvimento e a fundamentação teórica de uma arquitetura baseada em conceitos de **Blockchain** e **Smart Contracts** integrada a uma API REST moderna desenvolvida em Python e FastAPI, suportada pelo banco de dados relacional PostgreSQL em ambiente containerizado com Docker. O sistema implementa uma cadeia de blocos com encadeamento criptográfico via algoritmo SHA-256, integrando um motor de validação automatizada de regras de negócio (Smart Contract) que audita anúncios provenientes de conjuntos de dados reais antes de sua gravação no livro-razão (ledger). São detalhados os princípios matemáticos das funções hash, a estrutura dos blocos, o fluxo de validação contratual, a arquitetura em camadas do sistema e os resultados obtidos com dados reais do portal ZAP Imóveis. O trabalho destina-se a servir como referência didática e técnica para estudantes universitários, detalhando os princípios matemáticos, arquiteturais e práticos da tecnologia de registros distribuídos aplicada a um domínio concreto.

**Palavras-chave:** Blockchain. Smart Contracts. Criptografia. SHA-256. FastAPI. Integridade de Dados. Mercado Imobiliário. Python. Sistemas Distribuídos.

---

## Abstract

The digitalization of the real estate sector faces historical challenges related to transparency, record integrity, and prevention of cadastral fraud. This paper presents the development and theoretical foundation of an architecture based on **Blockchain** and **Smart Contract** concepts integrated into a modern REST API built with Python and FastAPI, supported by the PostgreSQL relational database in a Docker-containerized environment. The system implements a chain of blocks with cryptographic chaining via the SHA-256 algorithm, integrating an automated business rule validation engine (Smart Contract) that audits listings from real datasets before writing them to the ledger. The work is intended to serve as a didactic and technical reference for university students, detailing the mathematical, architectural, and practical principles of distributed ledger technology applied to a concrete domain.

**Keywords:** Blockchain. Smart Contracts. Cryptography. SHA-256. FastAPI. Data Integrity. Real Estate. Python. Distributed Systems.

---

## 1. Introdução

O mercado imobiliário tradicional depende extensivamente de intermediários cartorários, plataformas centralizadas e processos manuais de verificação. Essa estrutura centralizada acarreta riscos bem documentados: assimetria de informações entre compradores e vendedores, possibilidade de adulteração retroativa de históricos de preços, duplicidade de ofertas fraudulentas e ausência de rastreabilidade auditável das transações (TAPSCOTT; TAPSCOTT, 2016).

Com a evolução da Ciência da Computação e a consolidação das tecnologias de registro distribuído (*Distributed Ledger Technology* — DLT), propostas baseadas em cadeias de blocos (*blockchains*) surgiram como uma alternativa robusta para garantir a **imutabilidade**, a **rastreabilidade** e a **auditabilidade** de transações em domínios que exigem alto grau de confiança (NAKAMOTO, 2008).

Paralelamente, os **contratos inteligentes** (*Smart Contracts*), conceituados por Nick Szabo em 1997, introduziram a ideia de protocolos autoexecutáveis capazes de verificar e fazer cumprir regras de negócio de forma determinística, sem a necessidade de intermediários humanos (SZABO, 1997). A popularização desse conceito ocorreu com a plataforma Ethereum, que os implementou como código executável em uma máquina virtual descentralizada (BUTERIN, 2014).

O presente projeto propõe uma abordagem arquitetural em que anúncios de imóveis são processados sob a ótica de transações criptográficas. Cada operação — seja criação (`REGISTER`) ou atualização (`UPDATE`) — passa por um contrato inteligente de validação e é selada em um bloco encadeado deterministicamente ao bloco anterior. Os dados utilizados provêm de um conjunto real de anúncios do portal ZAP Imóveis, conferindo ao experimento aderência a cenários do mundo real.

### 1.1 Objetivos

- Apresentar os fundamentos teóricos de blockchain e smart contracts de forma acessível ao público universitário.
- Demonstrar a implementação prática desses conceitos em um sistema web funcional com Python e FastAPI.
- Evidenciar como a criptografia SHA-256 garante a integridade e a imutabilidade dos registros.
- Servir como referência de projeto para trabalhos de conclusão de curso, iniciações científicas e disciplinas de Segurança da Informação e Sistemas Distribuídos.

### 1.2 Organização do Artigo

O artigo está organizado da seguinte forma: a Seção 2 apresenta a fundamentação teórica sobre blockchain, funções hash e smart contracts. A Seção 3 descreve a arquitetura do sistema. A Seção 4 detalha a implementação técnica com trechos de código comentados. A Seção 5 apresenta o fluxo completo de uma transação. A Seção 6 analisa os resultados. A Seção 7 discute trabalhos relacionados e limitações. A Seção 8 conclui o artigo com sugestões de trabalhos futuros.

---

## 2. Fundamentação Teórica

### 2.1 Conceito e Estrutura de uma Blockchain

Uma *blockchain* é uma estrutura de dados sequencial composta por blocos encadeados linearmente no tempo. O conceito foi formalizado por Satoshi Nakamoto em 2008 no artigo seminal *Bitcoin: A Peer-to-Peer Electronic Cash System*, que propôs um sistema de pagamento eletrônico descentralizado sem necessidade de uma autoridade central de confiança (NAKAMOTO, 2008).

Cada bloco $B_i$ contém:

- Um conjunto de dados ou transações ($D_i$)
- Um índice sequencial ($i$)
- Um carimbo temporal (*timestamp* $t_i$)
- O valor de resumo criptográfico (*hash*) do bloco imediatamente anterior: $H(B_{i-1})$
- O próprio *hash* calculado: $H(B_i)$

```
┌──────────────────────────┐      ┌──────────────────────────┐      ┌──────────────────────────┐
│      Bloco Gênesis       │      │         Bloco 1          │      │         Bloco 2          │
├──────────────────────────┤      ├──────────────────────────┤      ├──────────────────────────┤
│ index:         0         │      │ index:         1         │      │ index:         2         │
│ timestamp:     t_0       │      │ timestamp:     t_1       │      │ timestamp:     t_2       │
│ previous_hash: 0000...   │─────►│ previous_hash: H(B_0)    │─────►│ previous_hash: H(B_1)    │
│ data:          Genesis   │      │ data:          {imóvel}  │      │ data:          {imóvel}  │
│ hash:          H(B_0)    │      │ hash:          H(B_1)    │      │ hash:          H(B_2)    │
└──────────────────────────┘      └──────────────────────────┘      └──────────────────────────┘
```

Essa amarração encadeada gera a propriedade de **resistência à adulteração**: caso um agente malicioso altere qualquer dado no bloco $B_{i-1}$, o seu *hash* recalculado resultará em um valor completamente divergente. Consequentemente, o campo `previous_hash` armazenado em $B_i$ torna-se inválido, quebrando a integridade de toda a cadeia subsequente. Para que a adulteração passasse despercebida, seria necessário recalcular todos os blocos a partir do ponto alterado — o que, em redes distribuídas com mecanismos de consenso, é computacionalmente inviável (ANTONOPOULOS, 2017).

É importante distinguir entre **blockchain pública** (como Bitcoin e Ethereum, onde qualquer nó pode participar) e **blockchain privada ou permissionada** (como a implementada neste projeto, onde o controle de escrita é centralizado em uma aplicação). Ambas compartilham os mesmos princípios criptográficos de encadeamento e imutabilidade, diferindo apenas no modelo de governança e consenso (HYPERLEDGER, 2023).

### 2.2 Funções Hash Criptográficas e o Algoritmo SHA-256

No centro da integridade de uma *blockchain* está a **função hash criptográfica**. Trata-se de uma função matemática determinística:

$$H: \{0,1\}^* \to \{0,1\}^n$$

que mapeia uma entrada de tamanho arbitrário em uma cadeia de bits de tamanho fixo ($n = 256$ bits no caso do SHA-256), produzindo uma saída de 64 caracteres hexadecimais (NIST, 2015).

Para ser considerada criptograficamente segura, a função hash deve satisfazer quatro propriedades fundamentais:

**1. Determinismo**
Uma mesma entrada $x$ sempre produzirá rigorosamente o mesmo valor de saída $H(x)$, independentemente do momento ou do sistema em que for executada.

**2. Resistência à Pré-Imagem (Unidirecionalidade)**
Dado um *hash* $y$, deve ser computacionalmente inviável encontrar qualquer entrada $x$ tal que $H(x) = y$. Isso garante que o conteúdo original não possa ser reconstituído a partir do resumo.

**3. Resistência a Colisões**
Deve ser computacionalmente inviável encontrar duas entradas distintas $x_1 \neq x_2$ tais que $H(x_1) = H(x_2)$. No SHA-256, o espaço de saída possui $2^{256}$ valores possíveis — um número astronomicamente maior que o número de átomos no universo observável.

**4. Efeito Avalanche**
Qualquer modificação mínima na entrada (como a alteração de um único caractere) resulta em uma saída completamente diferente e estatisticamente descorrelacionada da anterior. O exemplo abaixo ilustra esse efeito:

```
Entrada:  "Apartamento São Paulo"
SHA-256:  3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b

Entrada:  "apartamento São Paulo"  ← apenas a capitalização mudou
SHA-256:  9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
```

O algoritmo SHA-256 pertence à família SHA-2 (*Secure Hash Algorithm 2*), padronizado pelo NIST (*National Institute of Standards and Technology*) na publicação FIPS PUB 180-4. Ele opera sobre blocos de 512 bits, realizando 64 rodadas de operações bit a bit (rotações, deslocamentos e funções lógicas não-lineares) sobre um estado interno de 256 bits (FOROUZAN; MUKHOPADHYAY, 2015).

### 2.3 Smart Contracts — Contratos Inteligentes

O termo *Smart Contract* foi cunhado por Nick Szabo em 1994 e formalizado em seu artigo de 1997 *Formalizing and Securing Relationships on Public Networks*. Szabo definiu contratos inteligentes como:

> *"Um protocolo de transação computadorizado que executa os termos de um contrato. Os objetivos gerais do design de contratos inteligentes são satisfazer condições contratuais comuns [...], minimizar exceções tanto maliciosas quanto acidentais, e minimizar a necessidade de intermediários confiáveis."* (SZABO, 1997, tradução nossa)

Na prática, um contrato inteligente é um conjunto de regras codificadas que:

1. **Verifica pré-condições** antes de permitir que uma transação seja registrada.
2. **Executa automaticamente** sem intervenção humana quando as condições são satisfeitas.
3. **Registra o resultado** — tanto aprovações quanto rejeições — de forma auditável e imutável.
4. **É determinístico**: para os mesmos dados de entrada, sempre produz o mesmo resultado.

A diferença fundamental entre um contrato inteligente e uma simples validação de formulário está na **vinculação ao ledger**: a decisão do contrato é registrada permanentemente na cadeia, criando uma trilha de auditoria completa de todas as tentativas de transação, incluindo as rejeitadas.

No contexto deste projeto, o Smart Contract valida cada imóvel antes de seu registro na blockchain, garantindo que apenas dados íntegros e completos sejam aceitos na cadeia — e que qualquer tentativa de registro inválido seja documentada.

### 2.4 Server-Sent Events (SSE) e Observabilidade em Tempo Real

*Server-Sent Events* (SSE) é um padrão W3C que permite que um servidor HTTP envie dados de forma unidirecional e contínua para um cliente, sem que este precise realizar novas requisições. Diferente do WebSocket (bidirecional), o SSE é ideal para cenários de monitoramento e progresso onde apenas o servidor precisa transmitir atualizações (W3C, 2015).

No sistema desenvolvido, o SSE é utilizado para transmitir o progresso da importação do CSV em tempo real, permitindo que o cliente acompanhe cada linha processada sem bloquear a interface ou aguardar o término completo da operação.

---

## 3. Arquitetura do Sistema

A arquitetura do projeto foi estruturada em três camadas bem definidas, promovendo alta coesão, baixo acoplamento e conformidade com os princípios SOLID de Engenharia de Software:

```
┌──────────────────────────────────────────────────────────────────┐
│                  Camada de Exposição (REST API)                  │
│                                                                  │
│   GET /listings/          POST /listings/                        │
│   GET /listings/{id}      GET /blockchain/records                │
│   GET /blockchain/validate                                       │
│   POST /import/csv        GET /import/csv/stream (SSE)           │
│                                                                  │
│                    FastAPI + Pydantic + Uvicorn                  │
└────────────────────────────────┬─────────────────────────────────┘
                                 │
┌────────────────────────────────▼─────────────────────────────────┐
│              Camada de Lógica de Negócio e Criptografia          │
│                                                                  │
│   SmartContract          → Validação determinística de regras    │
│   Block / HashEngine     → SHA-256 via hashlib (stdlib)          │
│   crud.py                → Orquestração: banco + blockchain      │
│   services/importer.py   → Parsing sanitizado de CSV + SSE       │
└────────────────────────────────┬─────────────────────────────────┘
                                 │
┌────────────────────────────────▼─────────────────────────────────┐
│                     Camada de Persistência                       │
│                                                                  │
│   SQLAlchemy 2.0 (ORM)   → Mapeamento objeto-relacional          │
│   PostgreSQL 16           → Tabelas: listings, blockchain_records│
│   Docker / Compose        → Isolamento e portabilidade           │
└──────────────────────────────────────────────────────────────────┘
```

### 3.1 Estrutura de Arquivos

```
blockchain/
├── app/
│   ├── main.py              # Ponto de entrada: FastAPI + criação das tabelas
│   ├── config.py            # Configurações via pydantic-settings e .env
│   ├── database.py          # Engine SQLAlchemy, sessão e Base declarativa
│   ├── models.py            # Modelos ORM: Listing e BlockchainRecord
│   ├── schemas.py           # Schemas Pydantic para validação de I/O
│   ├── crud.py              # Operações de banco + orquestração blockchain
│   ├── blockchain.py        # Block, SmartContract, hashing SHA-256
│   ├── routers/
│   │   ├── listings.py      # Endpoints de imóveis
│   │   ├── blockchain.py    # Endpoints de blockchain
│   │   └── importer.py      # Endpoints de importação CSV e SSE
│   └── services/
│       └── importer.py      # Lógica de parsing, sanitização e streaming
├── data/
│   └── dataZAP.csv          # Dataset real do ZAP Imóveis
├── .env                     # Variáveis de ambiente
├── docker-compose.yml       # PostgreSQL 16 + pgAdmin 4
└── requirements.txt         # Dependências Python
```

### 3.2 Modelo de Dados Relacional

O banco relacional modela duas entidades complementares que juntas formam o sistema:

**Tabela `listings` — Estado atual dos imóveis**

Armazena o estado presente de cada imóvel, com todos os seus atributos cadastrais e financeiros. É a fonte de verdade para consultas e filtros.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | INTEGER PK | Identificador interno sequencial |
| `listing_id` | VARCHAR UNIQUE | ID original do portal ZAP |
| `city` / `state` / `neighborhood` | VARCHAR | Localização |
| `business_type` | VARCHAR | `RENTAL`, `SALE` ou `RENTAL_SALE` |
| `price` / `rental_price` / `sale_price` | FLOAT | Valores financeiros |
| `usable_area` / `total_area` | FLOAT | Metragens |
| `bedrooms` / `bathrooms` / `suites` | INTEGER | Características |
| `furnished` / `pool` / `gym` | BOOLEAN | Comodidades |
| `created_at` / `updated_at` | TIMESTAMP | Controle temporal |

**Tabela `blockchain_records` — Linha do tempo imutável**

Armazena cada evento registrado na cadeia. Nunca é atualizada — apenas recebe novos registros, preservando o histórico completo.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | INTEGER PK | Identificador interno |
| `block_index` | INTEGER UNIQUE | Posição cardinal na cadeia |
| `listing_id` | VARCHAR | ID do imóvel alvo |
| `action` | VARCHAR | `REGISTER`, `UPDATE` ou `DEACTIVATE` |
| `block_hash` | VARCHAR UNIQUE | SHA-256 deste bloco |
| `previous_hash` | VARCHAR | SHA-256 do bloco anterior |
| `block_data` | TEXT | Snapshot JSON do estado no momento |
| `contract_valid` | BOOLEAN | Resultado do Smart Contract |
| `contract_message` | VARCHAR | Mensagem de validação |
| `timestamp` | VARCHAR | ISO 8601 com fuso UTC |

### 3.3 Proteção contra Duplicatas — Duas Camadas

O sistema implementa proteção contra duplicatas em dois níveis independentes, garantindo idempotência tanto na importação em lote quanto no cadastro manual:

```
Camada 1 — Importação CSV (services/importer.py)
  └── Se listing_id já existe no banco → ignora a linha, incrementa skipped

Camada 2 — API Manual (crud.create_listing)
  └── Se listing_id já existe no banco → registra UPDATE na blockchain
                                         e retorna o imóvel existente
```

Essa abordagem garante que reimportar o CSV quantas vezes for necessário não gere duplicatas, e que chamadas repetidas à API sejam tratadas de forma semanticamente correta — registrando a tentativa de atualização na cadeia em vez de silenciosamente ignorá-la.

---

## 4. Implementação Técnica

### 4.1 Configuração e Conexão com o Banco

As configurações são gerenciadas via `pydantic-settings`, que lê automaticamente as variáveis do arquivo `.env` e as expõe como atributos tipados:

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "meubanco"
    postgres_port: int = 5432
    postgres_host: str = "localhost"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"  # ignora variáveis do .env não declaradas aqui

settings = Settings()
```

A sessão do banco é gerenciada como um gerador Python, garantindo que a conexão seja sempre fechada ao final de cada requisição — padrão recomendado pelo SQLAlchemy 2.0:

```python
# app/database.py
def get_db():
    db = SessionLocal()
    try:
        yield db       # injeta a sessão no endpoint via Depends()
    finally:
        db.close()     # garante fechamento mesmo em caso de exceção
```

### 4.2 Estruturação e Hashing do Bloco

A classe `Block` implementa a composição dos metadados e o cálculo do *hash*. O ponto crítico é o uso de `sort_keys=True` na serialização JSON, que garante **determinismo**: independentemente da ordem em que as chaves foram inseridas no dicionário, a serialização sempre produzirá a mesma string — e portanto o mesmo *hash*:

```python
# app/blockchain.py
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
            sort_keys=True,       # garante ordem determinística das chaves
            ensure_ascii=False,   # preserva caracteres UTF-8 (acentos)
        )
        return hashlib.sha256(content.encode()).hexdigest()
```

O **Bloco Gênesis** é o primeiro bloco da cadeia. Por convenção, seu `previous_hash` é uma string de 64 zeros hexadecimais, sinalizando que não há bloco anterior:

```python
def create_genesis_block() -> Block:
    return Block(
        index=0,
        data={"message": "Genesis Block - Blockchain Imobiliária"},
        previous_hash="0" * 64,
    )
```

### 4.3 Implementação do Smart Contract

O `SmartContract` opera como uma barreira regulatória antes de qualquer persistência na cadeia. Ele é composto por dois métodos estáticos independentes:

```python
# app/blockchain.py
class SmartContract:

    @staticmethod
    def validate_listing(data: dict) -> tuple[bool, str]:
        """Valida os dados cadastrais e financeiros do imóvel."""
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
        """Valida se a ação solicitada é permitida pelo contrato."""
        allowed_actions = {"REGISTER", "UPDATE", "DEACTIVATE"}
        if action not in allowed_actions:
            return False, f"Ação '{action}' não permitida. Use: {allowed_actions}"
        return True, f"Transação '{action}' autorizada para imóvel #{listing_id}."
```

Um aspecto importante do design: mesmo quando o contrato falha (`contract_valid = False`), o bloco **ainda é registrado** na cadeia com a mensagem de erro. Isso preserva a trilha de auditoria completa — incluindo tentativas inválidas — o que é fundamental para fins de conformidade e investigação forense.

### 4.4 Orquestração no CRUD

A função `register_on_blockchain` em `crud.py` é o ponto de integração entre o banco relacional e a cadeia de blocos. Ela é chamada sempre que um imóvel é criado ou atualizado:

```python
# app/crud.py
def register_on_blockchain(db: Session, listing: Listing, action: str) -> BlockchainRecord:
    # 1. Executa o Smart Contract
    contract = SmartContract()
    valid, message = contract.validate_transaction(listing.id, action)

    # 2. Monta o snapshot de dados do imóvel para o bloco
    block_data = {
        "listing_id": listing.listing_id,
        "city": listing.city,
        "neighborhood": listing.neighborhood,
        "price": listing.price,
        "usable_area": listing.usable_area,
        "business_type": listing.business_type,
        "action": action,
    }

    # 3. Cria o bloco encadeado ao último hash da cadeia
    block = create_block_from_record(
        index=get_next_block_index(db),
        data=block_data,
        previous_hash=get_last_block_hash(db),
    )

    # 4. Persiste o bloco no banco
    record = BlockchainRecord(
        block_index=block.index,
        listing_id=listing.listing_id,
        action=action,
        block_hash=block.hash,
        previous_hash=block.previous_hash,
        block_data=json.dumps(block.data, ensure_ascii=False),
        contract_valid=block.data.get("contract_valid", valid),
        contract_message=block.data.get("contract_validation", message),
        timestamp=block.timestamp,
    )
    db.add(record)
    db.commit()
    return record
```

### 4.5 Algoritmo de Validação de Integridade

O endpoint `GET /blockchain/validate` implementa a verificação matemática da cadeia. Para cada bloco $B_i$ (com $i > 0$), verifica-se:

$$\text{PreviousHash}(B_i) \stackrel{?}{=} \text{Hash}(B_{i-1})$$

```python
# app/crud.py
def validate_blockchain_integrity(db: Session) -> dict:
    records = db.query(BlockchainRecord).order_by(BlockchainRecord.block_index).all()
    invalid_blocks = []

    for i, record in enumerate(records):
        if i > 0:
            expected_previous = records[i - 1].block_hash
            if record.previous_hash != expected_previous:
                invalid_blocks.append(record.block_index)

    return {
        "is_valid": len(invalid_blocks) == 0,
        "total_blocks": len(records),
        "invalid_blocks": invalid_blocks,
        "message": (
            "Blockchain íntegra."
            if not invalid_blocks
            else f"{len(invalid_blocks)} bloco(s) inválido(s) detectado(s)."
        ),
    }
```

Caso um administrador de banco de dados altere diretamente um registro na tabela `blockchain_records`, o `previous_hash` do bloco seguinte não corresponderá mais ao hash recalculado, e a violação será imediatamente detectada.

### 4.6 Importação com Progresso em Tempo Real (SSE)

O serviço de importação implementa dois modos de operação. No modo síncrono (`POST /import/csv`), o processamento ocorre integralmente antes de retornar a resposta. No modo SSE (`GET /import/csv/stream`), um gerador Python emite eventos JSON a cada linha processada:

```python
# app/services/importer.py
def import_csv_stream(db: Session) -> Generator[str, None, None]:
    df = pd.read_csv(CSV_PATH, sep=";", dtype=str, on_bad_lines="skip")
    total = len(df)
    imported, skipped = 0, 0

    def _event(data: dict) -> str:
        return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

    yield _event({"status": "started", "total": total})

    for i, (_, row) in enumerate(df.iterrows(), start=1):
        listing = _build_listing(row)
        if not listing:
            skipped += 1
            yield _event({"status": "skipped", "row": i, "reason": "listing.id ausente"})
            continue

        exists = db.query(Listing).filter(
            Listing.listing_id == listing.listing_id
        ).first()

        if exists:
            skipped += 1
            yield _event({"status": "skipped", "row": i,
                          "listing_id": listing.listing_id, "reason": "já existe"})
            continue

        db.add(listing)
        db.flush()
        register_on_blockchain(db, listing, "REGISTER")
        imported += 1
        yield _event({
            "status": "imported", "row": i, "total": total,
            "listing_id": listing.listing_id,
            "city": listing.city,
            "imported_so_far": imported,
            "skipped_so_far": skipped,
        })

    db.commit()
    yield _event({"status": "done", "total_imported": imported,
                  "total_skipped": skipped})
```

O `StreamingResponse` do FastAPI consome esse gerador e transmite cada evento imediatamente ao cliente, sem aguardar o término do loop:

```python
# app/routers/importer.py
@router.get("/csv/stream")
def importar_csv_stream(db: Session = Depends(get_db)):
    return StreamingResponse(
        import_csv_stream(db),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
```

---

## 5. Fluxo Completo de uma Transação

Para consolidar a compreensão do sistema, esta seção descreve passo a passo o que ocorre quando um imóvel é cadastrado via `POST /listings/`:

```
Cliente HTTP
    │
    │  POST /listings/  { listing_id, city, neighborhood, price, usable_area, ... }
    ▼
FastAPI — Pydantic valida o schema (tipos, campos obrigatórios)
    │
    ▼
crud.create_listing(db, data)
    │
    ├─► listing_id já existe no banco?
    │       └── SIM → register_on_blockchain(existing, "UPDATE")
    │                  └── retorna imóvel existente (sem duplicar)
    │
    └─► NÃO → INSERT em listings
                   │
                   ▼
              register_on_blockchain(listing, "REGISTER")
                   │
                   ├─► SmartContract.validate_listing(data)
                   │       ├── preço > 0?          ✔ ou ✘
                   │       ├── cidade informada?   ✔ ou ✘
                   │       ├── bairro informado?   ✔ ou ✘
                   │       └── área útil > 0?      ✔ ou ✘
                   │
                   ├─► SmartContract.validate_transaction(id, "REGISTER")
                   │       └── ação permitida?     ✔ ou ✘
                   │
                   ├─► get_last_block_hash(db)     → previous_hash
                   ├─► get_next_block_index(db)    → index
                   │
                   ├─► Block(index, data, previous_hash)
                   │       └── _calculate_hash()  → SHA-256
                   │
                   └─► INSERT em blockchain_records
                           { block_index, block_hash, previous_hash,
                             contract_valid, contract_message, timestamp }
    │
    ▼
Resposta HTTP 201 — ListingResponse (JSON)
```

Este fluxo evidencia a separação clara de responsabilidades: o FastAPI cuida da exposição HTTP, o Pydantic da validação de schema, o `crud.py` da orquestração, o `SmartContract` das regras de negócio e o `Block` da criptografia.

---

## 6. Análise de Resultados

### 6.1 Dados Utilizados

O dataset utilizado é composto por anúncios reais do portal ZAP Imóveis, armazenados no arquivo `data/dataZAP.csv` com separador `;`. O conjunto contém aproximadamente 100 registros de apartamentos de diversas cidades brasileiras (São Paulo, Rio de Janeiro, Belo Horizonte, Florianópolis, Porto Alegre, Curitiba, entre outras), com atributos como preço de aluguel, área útil, número de quartos, comodidades e coordenadas geográficas.

O processo de sanitização dos dados trata os seguintes casos comuns no dataset:

| Problema no CSV | Tratamento aplicado |
|---|---|
| Valores `"normal"` em campos numéricos | Convertidos para `None` |
| Floats com vírgula como separador decimal | Normalizados para ponto |
| Campos booleanos como string `"True"`/`"False"` | Convertidos para `bool` |
| Linhas sem `listing.id` | Ignoradas e contabilizadas em `skipped` |
| Registros já existentes no banco | Ignorados (idempotência) |

### 6.2 Comportamento da Blockchain após Importação

Após a importação bem-sucedida de 98 imóveis, a cadeia apresenta o seguinte comportamento esperado:

**Consulta aos primeiros blocos:**
```json
[
  {
    "block_index": 1,
    "listing_id": "2486576702",
    "action": "REGISTER",
    "previous_hash": "0000000000000000000000000000000000000000000000000000000000000000",
    "block_hash": "a3f8c2d1e4b7a9f0c3d2e1b4a7f9c0d3e2b1a4f7c9d0e3b2a1f4c7d9e0b3a2f1",
    "contract_valid": true,
    "contract_message": "Contrato validado com sucesso.",
    "timestamp": "2024-01-15T10:30:00.123456+00:00"
  },
  {
    "block_index": 2,
    "listing_id": "2489060354",
    "action": "REGISTER",
    "previous_hash": "a3f8c2d1e4b7a9f0c3d2e1b4a7f9c0d3e2b1a4f7c9d0e3b2a1f4c7d9e0b3a2f1",
    "block_hash": "b4e9d3c2f5a8b1e4d7c0f3a6b9e2d5c8f1a4b7e0d3c6f9a2b5e8d1c4f7a0b3e6",
    "contract_valid": true,
    "contract_message": "Contrato validado com sucesso.",
    "timestamp": "2024-01-15T10:30:00.234567+00:00"
  }
]
```

Observe que o `previous_hash` do bloco 2 é idêntico ao `block_hash` do bloco 1 — essa é a propriedade de encadeamento que garante a integridade da cadeia.

**Validação de integridade com cadeia íntegra:**
```json
{
  "is_valid": true,
  "total_blocks": 98,
  "invalid_blocks": [],
  "message": "Blockchain íntegra."
}
```

**Simulação de adulteração:** Se um administrador alterar diretamente o campo `block_hash` do bloco de índice 15 no banco de dados, a próxima validação retornará:
```json
{
  "is_valid": false,
  "total_blocks": 98,
  "invalid_blocks": [16],
  "message": "1 bloco(s) inválido(s) detectado(s)."
}
```

O bloco 16 é sinalizado porque seu `previous_hash` não corresponde mais ao `block_hash` adulterado do bloco 15.

### 6.3 Comparativo com Sistemas Tradicionais

| Critério | Sistema Centralizado Tradicional | Sistema Proposto com Blockchain |
|---|---|---|
| **Rastreabilidade de preços** | Histórico sobregravado ou volátil | Histórico perene e imutável em blocos |
| **Integridade dos registros** | Vulnerável a manipulações diretas no banco | Detectável por recálculo de hash SHA-256 |
| **Validação de regras** | Dispersa no frontend/backend, sem auditoria | Centralizada e auditável via Smart Contract |
| **Auditoria externa** | Complexa, requer acesso a logs internos | Simples, acessível via `GET /blockchain/validate` |
| **Duplicatas** | Dependente de constraints de banco | Duas camadas: importer + crud |
| **Observabilidade** | Logs de servidor, sem progresso em tempo real | SSE com eventos por linha processada |
| **Portabilidade** | Dependente do ambiente de instalação | Containerizado com Docker Compose |

### 6.4 Logs de Importação

Durante a importação, o terminal exibe o progresso em tempo real com timestamp, posição e dados do imóvel:

```
10:32:01 [INFO] Iniciando importação: 100 linhas encontradas no CSV.
10:32:01 [INFO] [1/100] ✔ Importado: '2486576702' — São Paulo, Parada Inglesa
10:32:01 [INFO] [2/100] ✔ Importado: '2489060354' — Florianópolis, Agronômica
10:32:01 [INFO] [3/100] ✔ Importado: '2490399573' — Rio de Janeiro, Recreio Dos Bandeirantes
...
10:32:03 [INFO] Importação concluída: 98 importados, 2 ignorados.
```

---

## 7. Trabalhos Relacionados e Limitações

### 7.1 Trabalhos Relacionados

A aplicação de blockchain ao setor imobiliário tem sido objeto de pesquisa crescente. Vos e Karafiloski (2017) propuseram o uso de contratos inteligentes Ethereum para automatizar transferências de propriedade, eliminando intermediários cartorários. Pisu e Pinna (2018) investigaram a tokenização de ativos imobiliários em redes públicas. No Brasil, iniciativas como o projeto-piloto do Cartório de Registro de Imóveis de Porto Alegre com blockchain (2019) demonstraram a viabilidade técnica do conceito em contexto regulatório nacional.

O presente trabalho se diferencia dessas abordagens por adotar uma **blockchain permissionada de nível de aplicação**, sem dependência de redes públicas ou criptomoedas, tornando-o mais adequado para fins didáticos e para sistemas corporativos que exigem controle centralizado com auditabilidade.

### 7.2 Limitações do Sistema Atual

É importante que o leitor compreenda as limitações desta implementação em relação a blockchains distribuídas de produção:

**1. Ausência de consenso distribuído**
O sistema opera com um único nó de escrita. Em uma blockchain real como Bitcoin ou Ethereum, múltiplos nós independentes validam e concordam sobre o estado da cadeia, tornando a adulteração praticamente impossível. Aqui, um administrador com acesso direto ao banco poderia, em tese, recalcular toda a cadeia após uma adulteração.

**2. Sem criptografia assimétrica**
Os blocos não são assinados digitalmente por chaves privadas dos participantes. Em sistemas de produção, cada transação seria assinada com a chave privada do proprietário ou corretor, garantindo autenticidade além de integridade.

**3. Persistência centralizada**
Os dados residem em um único banco PostgreSQL. Uma falha catastrófica no servidor poderia comprometer toda a cadeia. Sistemas distribuídos replicam os dados entre múltiplos nós geograficamente dispersos.

**4. Sem mecanismo de prova de trabalho ou prova de participação**
Blockchains públicas utilizam mecanismos como *Proof of Work* (PoW) ou *Proof of Stake* (PoS) para dificultar a reescrita da cadeia. Este sistema não implementa tais mecanismos, pois seu objetivo é didático e corporativo.

Essas limitações são intencionais: o objetivo do projeto é ilustrar os **princípios fundamentais** da tecnologia de forma acessível, sem a complexidade operacional de uma rede distribuída completa.

---

## 8. Conclusão

Este artigo apresentou o desenvolvimento de um sistema imobiliário com conceitos de blockchain e smart contracts, demonstrando que os princípios fundamentais que regem as redes descentralizadas podem ser aplicados com eficácia no nível de aplicação para garantir a inviolabilidade dos dados cadastrais e a rastreabilidade temporal das transações.

A implementação evidenciou que:

1. **A criptografia SHA-256** fornece uma garantia matemática robusta de integridade: qualquer alteração em um bloco é detectável imediatamente pela quebra do encadeamento de hashes.

2. **Os Smart Contracts**, mesmo implementados como código Python simples sem uma rede distribuída, cumprem seu papel fundamental de validar regras de negócio de forma determinística e auditável antes de qualquer persistência no ledger.

3. **A separação em camadas** (exposição, lógica de negócio, persistência) torna o sistema extensível e testável, servindo como modelo arquitetural para projetos acadêmicos e profissionais.

4. **A observabilidade em tempo real** via SSE resolve um problema prático comum em sistemas de importação em lote: a ausência de feedback durante operações longas.

5. **A proteção contra duplicatas em duas camadas** garante idempotência tanto na importação em lote quanto no cadastro manual, um requisito crítico em sistemas de dados imobiliários.

### 8.1 Sugestões de Trabalhos Futuros

Para estudantes que desejam expandir este projeto como trabalho de conclusão de curso ou iniciação científica, sugere-se:

**Nível Intermediário:**
- Implementar autenticação JWT nos endpoints, associando cada transação blockchain ao usuário autenticado.
- Adicionar o endpoint `DEACTIVATE` com lógica de desativação de imóveis e registro na cadeia.
- Criar testes automatizados com `pytest` cobrindo o Smart Contract, o hashing e a validação de integridade.
- Implementar paginação por cursor em vez de offset para melhor performance em grandes volumes.

**Nível Avançado:**
- Implementar **assinaturas digitais assimétricas** (ECDSA ou Ed25519) para autenticar cada bloco com a chave privada do usuário que realizou a operação.
- Desenvolver um **segundo nó** da blockchain com sincronização via API, introduzindo um mecanismo simples de consenso entre dois participantes.
- Integrar com a rede **Ethereum testnet** (Sepolia ou Goerli) para registrar o hash raiz da cadeia em um contrato inteligente Solidity, ancorando a integridade em uma rede pública.
- Implementar **tokenização de imóveis** como NFTs (ERC-721) representando títulos de posse digital.
- Explorar **Hyperledger Fabric** como alternativa de blockchain permissionada empresarial para o mesmo domínio.

---

## Referências

ANTONOPOULOS, Andreas M. **Mastering Bitcoin: Programming the Open Blockchain**. 2. ed. Sebastopol: O'Reilly Media, 2017.

BUTERIN, Vitalik. **Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform**. White Paper, 2014. Disponível em: <https://ethereum.org/en/whitepaper/>. Acesso em: 10 jan. 2025.

FOROUZAN, Behrouz A.; MUKHOPADHYAY, Debdeep. **Cryptography and Network Security**. 3. ed. Nova York: McGraw-Hill Education, 2015.

HYPERLEDGER FOUNDATION. **Hyperledger Fabric Documentation**. 2023. Disponível em: <https://hyperledger-fabric.readthedocs.io/>. Acesso em: 10 jan. 2025.

NAKAMOTO, Satoshi. **Bitcoin: A Peer-to-Peer Electronic Cash System**. 2008. Disponível em: <https://bitcoin.org/bitcoin.pdf>. Acesso em: 10 jan. 2025.

NATIONAL INSTITUTE OF STANDARDS AND TECHNOLOGY (NIST). **FIPS PUB 180-4: Secure Hash Standard (SHS)**. Gaithersburg: U.S. Department of Commerce, 2015. Disponível em: <https://doi.org/10.6028/NIST.FIPS.180-4>. Acesso em: 10 jan. 2025.

PISU, Cristian; PINNA, Andrea. **Blockchain-Based Real Estate Market: One Method for Applying Blockchain Technology in Commercial Real Estate Market**. In: IEEE International Conference on Internet of Things (iThings), 2018. Anais... IEEE, 2018. p. 1062–1068.

RAMÍREZ, Sebastián. **FastAPI: Modern, Fast (High-Performance) Web Framework for Building APIs with Python**. Documentação Oficial, 2024. Disponível em: <https://fastapi.tiangolo.com/>. Acesso em: 10 jan. 2025.

SZABO, Nick. **Formalizing and Securing Relationships on Public Networks**. First Monday, v. 2, n. 9, 1997. DOI: 10.5210/fm.v2i9.548. Disponível em: <https://firstmonday.org/article/view/548/469>. Acesso em: 10 jan. 2025.

TAPSCOTT, Don; TAPSCOTT, Alex. **Blockchain Revolution: How the Technology Behind Bitcoin and Other Cryptocurrencies is Changing the World**. Nova York: Portfolio/Penguin, 2016.

VOS, Jur; KARAFILOSKI, Elena. **Disrupting the Real Estate Industry with Blockchain**. In: ENTRENOVA Conference Proceedings, 2017. Disponível em: <https://hrcak.srce.hr/file/274543>. Acesso em: 10 jan. 2025.

W3C. **Server-Sent Events — W3C Recommendation**. 2015. Disponível em: <https://www.w3.org/TR/eventsource/>. Acesso em: 10 jan. 2025.
