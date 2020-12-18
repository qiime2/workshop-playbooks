def build_base_fn(name):
    base_fn = name.replace(' ', '-').replace('.', '')
    base_fn = base_fn.replace('--', '-').lower()

    return base_fn
