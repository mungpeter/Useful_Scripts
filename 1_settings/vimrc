set nocompatible
set backspace=indent,eol,start
set history=300
set ruler
set hlsearch
set laststatus=2
noremap <Leader>m mmHmt:%s/<C-V><cr>//ge<cr>'tzt'm
syntax on
filetype plugin on
autocmd BufReadPost *
     \ if line("'\"") > 0 && line("'\"") <= line("$") |
          \   exe "normal! g`\"" |
               \ endif
