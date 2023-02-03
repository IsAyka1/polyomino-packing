# polyomino-packing
`polyominos` `packing` `matrix`


## How to execute
```commandline
source venv/bin/activate
```
```commandline
python search.py
```
### Input
* **by shell** 
1. in search.py:
```commandline
by_shell = True
```
2. input example

`Input NxM:` 4 4

`Input count of different rectangular polyominos:` 1

`Input rectangular polyominos (height, weight, count):` 2 2 2

`Input count of different П-polyominos:` 2

`Input П-polyominos (height, weight, count):` 3 4 1

`Input П-polyominos (height, weight, count):` 2 3 1

* **by code** 
1. in search.py 
```commandline
by_shell = False
```
2. in input.py
```commandline
(N, M) = (4, 6)
rec_polyominos = [((2, 2), 2)]
arc_polyominos = [((3, 4), 1), ((2, 3), 1)]
```

### Result example

`Result:` True


## Testing

### How to test
```commandline
pytest
```

## Asymptotic complexity is about
n*m - dimentions of matrix,
k - count of all polyominos

* time - O( (n*m)! )
* space - O( max(n*m, k!) ) 

