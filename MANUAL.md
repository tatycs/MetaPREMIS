# Manual do MetaPREMIS

**MetaPREMIS** é uma ferramenta de mesa (roda no navegador) para **construir, importar,
validar e exportar documentos PREMIS 3.0** (`premis.xml`). Foi pensada para ensino e para
produção leve de metadados de preservação a partir de sistemas produtores.

- **Site:** https://tatycs.github.io/MetaPREMIS
- **Código:** https://github.com/tatycs/MetaPREMIS
- **Tudo local:** nenhum arquivo, metadado ou hash sai da sua máquina — a montagem, a
  identificação de formato e a validação contra o XSD acontecem **dentro do navegador**.

> Documentos irmãos: [`docs/IMPORTACAO.md`](docs/IMPORTACAO.md) detalha as importações;
> [`REGRAS-VALIDACAO.md`](REGRAS-VALIDACAO.md) lista as regras do validador.

---

## Sumário

1. [Conceitos rápidos de PREMIS](#1-conceitos-rápidos-de-premis)
2. [A interface: os três painéis](#2-a-interface-os-três-painéis)
3. [Origem — como entram os dados](#3-origem--como-entram-os-dados)
4. [Modelo interno](#4-modelo-interno)
5. [Saída + validação](#5-saída--validação)
6. [DICIONÁRIO (ajuda por campo)](#6-dicionário-ajuda-por-campo)
7. [Salvar e retomar o trabalho](#7-salvar-e-retomar-o-trabalho)
8. [Privacidade e como é servido](#8-privacidade-e-como-é-servido)
9. [Limites conhecidos e dúvidas frequentes](#9-limites-conhecidos-e-dúvidas-frequentes)
10. [Licença e créditos](#10-licença-e-créditos)

---

## 1. Conceitos rápidos de PREMIS

PREMIS 3.0 descreve a preservação em quatro **entidades**:

- **object** — a coisa preservada. Tem quatro tipos (`xsi:type`): **file** (arquivo),
  **representation** (conjunto), **bitstream** (fluxo dentro de um arquivo) e
  **intellectualEntity** (a entidade intelectual, ex.: um processo, um dossiê).
- **event** — algo que aconteceu com o objeto (captura, ingestão, assinatura, validação de
  fixidez, etc.), com data, resultado e vínculos a agentes e objetos.
- **agent** — quem/o que agiu (pessoa, organização, software).
- **rights** — a base legal/política de acesso e uso (copyright, license, statute, other),
  com os atos concedidos e restrições.

Os **vínculos** entre entidades são feitos por **identificador** (um `Type` + um `Value`).
O MetaPREMIS religa esses vínculos automaticamente quando você importa.

O documento sai na ordem exigida pelo schema: **object → event → agent → rights**.

---

## 2. A interface: os três painéis

No topo há três botões — **1 Origem**, **2 Modelo**, **3 Saída**. Eles **alternam painéis**
(não são abas exclusivas): clique para mostrar/ocultar cada um; vários podem ficar abertos
**lado a lado**. A escolha é lembrada entre sessões.

- **Origem** — onde os dados entram (formulário, importação, extração).
- **Modelo** — o que já está montado (cards por entidade), para revisar e editar.
- **Saída** — o `premis.xml` gerado, a validação e o download.

Outros controles:
- **Tema claro/escuro** (☾/☼), no canto superior; respeita a preferência do sistema e é
  lembrado.
- **Barra de status** — mostra a contagem (obj/ev/ag/dir) e um selo de conformidade
  (✓ conforme / ⚠ validar / ✕ corrigir).

---

## 3. Origem — como entram os dados

O painel **Origem** tem três modos: **formulário**, **importar arquivo** e
**extrair metadados**. Em qualquer um deles, os dados vão para o **Modelo**.

### 3.1 Formulário

Abas **object · event · agent · rights**. Cada aba tem os campos da entidade, agrupados em
blocos que espelham a hierarquia do PREMIS. Recursos:

- **Blocos repetíveis** — botões **+** adicionam instâncias (ex.: várias `fixity`,
  `format`, `significantProperties`, `relationship`, vínculos, extensões `xs:any`). O **×**
  remove.
- **Ajuda por campo (ⓘ)** — abre/fecha a explicação do campo, com todos os atributos do
  **Data Dictionary** oficial, em **inglês ou português** (ver [seção 6](#6-dicionário-ajuda-por-campo)).
- **Vínculos por seleção** — em events e rights, você liga a agentes/objetos já existentes
  no modelo, escolhendo o papel (role).
- **salvar alterações** — grava a entidade em edição no modelo.

### 3.2 Importar arquivo

Quatro caminhos (detalhes e exemplos em [`docs/IMPORTACAO.md`](docs/IMPORTACAO.md)):

**a) Importar `premis.xml` (PREMIS 3.0).** Carrega um documento inteiro para edição.
Religa os vínculos internos automaticamente. Verificado por *round-trip*: um documento
gerado, importado e gerado de novo sai idêntico e válido. **Limites:** vínculos que apontam
para fora do documento e pontos de extensão `xs:any` não são trazidos (são listados no aviso).

**b) Importar CSV completo (documento PREMIS).** Um **único CSV** com o documento inteiro:
- coluna **`entity`** por linha (object/event/agent/rights);
- colunas com prefixo **`ob./ev./ag./rt.`** e subcampos por ponto
  (`ob.formatDesignation.formatName`);
- **repetível = repetir a coluna** (sem índice), **na ordem hierárquica** do PREMIS;
- vínculos por *IdentifierType + Value*, religados automaticamente.

Use **baixar modelo (CSV)** para obter o `template-premis-completo.csv` já com o cabeçalho
certo (blocos repetíveis aparecem 2×, o 2º vazio) e uma linha de exemplo por entidade —
abra numa planilha e substitua pelos seus dados.

**c) Importar CSV/JSON por-entidade.** Cria object/event/agent com **campos básicos** a
partir de uma planilha simples; você confere o mapeamento coluna→campo e completa a
estrutura no formulário.

**d) Importar identificação de formato (Siegfried/DROID).** Você roda a ferramenta
**localmente** e importa o relatório (`sf -json`, `sf -csv` ou CSV do DROID). O app casa por
nome de arquivo e preenche o `formatRegistry` (PUID/nome/versão) — **sem tocar a fixidez**.
Se o relatório trouxer hash (ex.: `sf -sha256`), a fixidez também é preenchida onde faltava.

### 3.3 Extrair metadados no navegador

Sem instalar nada, o app lê os próprios arquivos e cria objects. Escolha **arquivos** ou
**pasta** (no Chrome/Edge usa a File System Access API — sem aquele aviso de "upload"). Para
cada arquivo calcula:

- **tamanho**;
- **fixidez** — hash **SHA-256** (ou **SHA-512**, opção) via Web Crypto;
- **formato** por *magic-byte*, com **PUID do PRONOM quando determinável com segurança**
  (PDF — inclusive a versão via cabeçalho e override `/Version` do Catalog —, PNG, JPEG,
  TIFF, BMP, GIF, MP3, WAV, XML, texto e Office/ODF/EPUB via ZIP). Onde não há PUID seguro,
  preenche só nome/MIME.

E o **Siegfried no navegador**: o botão *Siegfried: escolher pasta/arquivos* roda o **WASM
oficial do Siegfried** (base PRONOM completa, embutida) localmente — identifica o formato
**autoritativo** e calcula a fixidez, tudo no navegador (Chrome/Edge; ~8 MB baixados só na
1ª vez).

**Opções (valem para os dois modos acima):**
- **usar SHA-512** (padrão SHA-256);
- **prefixar originalName com `objects/`** (para o Archivematica).

Tanto o extrair quanto o Siegfried **aplicam direto** ao modelo e mostram um resumo (sem
passo extra de confirmação).

---

## 4. Modelo interno

O painel **Modelo** mostra o que já existe, em **cards** por entidade. Cada card tem
**editar** (recarrega a entidade no formulário, mantendo o identificador). Relações
estruturais entre objects (is part of / includes, etc.) são refletidas na organização
hierárquica.

Importar um documento (XML ou CSV completo) **substitui** o conteúdo atual do modelo (com
confirmação).

---

## 5. Saída + validação

O painel **Saída** mostra o `premis.xml` gerado e valida em **três camadas**:

- **Camada 1 — schema XSD.** Validação real contra o **`premis-v3-0.xsd` oficial**, rodando
  no navegador (libxml2 via xmllint-wasm). É disparada pelo botão **verificar integridade**.
- **Camadas 2–3 — regras do modelo.** Unicidade de identificadores, integridade referencial
  dos vínculos e as expectativas do perfil. (A lista completa está em
  [`REGRAS-VALIDACAO.md`](REGRAS-VALIDACAO.md).)

**Perfis de saída:**
- **PREMIS 3.0 completo** — o documento inteiro, rights inclusos.
- **Archivematica** — `premis.xml` de importação; **omite os rights do XML** (o Archivematica
  ingere direitos por um `rights.csv` à parte) e ajusta o que o Archivematica espera.

**Fluxo:** clique em **verificar integridade** (roda camada 1 + 2–3 de uma vez). Se estiver
tudo conforme, o **baixar .xml** é liberado. O download só acontece com o documento
validado e **atual** (se você mexer no modelo, revalide).

---

## 6. DICIONÁRIO (ajuda por campo)

O botão **ⓘ** ao lado de cada campo abre um painel com **todos os atributos daquele elemento
no PREMIS Data Dictionary 3.0** (definição, justificativa, restrições, notas de uso,
exemplos). Você escolhe ler em **inglês** (texto oficial do LoC) ou **português**.

> **Sobre o português:** não existe uma tradução oficial do Data Dictionary. A versão em PT
> do MetaPREMIS é uma **tradução própria (não oficial)**, feita para a oficina — útil para
> estudo, mas para citação formal use o texto oficial em inglês.

---

## 7. Salvar e retomar o trabalho

- **salvar trabalho** — baixa um `metapremis-trabalho.json` com todo o modelo. Guarde-o.
- **carregar trabalho** — restaura o modelo a partir desse JSON.

É a forma de pausar e continuar depois sem perder nada (lembre: nada fica em servidor algum).

---

## 8. Privacidade e como é servido

- **Nada é enviado.** Leitura de arquivos, cálculo de hash, identificação de formato
  (inclusive o Siegfried WASM) e validação XSD acontecem no navegador.
- **Em produção** o app é servido pelo **GitHub Pages** (estático). O código é aberto —
  qualquer pessoa pode auditar o que roda.
- **Localmente**, para desenvolvimento, há um `serve.py` (o validador XSD usa módulo ES +
  Web Worker + WebAssembly, que não funcionam sob `file://`; o `serve.py` entrega tudo por
  http com os MIME certos). Em produção não é necessário.

---

## 9. Limites conhecidos e dúvidas frequentes

- **"Importei um `premis.xml` e os identificadores/tipos sumiram."** O arquivo provavelmente
  não está no **PREMIS 3.0 padrão** — por exemplo, `objectIdentifierType/Value` soltos sem o
  invólucro `<objectIdentifier>`, ou `<objectCategory>` em vez de `xsi:type`. O importador é
  feito para o schema oficial; serializações fora do padrão não são lidas corretamente (e não
  passariam no XSD). Regenerar a partir do **CSV completo** produz PREMIS válido.
- **Firefox/Safari.** A extração via File System Access API e o Siegfried WASM exigem
  **Chrome ou Edge**. Nesses outros navegadores, use a importação de arquivos ou de relatórios.
- **`keyInformation` e outros `xs:any`.** Pontos de extensão de schema externo não são
  importados (são avisados), como no import de `premis.xml`.
- **Vínculos para fora do documento.** Um `related*`/`linking*` cujo identificador não tem
  entidade correspondente é omitido e listado no aviso.

---

## 10. Licença e créditos

- MetaPREMIS © 2026 Tatiana Canelhas — **AGPL-3.0** (ver `LICENSE`).
- Terceiros: **xmllint-wasm** (MIT) para a validação XSD; **Siegfried** (Apache-2.0, Richard
  Lehane) no build WebAssembly para identificação PRONOM. Ver `vendor/*/` para as licenças.
- PREMIS Data Dictionary e XSD: Library of Congress (fontes oficiais em id.loc.gov / loc.gov).
