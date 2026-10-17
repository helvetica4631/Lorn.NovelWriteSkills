# Fix remaining dead reference files
$repo = "D:\第二职业\进行中\网文写作\提示词工程"

$fixes = @(
    @{sm="CommonSkills\общий-шлифовка-основного-текста\SKILL.md"; ref="колонка-qimao-читательская-рентабельность-и-телефон.md"; desc="七猫专栏阅读性价比与手机端适配增补"}
    @{sm="CommonSkills\общий-шлифовка-основного-текста\SKILL.md"; ref="правила-визуализации-технических-описаний.md"; desc="技术描写可视化规则"}
    @{sm="CommonSkills\общий-создание-основного-текста\SKILL.md"; ref="карточка-проверки-склейки-главы-начало-середина-конец-и-цепь-хуков.md"; desc="拼章检查卡"}
    @{sm="CommonSkills\общий-создание-основного-текста\SKILL.md"; ref="трёхстадийное-расширение-каркаса-жанры-и-объём.md"; desc="三阶段骨架扩写拼合"}
    @{sm="CommonSkills\общий-проектирование-реестра-улик-и-завязок\SKILL.md"; ref="арка-переклички-реквизита-и-отслеживание-появлений.md"; desc="道具呼应弧线与出场追踪"}
)

foreach ($f in $fixes) {
    $sm = Join-Path $repo $f.sm
    $c = Get-Content $sm -Raw
    $orig = $c

    # Find the ## 继续读取的 references section
    $refIdx = $c.IndexOf("## 继续读取的 references")
    if ($refIdx -lt 0) { Write-Host "NO SECTION: $($f.sm)"; continue }

    # Find end of this section (next ## heading or end of file)
    $secEnd = $c.IndexOf("`r`n## ", $refIdx + 10)
    if ($secEnd -lt 0) { $secEnd = $c.Length }

    # Check if this ref already exists
    if ($c.Substring($refIdx, $secEnd - $refIdx) -match [regex]::Escape($f.ref)) {
        Write-Host "ALREADY EXISTS: $($f.ref)"; continue
    }

    # Insert the new line before the section end
    $before = $c.Substring(0, $secEnd)
    $after = $c.Substring($secEnd)
    # Backtick format for markdown inline code
    $tick = [char]96  # backtick
    $newLine = "`r`n- ${tick}references/$($f.ref)${tick} — $($f.desc)"
    $newC = $before + $newLine + $after

    if ($newC -ne $c) {
        [System.IO.File]::WriteAllText($sm, $newC)
        Write-Host "FIXED: $($f.sm) + $($f.ref)"
    } else {
        Write-Host "NO CHANGE: $($f.sm) - $($f.ref)"
    }
}

Write-Host "=== Done ==="
