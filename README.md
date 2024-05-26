
# cryptm
[![python](https://img.shields.io/badge/Python->3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
![GitHub Repo stars](https://img.shields.io/github/stars/melo-afk/cryptm)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

Small python script collection of scripts that implement algorithms for prime finite fields and binary/prime elliptic curves





## Installation

Install cryptm with git

```bash
    git clone https://github.com/melo-afk/cryptm
```
    
## Usage/Examples


### Available options:
```
-h, --help   show the help message
-l, --list   list available methods/scripts
```


#### Listing all available scripts with their descriptions:
```Bash
python3 cryptm.py [folder] --list
```
### Starting a script:
```Bash
python3 cryptm.py <module> <args> [-h, --help]
```
All available scripts have their own `-h, --help` option 

<details>
<summary>Currently available scripts</summary>

| Script Name        | Description                                                                              | Category              | Rating |
|--------------------|------------------------------------------------------------------------------------------ | ---------------------- | ---|
|char2/            |  Scripts inside this folder are for polynomial operation                                  | [basic-char2]          | +++|
|char2/all         |  Get all Elements in a gf defined by the relation                                         | [basic-char2]          | +++|
|char2/inv         |  Bruteforce the inverse of an element                                                     | [basic-char2]          | +++|
|char2/mul         |  Multiplies two polynomials and reduces the result                                        | [basic-char2]          | +++|
|char2/reduce      |  Reduces a polynomial using the given polynomial relation                                 | [basic-char2]          | +++|
|egcd              |  Extended Euclidean algorithm                                                             | [basic]                | +++|
|gcd               |  Largest common divisor of a and b                                                        | [basic]                | +++|
|gen               |  Find the smallest generator / all generators                                             | [basic]                | +++|
|ord               |  Find the order of an element in a prime galois field                                     | [basic]                | +++|
|bsgs              |  Babystep GIANTSTEP discrete logarithm finder                                             | [dlog]                 | +++|
|dlog              |  Finds the discrete log: g^x\\equiv res (mod p)                                           | [dlog]                 | +++|
|curves_bin/       |  Scripts inside this folder are for binary elliptic curves of the form y^2+xy=x^3+ax^2+b  | [ecc-point-char2]      | +++|
|curves_bin/paam   |  Multiply a point with Add and Multiply: e.g 5 * P(r,s)                                   | [ecc-point-char2]      | +++|
|curves_bin/padd   |  Add two points: P1+P2                                                                    | [ecc-point-char2]      | +++|
|curves_bin/pdupe  |  Duplicates a point: 2*P = P+P                                                            | [ecc-point-char2]      | +++|
|curves_bin/pexists|  Check if a point exists in the curve                                                     | [ecc-point-char2]      | +++|
|curves_bin/pord   |  Get the order of a point                                                                 | [ecc-point-char2]      | +++|
|curves/           |  Scripts inside this folder are for prime elliptic curves of the form y^2=x^3+ax^2+b      | [ecc-point]            | +++|
|curves/paam       |  Multiply a point with Square and Multiply: e.g 5 * P(r,s)                                | [ecc-point]            | +++|
|curves/padd       |  Add two points: P1+P2                                                                    | [ecc-point]            | +++|
|curves/pdupe      |  Duplicate a point: 2*P = P+P                                                             | [ecc-point]            | +++|
|curves/pexists    |  Check if a point exists in the curve                                                     | [ecc-point]            | +++|
|curves/pord       |  Get the order of a point on a char>3 ec                                                  | [ecc-point]            | +++|
|mtm               |  Montgommery ladder to calculate: base**power % mod                                       | [high-power-modulo]    | +++|
|sqm               |  Square and multiply                                                                      | [high-power-modulo]    | +++|
|pmo               |  P minus 1 method                                                                         | [prime-factorization]  | +++|
|tdiv              |  Trial division to find prime factors                                                     | [prime-factorization]  | +++|
|soe               |  Find all primes <= b with the help of the sieve of erastothenes                          | [prime-generation]     | +++|
|mrt               |  Miller Rabin prime test                                                                  | [prime-test]           | +++|
|pft               |  Prime fermat test                                                                        | [prime-test]           | +++|
|qsqrt             |  Find sqares of the base modulo the mod                                                   | [root-finder]          | +++|


</details>

### Examples

<details>
<summary>soe (Sieve of erastothenes)</summary>
    
```Bash
python3 cryptm.py soe -h
```

**Output**
```
usage: cryptm.py soe [-h] limit

Sieve of erastothenes

positional arguments:
  limit       the limit to which pimes should be returned

options:
  -h, --help  show this help message and exit
```

```Bash
python3 cryptm.py soe 48
```

**Output**
```
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

</details>



<details>
<summary>sqm (Square and multiply)</summary>

```Bash
python3 cryptm.py sqm -h
```

**Output**
```
usage: cryptm.py sqm [-h] base power mod

Square and multiply

positional arguments:
  base        base
  power       power
  mod         modulo

options:
  -h, --help  show this help message and exit
```
**Calculating $(953^{2211}\mod 4799)$**
```Bash
python3 cryptm.py sqm 953 2211 4799
```

**Output**
```
2620
```
$$\implies(953^{2211}\equiv 2620\mod 4799)$$
</details>



<details>
<summary>curves/paam (Multiply a point on prime elliptic curves)</summary>

```Bash
python3 cryptm.py curves/paam -h
```

**Output**
```
usage: cryptm.py curves/paam [-h] [-d] m r s a b p

Multiply a point on a prime ec: e.g 5*P

positional arguments:
  m           amount of multiplications
  r           r / x component of the point
  s           s / y component of the point
  a           paramter a of the elliptic curve
  b           paramter b of the elliptic curve
  p           the modulo of the galois field

options:
  -h, --help  show this help message and exit
  -d          debug logging
```

**Multiplying a point**

```bash
python3 cryptm.py curves/paam 199, 501, 449, 1, 679, 1151
```

**Output**
```
The point 199*(501, 449)=(866, 715) exists: True
```

Elliptic curve: 

$$y^2\equiv x^3+x+679 \qquad[x,y]\in\mathbb{F}_{1151}$$
or
$$F(X,Y)=Y^2-X^3-X-679\qquad[x,y]\in\mathbb{F}_{1151}$$

</details>


<details>
<summary>curves_bin/paam (Multiply a point on binary elliptic curves)</summary>

```Bash
python3 cryptm.py curves_bin/paam -h
```

**Output**
```
usage: cryptm.py curves_bin/paam [-h] m r s a b p

Multiply a point on a binary ec: e.g 5*P

positional arguments:
  m           amount of multiplications
  r           r / x component of the point
  s           s / y component of the point
  a           paramter a of the elliptic curve
  b           paramter b of the elliptic curve
  p           the polynomial/defining relation of the galois field

options:
  -h, --help  show this help message and exit
```

**Multiplying a point**

```bash
python3 cryptm.py curves_bin/paam 4, 0x3, 0x2, 0b101, 0x1, 0xb 
```

(You can enter numbers here in decimal, binary or hexadecimal format)

**Output**
```
The point 4*(x + 1, x)=(x^2 + 1, x^2 + x) exists: True
```

Elliptic curve with the defining polynomial/relation $a^3=a+1$: 

$$y^2+xy\equiv x^3+(a^2 + 1)x^2+1 \qquad[x,y]\in\mathbb{F}_{2^3}$$
or
$$F(X,Y)=Y^2+XY+X^3+(a^2 + 1)X^2+1\qquad[X,Y]\in\mathbb{F}_{2^3}$$


</details>

### Testing:
Requirement: `pytest` package (`pip install pytest`)

```Bash
pytest .
```

### Linting:
Requirement: `mypy` package (`pip install mypy`)

```Bash
mypy . --strict
```