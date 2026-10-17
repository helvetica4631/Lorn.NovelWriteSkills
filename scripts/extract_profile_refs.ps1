# общий-написание-аннотации 外化脚本
# 将 SKILL.md 中可外化的方法论节拆到 references/

$SkillDir = "D:\第二职业\进行中\网文写作\提示词工程\CommonSkills\общий-написание-аннотации"
$SkillMd = Join-Path $SkillDir "SKILL.md"
$RefDir = Join-Path $SkillDir "references"

$c = [System.IO.File]::ReadAllText($SkillMd)

# 1. 简介即开篇原则 → references/简介即开篇原则.md
$start1 = $c.IndexOf("`r`n## 简介即开篇：简介与开头的同构原则（新增）")
$end1 = $c.IndexOf("`r`n## 简介的三句法", $start1 + 5)
if ($start1 -ge 0 -and $end1 -gt $start1) {
  $s1 = $c.Substring($start1, $end1 - $start1)
  $r1 = "# 简介即开篇原则`r`n`r`n> 本文件是 общий-написание-аннотации 的支撑数据，由 SKILL.md 外化所得。`r`n$s1"
  [System.IO.File]::WriteAllText("$RefDir\简介即开篇原则.md", $r1)
  $n1 = "`r`n## 简介即开篇原则`r`n`r`n> 详见 references/简介即开篇原则.md。包含简介与开头在核心任务、交易本质、认知缺口、卖点展示等8维度的同构对照。`r`n"
  $c = $c.Replace($s1, $n1); Write-Host "1. OK"
}

# 2. 简介的三句法 → references/метод-трёх-фраз-аннотации.md
$start2 = $c.IndexOf("`r`n## 简介的三句法（新增——吸收自知乎开篇精华）")
$end2 = $c.IndexOf("`r`n## 简介的切片原则", $start2 + 5)
if ($start2 -ge 0 -and $end2 -gt $start2) {
  $s2 = $c.Substring($start2, $end2 - $start2)
  $r2 = "# 简介三句法`r`n`r`n> 本文件是 общий-написание-аннотации 的支撑数据，由 SKILL.md 外化所得。`r`n$s2"
  [System.IO.File]::WriteAllText("$RefDir\метод-трёх-фраз-аннотации.md", $r2)
  $n2 = "`r`n## 简介的三句法`r`n`r`n> 详见 references/метод-трёх-фраз-аннотации.md。包含三句法的疑问/情绪/代入三任务及示例。`r`n"
  $c = $c.Replace($s2, $n2); Write-Host "2. OK"
}

# 3. 简介的切片原则 → references/принцип-среза-аннотации.md
$start3 = $c.IndexOf("`r`n## 简介的切片原则 vs 大纲体（新增——吸收自知乎开篇精华）")
$end3 = $c.IndexOf("`r`n## 信息差与认知缺口", $start3 + 5)
if ($start3 -ge 0 -and $end3 -gt $start3) {
  $s3 = $c.Substring($start3, $end3 - $start3)
  $r3 = "# 简介切片原则`r`n`r`n> 本文件是 общий-написание-аннотации 的支撑数据，由 SKILL.md 外化所得。`r`n$s3"
  [System.IO.File]::WriteAllText("$RefDir\принцип-среза-аннотации.md", $r3)
  $n3 = "`r`n## 简介的切片原则 vs 大纲体`r`n`r`n> 详见 references/принцип-среза-аннотации.md。包含大纲体与切片式的对比、切片简介的核心原则及AI搜索摘要摘录区格式。`r`n"
  $c = $c.Replace($s3, $n3); Write-Host "3. OK"
}

# 4. 信息差与认知缺口 → references/информационная-разница-и-когнитивный-разрыв.md
$start4 = $c.IndexOf("`r`n## 信息差与认知缺口在简介中的应用（新增）")
$end4 = $c.IndexOf("`r`n## 简介的交易本质自检", $start4 + 5)
if ($start4 -ge 0 -and $end4 -gt $start4) {
  $s4 = $c.Substring($start4, $end4 - $start4)
  $r4 = "# 信息差与认知缺口`r`n`r`n> 本文件是 общий-написание-аннотации 的支撑数据，由 SKILL.md 外化所得。`r`n$s4"
  [System.IO.File]::WriteAllText("$RefDir\информационная-разница-и-когнитивный-разрыв.md", $r4)
  $n4 = "`r`n## 信息差与认知缺口在简介中的应用`r`n`r`n> 详见 references/информационная-разница-и-когнитивный-разрыв.md。包含信息差公式及使用方法。`r`n"
  $c = $c.Replace($s4, $n4); Write-Host "4. OK"
}

# 5. 简介的交易本质自检 → references/самопроверка-сделки-аннотации.md
$start5 = $c.IndexOf("`r`n## 简介的交易本质自检（新增——吸收自知乎开篇精华）")
$end5 = $c.IndexOf("`r`n## 简介的 GEO 友好度自检", $start5 + 5)
if ($start5 -ge 0 -and $end5 -gt $start5) {
  $s5 = $c.Substring($start5, $end5 - $start5)
  $r5 = "# 简介交易本质自检`r`n`r`n> 本文件是 общий-написание-аннотации 的支撑数据，由 SKILL.md 外化所得。`r`n$s5"
  [System.IO.File]::WriteAllText("$RefDir\самопроверка-сделки-аннотации.md", $r5)
  $n5 = "`r`n## 简介的交易本质自检`r`n`r`n> 详见 references/самопроверка-сделки-аннотации.md。包含自检三问及判断标准。`r`n"
  $c = $c.Replace($s5, $n5); Write-Host "5. OK"
}

# 更新 references 清单
$oldRefs = $c.Substring($c.IndexOf("`r`n## 继续读取的 references"), $c.IndexOf("`r`n<!-- ===== Layer 2") - $c.IndexOf("`r`n## 继续读取的 references"))
$newRefs = @"
## 继续读取的 references

- `references/шаблон-структуры-аннотации-и-правила-сжатия.md`
- `references/ситуационные-хуки-и-психологическая-ценность.md`
- `references/напоминание-о-различиях-аннотаций-платформ.md`
- `references/сохранение-и-версии-аннотации.md`
- `references/geo-правила-оптимизации-аннотаций.md`
- `references/简介即开篇原则.md`
- `references/метод-трёх-фраз-аннотации.md`
- `references/принцип-среза-аннотации.md`
- `references/информационная-разница-и-когнитивный-разрыв.md`
- `references/самопроверка-сделки-аннотации.md`
- `../../исследования-письма/GEO小说项目核心参考.md`（必读——了解 GEO 基础知识与小说四维框架）

**以下为腾讯专栏专用 references（仅在目标平台包含腾讯专栏时加载）：**
- `references/колонка-tencent-первая-фраза-аннотации-и-теги.md`
- `references/колонка-tencent-аннотация-круглый-стол-многомерно.md`
- `references/колонка-tencent-аннотация-пять-делать-пять-не-делать.md`
- `references/колонка-tencent-нормы-аннотации-от-нескольких-редакторов.md`
- `references/колонка-tencent-три-элемента-аннотации-и-конкретизация-профессии.md`
- `references/колонка-tencent-приёмы-аннотации-и-классификация-стилей-платформ.md`
"@
$c = $c.Replace($oldRefs, "`r`n$newRefs`r`n")

[System.IO.File]::WriteAllText($SkillMd, $c)
Write-Host "=== Done ==="
