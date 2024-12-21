# clean-tree

```bash
conda create --name clean-tree python
conda activate clean-tree
```

```bash
python -m pip install '.[dev]'
```

## Running tests

```
tox -e cov_clean,py312
```