from brownie import accounts
from scripts.utils import get_account
from brownie import interface, config, network


def main():
    get_weth()


def get_weth():
    # ABI - tengo la interfaz en la carpeta Interfaces
    # Address, pero como voy a estar usando diferentes networks, esta direccion deberia variar de acuerdo a eso
    # brownie config

    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])

    # fijandome en la interfaz, tengo una funcion 'depositar', yo cuando deposito ether en ese contrato
    # me hace la conversion 1 a 1, y me da Weth
    tx = weth.deposit({"from": account, "value": 0.1 * 10 ** 18})
    tx.wait(1)
    print("Received 0.1 weth")
    return tx
