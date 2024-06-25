# Polynomial tool box
[info]: <> (Scripts inside this folder are for polynomial operation [basic-char2]+++)
The (defining) polynomials are entered as:


| usual notation | in binary |  in hex |
| --- | --- | --- |
|$1$ | `0b1`|`0x1`|
|$x$ | `0b10`|`0x2`|
|$x^2$ | `0b100`|`0x4`|
|$x+1$ | `0b11`|`0x3`|
|$x^2+x+1$ | `0b111`|`0x7`|

sometimes the notation is also: $x^3=x+1$ but this is the same as $x^3+x+1$ and `0b1011/0xb`

$\implies$ Values are reduced when they have the same / a higher degree than the defining polynomial