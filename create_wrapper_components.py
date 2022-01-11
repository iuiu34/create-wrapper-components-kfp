"""Create wrapper components."""
import inspect

_SCRIPT_START = """\"\"\"Components.\"\"\"
from typing import NamedTuple

from edo.ml_plumber import Constants
from kfp.v2.dsl import component

base_image = Constants().DEFAULT_IMAGE


# get_output_path = create_component_from_func_in_base_image(
#     func=get_output_path,
#     base_image=base_image
# )
"""


def get_func_source(func):
    """Get func source."""
    name = func.__name__
    signature = inspect.signature(func)
    return_annotation = signature.return_annotation
    signature = str(signature)
    signature = signature.split('->')
    if len(signature) != 2:
        raise ValueError

    params = signature[0]
    return_types = signature[1]

    params = params.replace(')', '\n    )')

    if '**' in params:
        params = params[:params.index('**')]
        params = params[:params.rfind(',')]
        params = f"{params})"

    if hasattr(return_annotation, '_field_types'):
        return_types = return_annotation._field_types
        return_types = [f"('{k}', {v.__name__})" for k, v in return_types.items()]
        return_types = ',\n'.join(return_types)
        return_types = f" NamedTuple('{return_annotation.__name__}',[{return_types}]): # noqa"

    signature = f"{params}->{return_types}"

    func_source = f'def {name}{signature}:\n' \
                  f'    """Kfp wrapper."""\n' \
                  '    kwargs = locals()\n' \
                  '    kwargs = {k: None if v == "None" else v for k, v in kwargs.items()}\n' \
                  f'    from {func.__module__} import {name}\n' \
                  f'    return {name}(**kwargs)\n'
    return func_source


def create_wrapper_components(components, base_image, install_kfp_package=True,
                              filename='tmp/components.py'):
    """Create wrapper components."""
    out = [_SCRIPT_START]
    for component in components:
        aux = f'@component(base_image={base_image}, install_kfp_package={install_kfp_package})\n'
        aux += get_func_source(component)
        out += [aux]

    out = '\n\n'.join(out)
    # print(out)
    with open(filename, 'w') as f:
        f.write(out)
    return
