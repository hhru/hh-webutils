## hh-webutils

hh.ru python common web utility library.

Не содержит бизнес-логики и кода, зависящего от Frontik.

### Установка и использование

```
apt-get install hh-webutils
# или
cd hh-webutils ; python setup.py develop
```

```python
import hhwebutils  # that's it
```

Настоятельно рекомендуется сделать [run_tests.sh](run_tests.sh) pre-commit хуком в гите.
Для этого достаточно сделать:

```shell
ln -s ../../run_tests.sh .git/hooks/pre-commit
```
