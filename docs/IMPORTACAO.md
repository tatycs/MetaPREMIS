# Importação na Oficina PREMIS

O painel **Origem** tem, além do **formulário**, dois modos de entrada por arquivo:
**importar arquivo** (um `premis.xml` inteiro para edição, ou **CSV/JSON** em lote) e
**extrair metadados** (lê os próprios arquivos e gera os objects). Tudo roda no
navegador — nenhum arquivo sai da máquina.

## 1. Importar um `premis.xml` (PREMIS 3.0) e editar

Use isto para abrir um documento PREMIS existente, revisar e ajustar.

1. No painel **Origem**, clique em **importar arquivo**.
2. Em **Importar premis.xml**, clique em **escolher premis.xml** e selecione o arquivo.
3. O documento é carregado no **Modelo interno**: objects, events, agents e rights.
   - Os **vínculos** (que no XML são por identificador *Type/Value*) são religados
     automaticamente às entidades do próprio documento.
   - Aparece um resumo do que foi importado e, se houver, um aviso sobre vínculos
     **não trazidos** (ver limites abaixo).
4. Edite: em **Modelo interno**, cada card tem um botão **editar** que recarrega a
   entidade no formulário (mantendo o identificador). Altere e clique em
   **salvar alterações**. Ou use as abas (object/event/agent/rights) normalmente.
5. Em **Saída + validação**, clique em **verificar integridade** e depois **baixar .xml**.

> Importar **substitui** o conteúdo atual do modelo (há confirmação se já houver dados).

### O que é trazido
Todos os campos cobertos pelo construtor: os quatro tipos de object (file,
representation, bitstream, intellectualEntity) com suas características, fixity,
formato, storage, assinatura, environment, relationship; events com detalhe,
resultado e vínculos; agents com nome/tipo/versão/nota e vínculos
(inclusive `linkingRightsStatementIdentifier` e `linkingEnvironmentIdentifier`);
e rights (`rightsStatement`) nas quatro bases (copyright, license, statute, other).

Verificado por *round-trip*: um documento gerado pela ferramenta, importado e
gerado de novo, sai **idêntico** e válido contra o XSD oficial.

### Limites (o que NÃO é trazido)
- **Vínculos para fora do documento:** um vínculo cujo identificador não corresponde
  a nenhuma entidade do próprio arquivo é **omitido** (e listado no aviso). O modelo
  só representa vínculos entre entidades presentes.
- **`rightsExtension`, `agentExtension`, `objectCharacteristicsExtension` e demais
  `*Extension` (`xs:any`):** pontos de extensão para XML de schema externo, fora do
  escopo do construtor; não são importados.
- **`statuteInformation` repetido:** o construtor edita um por rights; ao importar,
  o primeiro é carregado.

## 2. Importar CSV/JSON (com template)

Use isto para criar várias entidades de uma vez a partir de uma planilha/exportação.
Disponível para **object**, **event** e **agent** (rights exige o formulário, por
causa da estrutura condicional por base de direito).

1. Selecione a aba da entidade (object/event/agent).
2. Clique em **baixar template CSV** ou **baixar template JSON**. O arquivo já vem
   com os cabeçalhos certos e uma linha de exemplo.
3. Preencha o template (uma linha por entidade) e salve.
4. Clique em **escolher CSV/JSON** e selecione o arquivo.
5. Confira o **mapeamento** coluna → campo (ele tenta adivinhar) e clique em
   **criar N entidade(s)**.

### Colunas dos templates
| Entidade | Colunas |
|---|---|
| object | `idType`, `idValue`, `formatName`, `originalName` |
| event  | `idType`, `idValue`, `eventType`, `dateTime` |
| agent  | `idType`, `idValue`, `name`, `type` |

O CSV/JSON cria entidades com os **campos básicos**; a estrutura completa
(sub-blocos repetíveis, assinatura, vínculos) é montada/editada no formulário.

### Exemplo de CSV (object)
```
idType,idValue,formatName,originalName
UUID,5b2c8d1e-0000-4aaa-bbbb-1234567890ab,MP3,objects/bird.mp3
```

### Exemplo de JSON (agent)
```json
[
  { "idType": "repository code", "idValue": "NRI", "name": "Not a Real Institution", "type": "organization" }
]
```

## 3. Extrair metadados no navegador (sem instalar nada)

Em vez de instalar DROID/Siegfried, dá para extrair metadados técnicos **no próprio
navegador** — os arquivos **não saem da máquina**.

1. No painel **Origem**, clique em **extrair metadados**.
2. Clique em **escolher arquivos** (ou **escolher pasta**, para um lote).
3. Para cada arquivo o app calcula:
   - **tamanho** (`size`);
   - **fixity**: hash **SHA-256** (ou SHA-512, opcional) — via Web Crypto, nativo do navegador;
   - **formato** por *magic-byte* (conteúdo), com **PUID do PRONOM quando determinável
     com segurança** (PDF e GIF trazem a versão no próprio arquivo; MP3 = `fmt/134`;
     XML = `fmt/101`; texto = `x-fmt/111`).
4. Revise a lista e clique em **adicionar N object(s) ao modelo**. Cada arquivo vira um
   `object` (xsi:type `file`) com `objectIdentifier` (UUID gerado), `originalName`,
   `size`, `fixity` e `format` (nome + registro PRONOM/PUID, quando houver) preenchidos.
5. Edite o que faltar pelos cards/abas e valide.

**Limites (honestos):** a identificação por magic-byte cobre os formatos mais comuns;
onde não há PUID seguro, o app preenche só **nome/MIME** (sem PUID). Para identificação
**PRONOM completa e autoritativa**, rode **DROID** ou **Siegfried** localmente e importe
o relatório (**seção 4**). Arquivos muito grandes são lidos inteiros na memória para o cálculo do hash.

> Sobre a versão do PDF: o app lê a versão do **cabeçalho** (`%PDF-x.y`) **e** o override
> `/Version` do dicionário Catalog (`/Root`) — comum em PDFs assinados/atualizados — e usa a
> **maior** das duas (ISO 32000-1 §7.5.2), mapeando ao PUID correto. Ainda assim, para
> identificação autoritativa, o Siegfried/DROID (seção 4) é a referência.

### Identificar com o Siegfried **no navegador** (sem instalar nada) — Chrome/Edge

No mesmo painel **extrair metadados** há também **“Siegfried: escolher pasta / arquivos”**.
Isso roda o **Siegfried oficial em WebAssembly** dentro da própria página (base **PRONOM
completa**, embutida) — **sem instalar nada e sem enviar arquivos**. Preenche o
`formatRegistry` (PUID/nome/versão) nos objects e **preserva a fixidez**. Requer **Chrome ou
Edge** (usa a File System Access API) e baixa ~8&nbsp;MB do WASM só na 1ª vez. No
Firefox/Safari, use a identificação embutida ou a importação de `sf.json`/CSV (seção 4).

> **Para a oficina:** é o caminho mais simples para o aluno — abre o site, clica em
> *extrair metadados* (fixidez + tamanho) e depois em *Siegfried: escolher pasta* (formato
> PRONOM autoritativo), tudo no navegador, sem instalação.

## 4. Importar identificação de formato (Siegfried / DROID) — PRONOM completo

Para identificação de formato **de produção** (base PRONOM completa e autoritativa), rode
**Siegfried** (preferencial) ou **DROID** na sua máquina e importe o resultado. A ferramenta
lê os arquivos **localmente**; o app só lê o *relatório* que você importa — **nada é enviado**.
A fixidez calculada no navegador (Web Crypto) é **preservada**; apenas o `formatRegistry`
(PUID, nome, versão) é preenchido, e a identificação da ferramenta **prevalece** sobre o
magic-byte interno.

### Gerar o relatório

**Siegfried** (https://www.itforarchivists.com/siegfried):

```bash
sf -json objects/ > sf.json      # JSON (recomendado — traz a versão do sf e do PRONOM)
sf -csv  objects/ > sf.csv       # CSV
sf -version                      # confira: ex. "siegfried 1.11.0 ... DROID_SignatureFile_V120.xml"
```

No JSON, a versão do Siegfried e da assinatura PRONOM vêm no próprio arquivo
(`siegfried` e `identifiers[].details`) e são registradas numa **nota** do formato.

**DROID** (The National Archives — tem interface gráfica; bom para começar).
Página: https://github.com/digital-preservation/droid/releases. Requer **Java** instalado
(verifique com `java -version`; o DROID 6.7 pede Java 11+, e o **6.6.1** roda com Java 8).
Passo a passo no Windows:

1. Baixe o **`droid-binary-6.x.x-bin.zip`** (o arquivo que termina em `-bin.zip`) e **extraia**
   para uma pasta simples, ex.: `C:\DROID`.
2. Abra com **duplo clique em `droid.bat`**. Se o Windows (SmartScreen) avisar:
   *Mais informações → Executar assim mesmo* (é software do The National Archives).
3. **Atualize as assinaturas** (só na 1ª vez): *Tools → Check for signature updates → Download*.
   **Anote a versão** que aparecer (ex.: `DROID_SignatureFile_V120`) para rastreabilidade — o
   CSV do DROID **não** a inclui.
4. **New** (novo perfil) → **Add** → escolha a **pasta** com os arquivos → **Start**.
5. **Export → Export profiles as CSV**, opção **“one row per file”** → salve como `droid.csv`.

Nada é enviado: o DROID lê os arquivos **localmente**; o *Check for signature updates* apenas
baixa a base pública do PRONOM (dado de referência).

### Importar no app

1. No painel **Origem** → **importar arquivo**.
2. Em **Importar identificação de formato**, clique em **importar identificação
   (Siegfried/DROID)** e escolha `sf.json`, `sf.csv` ou o CSV do DROID (detecção automática
   pelo cabeçalho).
3. O app casa cada linha ao `object` do modelo pelo **nome do arquivo** (o `originalName` sem
   o prefixo `objects/`; o **tamanho** desempata nomes iguais) e preenche `formatName`,
   `formatVersion` e `formatRegistry` = **PRONOM** / **PUID** / `role=specification`. Havendo
   **múltiplos matches** (Siegfried), usa o de maior confiança e registra os demais e o
   `warning` numa **nota**, junto com a origem (ex.: *formato identificado por Siegfried
   1.11.0 / PRONOM DROID_SignatureFile_V120.xml*).
4. Arquivos do relatório **sem object** no modelo viram novos `object` (tipo `file`, com
   `size`, **sem fixidez** — rode a extração se quiser o hash). Registros **UNKNOWN** são
   apenas reportados.
5. O resumo mostra quantos objects foram **atualizados**, **criados**, quantos ficaram **sem
   correspondência** no relatório e quantos registros ficaram **sem identificação** — nada é
   silenciado.

> **Ordem sugerida:** primeiro **extrair metadados** (fixidez + tamanho no navegador), depois
> **importar a identificação** do Siegfried/DROID (formato/PUID). A fixidez não é tocada.

## Depois de importar
Reveja sempre em **Saída + validação**: a **camada 1** valida a estrutura contra o
XSD oficial; as **camadas 2 e 3** checam unicidade de identificadores, integridade
referencial e as expectativas do Archivematica. O download só é liberado com tudo
conforme.
