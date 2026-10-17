# usage:  export TM_DIR=/tmp/work  (рабочая папка, где лежит очередь Q и tsv)  ;  . .github/translation-workflow/ap.sh
#         ap QUEUE START END ROW_FROM ROW_TO tsv relpath
# QUEUE — файл-очередь (результат prep_queue.py); START..END — строки данных в очереди (без заголовков "# путь: ..."),
# ROW_FROM..ROW_TO — строки моего tsv, соответствующие этому диапазону; relpath — файл в репозитории.
ap(){ W="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; sed -n "$4,$5p" "$TM_DIR/$6" > "$TM_DIR/apx.tsv"; python3 "$W/align.py" "$TM_DIR/$1" $2 $3 "$TM_DIR/apx.tsv" "$TM_DIR/apx.o" && python3 -I "$W/tmflow.py" done "$7" "$TM_DIR/apx.o"; }
