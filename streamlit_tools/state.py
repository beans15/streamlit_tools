from typing import TypeVar
import streamlit as st

T = TypeVar("T")


def use_state(class_: type[T]) -> T:
    name = f"__state##{class_.__name__}"
    if name not in st.session_state:
        st.session_state[name] = class_()
    return st.session_state[name]
