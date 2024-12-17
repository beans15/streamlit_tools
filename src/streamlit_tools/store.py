from typing import TypeVar
import streamlit as st

T = TypeVar("T")


def use_store(class_: type[T]) -> T:
    name = f"__store##{class_.__qualname__}"
    if name not in st.session_state:
        st.session_state[name] = class_()
    return st.session_state[name]
