# create-wrapper-components-kfp

Usage

```py
from create_wrapper_components import create_wrapper_components
from your_custom package import py_func_component_1, py_func_component_2

components = [py_func_component_1, py_func_component_2]
create_wrapper_components(components,
                          base_image='your_base_image',
                          install_kfp_package=True,
                          filename='tmp/components.py')
```

Requirements:
- your functions should have type hint for input and output args (and only kfp-py-func available types)
- your base_image for the components and the image/pc where you run the `create-wrapper-components`  should have the same `your_custom_package` version