# ----------------------------------------------------------------------------
# Copyright (c) 2016-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

def build_base_fn(name):
    base_fn = name.replace(' ', '-').replace('.', '')
    base_fn = base_fn.replace('--', '-').lower()

    return base_fn
