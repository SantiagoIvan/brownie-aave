from scripts.get_weth import get_weth
from scripts.utils import get_account
from brownie import network, config, interface
from scripts.get_weth import get_weth
from web3 import Web3

AMOUNT = Web3.toWei(0.1, "ether")


def get_lending_pool():
    # abi. Si vamos a trabajar o a usar solo un par de funciones de un contrato, podemos crear
    # la interfaz solo con esas funciones
    # address
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    addr = lending_pool_addresses_provider.getLendingPool()
    # tengo la direccion del contrato de lending pool, faltaria el ABI, que lo agrego a la carpeta interfaces
    # y hago eso de las dependencias agregar la dependencia en el brownie-config
    lending_pool = interface.ILendingPool(addr)

    return lending_pool


def approve_erc20(
    amount, spender_address, erc20_address, account
):  # el spender seria a quien le estamos dando permiso para usar ese 'amount' de mis tokens
    # abi y address del token contract
    print("Approving erc20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender_address, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    return tx


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]

    if network.show_active() in ["mainnet-fork"]:
        get_weth()

    # para depositar, fijandome en la documentacion de aave, veo que necesito depositar en un contrato
    # llamado LendingPool

    # Necesito su ABI y su address. Para eso existe un contrato llamado LendingPoolProvider que te
    # devuelve la direccion actual de LendingPool
    lending_pool = get_lending_pool()

    # para depositar weth, necesito aprobar el token. Los token ERC20 tienen una funcion llamada approve
    approve_erc20(AMOUNT, lending_pool.address, erc20_address, account)
    tx = lending_pool.deposit(
        erc20_address, AMOUNT, account.address, 0, {"from": account}
    )
    # el tercer parametro seria 'a nombre de ' , 'onBehalfOf'. Le paso la direccion del contrato erc20
    # y le digo que puede retirar esa cantidad a nombre de 'x'(en este caso yo), osea que yo estoy dejando
    # que retiren esa cantidad, la cantidad que aprove anteriormente
    tx.wait(1)
    print("Deposited!")

    # get account data, cuanto puedo prestar, healthfactor, etc
    # https://docs.aave.com/developers/v/2.0/the-core-protocol/lendingpool
    (borrowable_eth, total_debt) = get_borrowable_data(lending_pool, account)
    # ahi se puede ver que lo que tengo depositado en weth, no es lo mismo que
    # la cantidad que puedo prestar, y eso es debido al ltv o loan to value. Varia segun cada asset,
    # En el caso de Eth, ese ltv es 80%
    print("Let's borrow!")
    # DAI in terms of eth
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )  # lo saco de chainlink

    dai_to_borrow = (1 / dai_eth_price) * (
        borrowable_eth * 0.95
    )  # Por seguridad no dispongo todo el eth para el prestamo
    # de ese resultado, lo divido por la cantidad en eth que sale cada dai, y asi tengo cuantos dai puedo pedir prestado

    print(f"We are going to borrow {dai_to_borrow}")
    dai_contract_addr = config["networks"][network.show_active()][
        "dai_contract_address"
    ]  # la direccion esta la saco de la doc de aave, porque suelen cambiar de version.
    borrow_tx = lending_pool.borrow(
        dai_contract_addr,
        Web3.toWei(dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account},
    )
    borrow_tx.wait(1)
    print("You borrowed some dai! Displaying new information")
    (borrowable_eth, total_debt) = get_borrowable_data(lending_pool, account)
    repay_all(AMOUNT, lending_pool, account)
    print("Listorti, depositaste y pediste prestado con Aave programaticamente!!")

    return


def repay_all(amount, lending_pool, account):
    approve_erc20(
        Web3.toWei(AMOUNT, "ether"),
        lending_pool,
        config["networks"][network.show_active()]["dai_contract_address"],
        account,
    )
    repay_tx = lending_pool.repay(
        config["networks"][network.show_active()]["dai_contract_address"],
        AMOUNT,
        1,
        account.address,
        {"from": account},
    )
    repay_tx.wait(1)
    print("Repayed!")


def get_asset_price(price_feed_address):
    # abi y address
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[
        1
    ]  # para tomar el precio e ignorar los demas elementos de la tupla resultante
    converted = Web3.fromWei(latest_price, "ether")
    print(f"Dai/Eth price is {converted}")
    return float(converted)


def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)

    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of Eth deposited")
    print(f"You have {total_debt_eth} worth of Eth borrowed")
    print(f"You can borrow {available_borrow_eth} worth of Eth")

    return (float(available_borrow_eth), float(total_debt_eth))
