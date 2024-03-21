from typing import Callable, Any
import inspect
import streamlit as st


def st_callback(func: Callable[[Any], None]):
    sig = inspect.signature(func)
    params = list(sig.parameters.keys())
    assert len(params) == 1, f"Too many parameters in function '{func.__name__}'"

    param = params[0]

    class Callback:
        @property
        def key(self):
            return f"__callback_{func.__name__}##{param}"

        @property
        def handler(self):
            def wrapper():
                value = st.session_state[self.key]
                func(value)

            return wrapper

        @property
        def kwargs(self):
            return {"key": self.key, "on_change": self.handler}

        def __call__(self, *args, **kwargs):
            return func(*args, **kwargs)

    return Callback()
