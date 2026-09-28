class BancoError(Exception):
    """Erro base das regras de negócio."""


class ValorInvalidoError(BancoError):
    pass


class SaldoInsuficienteError(BancoError):
    pass


class LimiteSaqueExcedidoError(BancoError):
    pass


class LimiteSaquesDiariosError(BancoError):
    pass


class UsuarioJaExisteError(BancoError):
    pass


class UsuarioNaoEncontradoError(BancoError):
    pass


class CpfInvalidoError(BancoError):
    pass
