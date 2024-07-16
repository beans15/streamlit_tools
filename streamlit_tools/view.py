from typing import Iterable, Iterator, Sized

import streamlit as st


def st_tqdm[
    T
](seq: Iterable[T], title: str = "", total: int | None = None) -> Iterator[T]:
    if isinstance(seq, Sized):
        total = len(seq)

    if total is not None:
        bar = st.progress(0.0, f"{title} [0/{total}]")
        for i, value in enumerate(seq):
            yield value
            bar.progress((i + 1) / total, f"{title} [{i + 1}/{total}]")
        bar.empty()
    else:
        with st.spinner(title):
            yield from seq
