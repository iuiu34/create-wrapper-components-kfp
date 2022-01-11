# create-wrapper-components-kfp

Usage

```py
from create_wrapper_components import create_wrapper_components
from your_package import py_func_component_1, py_func_component_2

components = [py_func_component_1, py_func_component_2]
create_wrapper_components(components,
                          install_kfp_package=True,
                          filename='tmp/components.py')
```

py_func_component should have input & output args typed according to kgp rules in your package