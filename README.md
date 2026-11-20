# Laboratório de testes de infraestrutura com Nginx

Exercício de DevOps para instalar o Nginx em um contêiner Ubuntu e verificar
automaticamente se a configuração funcionou. A proposta é praticar Ansible,
Molecule e Testinfra com uma automação pequena.

## O papel de cada ferramenta

- **Ansible:** executa a receita que instala e inicia o Nginx. Uma role é uma
  pasta que organiza essa receita e seus metadados.
- **Docker:** fornece o contêiner Ubuntu usado como servidor temporário.
- **Molecule:** organiza a criação, a configuração, os testes e a remoção desse
  ambiente.
- **Testinfra:** verifica o resultado dentro do servidor. O `assert` indica uma
  condição que precisa ser verdadeira para o teste passar.

## Onde fica cada parte

```text
servidor_nginx/
├── meta/main.yml                       # Identificação da role
├── tasks/main.yml                      # Instalação e inicialização do Nginx
└── molecule/default/
    ├── molecule.yml                    # Contêiner e ferramentas do cenário
    ├── converge.yml                    # Playbook que chama a role
    └── tests/test_default.py           # Verificações do servidor
```

## Como executar

Use o terminal Linux de um GitHub Codespaces, conforme o roteiro da atividade.
No Windows, os comandos abaixo devem ser executados em um ambiente Linux,
como o WSL com Docker disponível, e não diretamente no PowerShell.

Na pasta raiz do projeto, prepare um ambiente Python separado:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install ansible molecule molecule-docker pytest-testinfra
docker info
```

O `docker info` precisa mostrar que o serviço Docker está acessível. As
dependências acima seguem o roteiro fornecido; suas versões não estão fixadas,
então a compatibilidade deve ser confirmada ao executar no ambiente Linux.

O roteiro também orienta ativar esta variável para a combinação de ferramentas
usada no laboratório:

```bash
export ANSIBLE_ALLOW_BROKEN_CONDITIONALS=true
cd servidor_nginx
molecule test
```

Essa variável é uma medida de compatibilidade indicada no material da atividade.
A configuração do contêiner, incluindo as permissões para executar o `systemd`
(gerenciador de serviços do Linux), foi mantida conforme o roteiro.

## O que observar no resultado

O ciclo cria o contêiner, aplica a role, repete a configuração para testar a
idempotência, executa as verificações e remove o ambiente temporário.

**Idempotência** significa que, quando o servidor já está no estado desejado,
repetir a configuração não deve fazer novas alterações. Na etapa `idempotence`,
observe `changed=0` e ausência de falhas.

Os testes conferem três pontos:

1. O pacote `nginx` está instalado.
2. O serviço está rodando e habilitado para iniciar no boot.
3. A porta TCP 80 está escutando em `0.0.0.0` dentro do contêiner.

Como as verificações foram separadas em três funções, o resultado esperado da
etapa `verify` é **3 passed**, em vez do **1 passed** mostrado no exemplo do PDF.
Isso é uma expectativa para a execução, não um resultado já obtido neste projeto.
O teste da porta não verifica o conteúdo de uma página nem o acesso pelo navegador
do Windows; o cenário não publica a porta no computador hospedeiro.

Para investigar um erro, execute as etapas separadamente, dentro de
`servidor_nginx`:

```bash
molecule create
molecule converge
molecule idempotence
molecule verify
```

Ao terminar a investigação, remova o contêiner de teste:

```bash
molecule destroy
```

## Ajustes desta versão

- Os nomes das tarefas descrevem o estado desejado do servidor.
- Os booleanos usam `true`, mantendo o significado anterior de `yes`.
- O namespace passou a ser `felipe`, e a chamada da role passou a usar
  `felipe.servidor_nginx`. Esses dois arquivos precisam usar o mesmo nome.
- Cada grupo de verificações tem seu próprio teste e mensagens de erro em
  português, facilitando localizar o problema.
- O `.gitignore` evita incluir caches e o ambiente Python em futuros commits.
- Este README explica a estrutura, a execução e a leitura dos resultados.

O código recebido identifica **João Victor Luiz** como autor original, crédito
preservado em `meta/main.yml`. Esta versão contém adaptações para o estudo de
Felipe, com auxílio do Codex.

## Relação com os anexos

O roteiro prático pede a role Nginx e as verificações de pacote, serviço e porta.
Os dois guias didáticos explicam o papel das ferramentas e o ciclo dos testes.
A configuração principal desse laboratório foi preservada.

O desafio teórico é uma entrega separada: pede um relatório sobre IaC versus
configuração manual, idempotência, testes de infraestrutura e um exemplo de
mercado diferente de um servidor web básico. Este README documenta o laboratório;
o relatório teórico ainda precisa ser elaborado.

Para estudar essa parte, tente explicar por que um histórico no Git ajuda a
entender mudanças, o que deveria acontecer ao aplicar a role dez vezes e por que
um teste em contêiner reduz riscos sem garantir que toda falha de produção será
detectada. Como exemplo para desenvolver, considere uma rotina de backup de
banco de dados: quais arquivos, permissões e serviços você verificaria? Como
testaria também a restauração dos dados?

## Estado da validação

Nesta revisão foi verificada localmente a sintaxe do arquivo Python. O ciclo
`molecule test` ainda precisa ser executado no ambiente Linux: o serviço Docker
estava indisponível, e Ansible, Molecule e Testinfra não estavam instalados no
Python local. A aprovação completa depende dessa execução; não há log de sucesso
do laboratório nesta revisão.
