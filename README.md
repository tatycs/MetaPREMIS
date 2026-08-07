# MetaPremis — construtor de `premis.xml`

Ferramenta de aula para construir documentos **PREMIS 3.0** a partir de metadados de
sistemas produtores. Roda inteiramente no navegador (nada sai da máquina), em dois
perfis de saída: **Archivematica** (premis.xml de importação) e **PREMIS 3.0 completo**
(documento autônomo).

A validação tem **três camadas** (detalhe e fontes em [REGRAS-VALIDACAO.md](REGRAS-VALIDACAO.md)):

1. **Estrutura (XSD)** — validação real e exaustiva contra o `premis-v3-0.xsd` **oficial**,
   rodando no próprio navegador via [`xmllint-wasm`](vendor/xmllint-wasm/) (libxml2 compilado
   para WebAssembly). Gata o download: documento que não valida no schema não é exportado.
2. **Conformidade semântica** — Data Dictionary 3.0 + norma de conformidade (regras próprias).
3. **Expectativa do Archivematica 1.18** — aplicada só no perfil Archivematica.

## Rodar localmente

O validador usa módulo ES + Web Worker + WebAssembly + um `fetch` do XSD. **Nada disso
funciona abrindo o HTML por `file://`** — é preciso servir por http. Há um servidor de
desenvolvimento pronto (Python, sem dependências):

```
python serve.py 8000
```

Depois abra **http://127.0.0.1:8000/**. O `serve.py` existe só para o desenvolvimento:
entrega `.mjs` e `.wasm` com o MIME correto e atende em paralelo (o worker busca o `.wasm`
enquanto a página espera). Em produção isso não é necessário.

## Publicar no GitHub Pages

O GitHub Pages já serve `.mjs` como `text/javascript` e `.wasm` como `application/wasm`,
então basta subir os arquivos na raiz do repositório e habilitar o Pages:

- `index.html`, `premis-v3-0.xsd` e a pasta `vendor/` precisam ficar na **raiz** publicada
  (os caminhos são relativos: `./premis-v3-0.xsd`, `./vendor/xmllint-wasm/index-browser.mjs`).
- Settings → Pages → Source: branch `main` → Save. Em 1–2 min:
  `https://SEU-USUARIO.github.io/SEU-REPO/`.

Não é preciso embutir o `.wasm` em base64: ele fica como arquivo servido (≈760 KB,
carregado sob demanda na primeira validação).

## Estrutura

```
index.html                      o programa (núcleo + interface + ajuda)
premis-v3-0.xsd                 schema PREMIS 3.0 OFICIAL (Library of Congress)
REGRAS-VALIDACAO.md             regras de validação, com a fonte de cada uma
serve.py                        servidor de desenvolvimento (http + MIME correto)
vendor/xmllint-wasm/            libxml2/WASM (MIT) — index-browser.mjs, worker, .wasm, COPYING
docs/IMPORTACAO.md              tutorial de importação (premis.xml e CSV/JSON)
docs/verificacao-xsd/           procedência e verificação do XSD (ver abaixo)
```

## Importação

A aba "importar arquivo" abre um `premis.xml` para edição (reconstrói o modelo e
religa os vínculos por identificador) ou cria entidades em lote a partir de CSV/JSON
(com templates para baixar). Passo a passo em [docs/IMPORTACAO.md](docs/IMPORTACAO.md).

## Procedência do XSD

O `premis-v3-0.xsd` deste repositório é o arquivo **oficial** da Library of Congress,
verificado como estruturalmente idêntico à transcrição usada nas sessões anteriores.
Método, resultado e como reproduzir: [docs/verificacao-xsd/VERIFICACAO.md](docs/verificacao-xsd/VERIFICACAO.md).

## Licença

Distribuído sob a **GNU Affero General Public License v3.0 (AGPL-3.0)** — veja
[LICENSE](LICENSE). Copyright © 2026 Tatiana Canelhas. Distribuído sem garantia.

Como é uma aplicação que roda em rede (servida pelo GitHub Pages), a AGPL pede que os
usuários tenham acesso ao código-fonte — ele está em https://github.com/tatycs/oficina-premis.

### Terceiros
`vendor/xmllint-wasm/` é uma porta de libxml2 para WebAssembly, sob licença **MIT**
(ver `vendor/xmllint-wasm/COPYING`) — compatível com a AGPL e mantida sob seus próprios termos.
O `premis-v3-0.xsd` é o schema oficial da Library of Congress (padrão PREMIS).
