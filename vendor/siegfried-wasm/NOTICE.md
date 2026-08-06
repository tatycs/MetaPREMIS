# Siegfried (build WebAssembly) — vendorizado

Os arquivos `sf.wasm` e `wasm_exec.js` são o **build WASM oficial do Siegfried v1.11.6**,
por Richard Lehane. As assinaturas do **PRONOM** já vêm **embutidas** no `sf.wasm`
(não é preciso um arquivo `.sig` externo).

- Projeto: https://github.com/richardlehane/siegfried
- Release: https://github.com/richardlehane/siegfried/releases/tag/v1.11.6
- Licença do Siegfried: **Apache License 2.0**
- `wasm_exec.js`: runtime Go (Google; licença BSD), distribuído junto com o build.

Uso na Oficina PREMIS: identificação de formato **no navegador** (PRONOM completo), via a
API `identify(handle, "json")` exposta pelo WASM. **Nada é enviado** — o WASM roda
localmente na página e lê os arquivos pela File System Access API (Chrome/Edge).
Carregado **sob demanda** (só ao clicar), para não pesar o carregamento normal do app.
