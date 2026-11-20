def test_pacote_nginx_instalado(host):
    """Confere se a instalação do pacote foi realizada."""
    pacote = host.package("nginx")
    assert pacote.is_installed, "O pacote nginx não está instalado"


def test_servico_nginx_ativo_e_habilitado(host):
    """Confere o serviço agora e sua habilitação para o próximo boot."""
    servico = host.service("nginx")
    assert servico.is_running, "O serviço nginx está parado"
    assert servico.is_enabled, "O serviço nginx não está habilitado no boot"


def test_nginx_escutando_na_porta_80(host):
    """Confere se há um socket IPv4 escutando na porta HTTP do contêiner."""
    porta = host.socket("tcp://0.0.0.0:80")
    assert porta.is_listening, "A porta 80 não está escutando conexões"
