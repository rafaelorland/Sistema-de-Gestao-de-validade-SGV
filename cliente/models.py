from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome do Cliente")
    cpf_cnpj = models.CharField(max_length=20, unique=True, verbose_name="CPF/CNPJ")
    endereco = models.CharField(max_length=255, verbose_name="Endereço")
    email = models.EmailField(max_length=254, unique=True, verbose_name="Email do Cliente", null=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class TelefoneCliente(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='telefones', verbose_name="Cliente")
    numero = models.CharField(max_length=14, verbose_name="Número de Telefone")

    def __str__(self):
        return f"Cliente: {self.cliente.nome} - Número: {self.formata_numero()}"

    def formata_numero(self):
        return f"({self.numero[:2]}) {self.numero[2:7]}-{self.numero[7:]}"

    class Meta:
        verbose_name = "Telefone do Cliente"
        verbose_name_plural = "Telefones dos Clientes"
