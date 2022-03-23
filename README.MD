1 - Intercambiar Eth por Weth (wrapped Eth, la version ERC20 de Eth, ya que Eth no cumple con el estandar y no puede ser usada por todas las defi)
   Depositando Eth en el contrato de WETH, nos transferira WETH

2 - Deposito un poco de WETH en Aave, ( Defi app )

3 - Con el interes ganado al depositar, pedimos prestado algun otro asset ( collateral )

   2.2 - Vender ese asset que pedimos prestado ( Short selling )

4 - Pagar lo que prestamos


No vamos a necesitar deployar ningun contrato, ya que vamos a interactuar con Aave, ya posee su smart contract deployado, tanto en Mainnet como en Testnet

Tests:

- Integration test: kovan
- Unit tests: mainnet-fork