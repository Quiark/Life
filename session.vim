set et
set background=light
set termguicolors
color PaperColor

" TODO make it autoload after typescript
syn match typescriptSpecial "v-for\|v-bind\|v-model\|v-on"

let g:syntastic_python_mypy_exec = "/Users/roman/Devel/Life/env36/bin/mypy"
let g:syntastic_python_checkers = ["mypy"]
