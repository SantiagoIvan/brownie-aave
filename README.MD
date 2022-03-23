1 - Intercambiar Eth por Weth (wrapped Eth, la version ERC20 de Eth, ya que Eth no cumple con el estandar y no puede ser usada por todas las defi)
   Depositando Eth en el contrato de WETH, nos transferira WETH

2 - Deposito un poco de WETH en Aave, ( Defi app )
Para eso, mediante el contrato ERC20 de WEth, le doy permiso al contrato de lending pool para usar mis tokens, mediante la funcion approve, donde le indico la cantidad.
Luego, para que Aave efectivamente tenga ese token, llamo a su funcion 'deposit'

3 - Solicitamos informacion de nuestra cuenta.

4 - Con el interes ganado al depositar, pedimos prestado algun otro asset ( collateral )
Pedimos prestado Dai. Para eso nos comunicamos Chainlink, usando el data price feed.
Para poder comunicarnos con ese contrato, necesitamos su ABI y su address(la sacamos de la documentacion) 
Luego, con una simple conversion, calculamos cuanto dai podemos pedir prestado con la cantidad
de weth que disponemos (de los intereses generados al depositar)

Llamamos a la funcion 'borrow' indicandole la direccion del contrato erc20 que vamos a pedir prestado.
En este caso, para la red de kovan, van cambiando de version entonces lo saque de la documentacion de Aave.

4 - Pagar lo que prestamos


No vamos a necesitar deployar ningun contrato, ya que vamos a interactuar con Aave, ya posee su smart contract deployado, y con otros ERC20
