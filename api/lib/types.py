from dataclasses import fields, is_dataclass
import datetime
import dataclasses
import typing
from typing import cast, List

import lib.data


class TypescriptDefs:
    tstypes = {
        str: 'string',
        int: 'number',
        datetime.datetime: 'string' # currently
    }

    def to_ts_type(self, t: type) -> str:
        if is_dataclass(t):
            return t.__name__
        elif type(t) == type(List):
            assert isinstance(t, typing._GenericAlias)
            if t._name == 'List':
                inner = self.to_ts_type(t.__args__[0])
                return f"Array<{inner}>"
            elif t._name == 'Dict':
                return 'object'
            else:
                raise RuntimeError('unknown type')
        else: 
            return self.tstypes[t]

    def build_def(self, cl: type) -> str:
        lines = []
        lines.append(f"export interface {cl.__name__} {{")
        for f in fields(cl):
            lines.append(f"\t{f.name}: {self.to_ts_type(f.type)};")
        lines.append('}')

        return '\n'.join(lines)

    def write_types(self, fname: str):
        types = [
                lib.data.Comment, 
                lib.data.Post,
                lib.data.User,
                lib.data.Group,
                lib.data.PostPayload
        ]
        with open(fname, 'w') as outf:
            for it in types:
                outf.write(self.build_def(it))
                outf.write('\n\n')

