# Conjunto de regras de validação — MetaPREMIS

Documento de referência das regras aplicadas pelo validador, com a fonte de cada uma.
Três camadas independentes, conforme discutido: validade de schema (XSD), conformidade
semântica (Data Dictionary + norma de conformidade) e expectativa do software (Archivematica).

## Camada 1 — Estrutura (XSD PREMIS v3)

Verificada de forma **exaustiva** por validação contra o próprio `premis-v3-0.xsd`
(via xmllint/WASM no navegador). Cobre, sem depender de transcrição manual:

- presença e cardinalidade de todo elemento obrigatório, por tipo de objeto
- ordem das sequências (xs:sequence) e construções xs:choice
- atributo `version="3.0"` obrigatório e enumerado
- `xsi:type` obrigatório no objeto (objectComplexType é abstrato)
- tipos de dado (xs:string, xs:long, nonNegativeInteger, etc.)

Fonte: XSD PREMIS v3 (fornecido; equivalente a https://www.loc.gov/standards/premis/v3/premis.xsd)

## Camada 2 — Conformidade semântica (Data Dictionary 3.0 + norma de conformidade)

Regras que o XSD não captura. Cada uma verificada por código próprio.

R2.1 — Unicidade de identificadores.
"Identifiers must be unique within the repository." Dois objetos, eventos ou agentes
não podem ter o mesmo par (type, value). [BLOQUEIA]
Fonte: PREMIS DD — Object Identifier, notas. https://www.loc.gov/standards/premis/v3/premis-3-0-final.pdf

R2.2 — Componente obrigatório dentro de contêiner opcional.
"If a container unit is optional, but a semantic component within that container is
mandatory, the semantic component must be supplied if and only if the container unit exists."
Ex.: criar fixity obriga messageDigestAlgorithm + messageDigest; criar linkingAgentIdentifier
obriga type + value. [BLOQUEIA quando o contêiner foi criado]
Fonte: PREMIS DD 3.0, seção de obrigação. https://www.loc.gov/standards/premis/v3/premis-3-0-datadictionary-only.pdf

R2.3 — Integridade referencial dos vínculos.
Todo vínculo (linkingEvent, linkingAgent, linkingObject, linkingRights, relatedObject,
relatedEvent) deve apontar para uma entidade existente no documento. Vínculo órfão é
defeito (o componente existe mas é inválido — viola R2.2). [BLOQUEIA]
Fonte: decorrência de R2.2 + modelo de dados PREMIS (entidades associadas por links).

R2.4 — "Mandatory if applicable".
Obrigatoriedade de uma unidade aplica-se apenas ao tipo de objeto a que se aplica.
Já tratado pela Camada 1 (o XSD por tipo) e pela lógica condicional de tipo.
Fonte: PREMIS DD 3.0 — "'Mandatory' actually means 'mandatory if applicable'."

R2.5 — Entidade sem vínculo.
Pela norma, é CONFORME (linking* são opcionais). NÃO bloqueia; gera aviso informativo.
Fonte: PREMIS DD 3.0 — linkingAgentIdentifier etc. são opcionais (O).

R2.6 — Conformidade Object+Event+Agent (nível de exchange).
Um conjunto conformante neste nível tem: todos os elementos mandatórios do Object;
um ou mais agentes; e Event suficiente para documentar as ações. [AVISO informativo]
Fonte: PREMIS conformance / NDIIPP 2014. https://www.loc.gov/standards/premis/premis-conformance-oct2010.pdf

## Camada 3 — Expectativa do Archivematica (release 1.18)

Aplicada apenas no perfil Archivematica.

R3.1 — Cada Event deve vincular-se a um Agent.
"Each Event should be linked to one Agent." Mais estrito que o XSD (onde é opcional).
[BLOQUEIA no perfil Archivematica]
Fonte: Archivematica 1.18 — Import metadata. https://www.archivematica.org/en/docs/archivematica-1.18/user-manual/transfer/import-metadata/

R3.2 — eventDateTime em ISO 8601.
"premis:eventDateTime value should be in ISO 8601 format." O XSD aceita qualquer string.
[BLOQUEIA no perfil Archivematica]
Fonte: Archivematica 1.18 — Import metadata.

R3.3 — originalName aponta para objects/.
O originalName vincula o objeto ao arquivo físico em objects/. [AVISO no perfil Archivematica]
Fonte: Archivematica 1.18 — Import metadata.

R3.4 — Cada premis.xml com ao menos um object, event e agent; identificadores locais.
[AVISO informativo]
Fonte: Archivematica 1.18 — Import metadata.

R3.5 — Rights não entram no premis.xml de importação.
Direitos entram por rights.csv ou pela interface. [INFORMATIVO; rights omitidos do XML]
Fonte: Archivematica 1.18 — Import metadata / PREMIS metadata.

## Vocabulário de eventType — regra específica (código × rótulo + @authority)

Diferente dos demais vocabulários (que só recebem sugestão), o `eventType` tem verificação
dedicada, contra a lista **oficial da LoC** (50 termos, código→rótulo):
`id.loc.gov/vocabulary/preservation/eventType`.

- **@authority ausente ou ="eventType"** com rótulo na lista → válido, sem mensagem.
- **@authority própria** (ex.: `perfil-local`) → **nota informativa** (não é aviso): o PREMIS
  permite vocabulário próprio declarado ("It does not require specific controlled vocabularies").
  Se o rótulo coincidir com um termo oficial, a nota alerta para possível engano.
- **@authority ausente e rótulo fora da lista** → **aviso** (recomendado; não bloqueia).
- **@valueURI presente** (`…/eventType/<código>`) → confronto **código × rótulo**:
  código inexistente → **erro** (bloqueia); código existe mas rótulo diverge do oficial →
  **erro**, citando os dois; código casa com o rótulo → válido.
- Toda mensagem cita o **`eventIdentifierValue`** do arquivo (e o id interno entre parênteses).

Escopo: a regra código × rótulo vale **apenas para eventType** — os demais vocabulários
(rightsBasis, relationshipSubType, act, etc.) seguem só como sugestão, por não terem sido
verificados contra a fonte.

### Diff da lista embutida (indica a origem)
A lista anterior tinha 39 rótulos **sem código**, um subconjunto do **PREMIS 2.x**:
- **faltavam (adições da v3):** accession, appraisal, compiling, digital signature generation,
  filename change, information package creation/merging/splitting, interpreting, metadata
  extraction, metadata modification, printing;
- **rótulos não oficiais:** `dispatch` (inexistente), `display` (oficial: *displaying* / `dsp`),
  `exportation` (oficial: *exporting* / `exp`).
Substituída pela tabela oficial dos 50 termos com código e rótulo.

## Relationship — vocabulário e hierarquia de objectCategory

`relationshipType` e `relationshipSubType` usam os vocabulários oficiais da LoC
(`relationshipType`, `relationshipSubType`), como menus dependentes (o subtipo é filtrado
pelo tipo) com opção **"Outro"**. Validação:

- `relationshipSubType` fora do vocabulário → **aviso**.
- **Coerência Type↔SubType**: o subtipo tem de pertencer ao tipo escolhido (ex.: *is Part Of*
  é `structural`; declarado como `derivation` → **aviso**).
- **Hierarquia de objectCategory** (subtipos structural de contenção/representação): a
  combinação (categoria do objeto, subtipo, categoria do relacionado) tem de ser válida —
  `isPartOf`/`hasPart` só entre **mesma** categoria; `includes`/`isIncludedIn` só entre
  categorias **diferentes** (rep→file/bit, file→bit); `isRepresentedBy` de IE para
  rep/file/bit; `represents` de rep/file/bit para IE; `hasRoot` de rep para file. Fora
  disso → **aviso** (ex.: *IE includes File*, *File isPartOf IE*, *Bitstream includes
  Representation*). Fonte: id.loc.gov/vocabulary/preservation/relationshipSubType + hierarquia
  objectCategory.

**Recíproco automático**: ao salvar um object, o app cria a relação inversa no objeto-alvo
(`isRepresentedBy`↔`represents`, `isPartOf`↔`hasPart`, `includes`↔`isIncludedIn`, etc.).

## Limites declarados (o que NÃO é verificado)

- Vocabulários controlados (relationshipSubType, rightsBasis, act, etc. — **exceto eventType**,
  ver seção acima): o PREMIS recomenda valores de vocabulário, mas não os torna obrigatórios
  nem fixa uma lista única ("different repositories will use different vocabularies"). Logo, o
  validador NÃO rejeita valores fora de vocabulário; apenas oferece os oficiais como sugestão.
  Fonte: PREMIS DD — "Value should be taken from a controlled vocabulary" (recomendação).
- Conteúdo de elementos *Extension (xs:any): validade depende de schema externo, fora de escopo.
- Formato de datas EDTF: o XSD define edtfSimpleType como equivalente a xs:string; não há
  validação de formato de data no schema (exceto a regra R3.2 do Archivematica para eventDateTime).
