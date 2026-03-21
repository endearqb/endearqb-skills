# GB/T 7714-2015 参考文献格式规范

本文件为实验报告引文提供格式模板、搜索策略和HTML渲染示例。

---

## 一、文献类型标识符

| 标识符 | 文献类型 | 典型来源 |
|--------|----------|----------|
| `[J]`  | 期刊论文 | CNKI、PubMed、ACS、RSC、Elsevier、Springer |
| `[M]`  | 专著/教材 | 出版社官网、Google Books |
| `[S]`  | 标准文献 | std.samr.gov.cn（国家标准）、iso.org、astm.org |
| `[D]`  | 学位论文 | 中国知网（CNKI）学位论文库、ProQuest |
| `[R]`  | 技术报告 | 机构官网、arXiv |
| `[EB/OL]` | 网络资源 | 官方数据库网页、机构页面 |
| `[DB/OL]` | 数据库 | 在线数据库 |

---

## 二、各类型格式模板

### 期刊论文 [J]
```
作者1, 作者2, 作者3, 等. 题名[J]. 刊名, 年份, 卷(期): 起始页-终止页. DOI.
```
- 作者≤3人：全部列出
- 作者>3人：列前3位，后加"等"（中文）或"et al."（英文）
- 刊名：中文刊名不斜体；英文刊名斜体
- DOI格式：`https://doi.org/10.xxxx/xxxxx`

**示例（中文）：**
```
朱明, 张华伟, 李婷. 活性炭对水溶液中亚甲基蓝的吸附动力学研究[J].
环境科学学报, 2021, 41(8): 3012-3020.
https://doi.org/10.13671/j.hjkxxb.2021.0231
```

**示例（英文）：**
```
Ho Y S, McKay G. Pseudo-second order model for sorption processes[J].
Process Biochemistry, 1999, 34(5): 451-465.
https://doi.org/10.1016/S0032-9592(98)00112-5
```

### 专著/教材 [M]
```
作者. 书名[M]. 版次. 出版地: 出版社, 年份: 起止页码.
```
- 第1版可省略版次
- 如引用特定章节，须标注页码

**示例：**
```
朱文涛. 物理化学[M]. 4版. 北京: 清华大学出版社, 2019: 156-162.

Atkins P, de Paula J, Keeler J. Physical Chemistry[M]. 11th ed.
Oxford: Oxford University Press, 2018: 634-639.
```

### 标准文献 [S]
```
标准代号. 标准名称[S]. 发布机构, 年份.
```
- 标准代号包含年份时，正文和列表保持一致
- 可附标准官网链接

**示例：**
```
GB/T 7714-2015. 信息与文献 参考文献著录规则[S]. 中国国家标准化管理委员会, 2015.
https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D8055ED3A7E05397BE0A0AB82A

GB 8978-1996. 污水综合排放标准[S]. 国家环境保护局, 1996.
https://www.mee.gov.cn/ywgz/fgbz/bz/bzwb/shjbh/swrwpfbz/199801/t19980101_66568.shtml
```

### 学位论文 [D]
```
作者. 题名[D]. 授予单位所在城市: 授予单位, 年份.
```

**示例：**
```
王磊. 纳米TiO₂光催化降解有机污染物机理研究[D]. 北京: 北京大学, 2020.
https://kns.cnki.net/kcms/detail/xxxxx
```

### 网络资源 [EB/OL]
```
作者/机构. 题名[EB/OL]. (发布/更新日期)[引用日期]. URL.
```

**示例：**
```
National Institute of Standards and Technology.
NIST Chemistry WebBook: Methanol[EB/OL]. (2023-05-10)[2024-03-15].
https://webbook.nist.gov/cgi/cbook.cgi?ID=67-56-1
```

---

## 三、正文内引用规则

### 行文中的引用标注

```html
<!-- 单文献引用 -->
该反应遵循准二阶动力学模型<sup><a href="#ref-1">[1]</a></sup>。

<!-- 多文献同引 -->
吸附过程常用Langmuir和Freundlich等温线描述<sup><a href="#ref-2">[2]</a><a href="#ref-3">[3]</a></sup>。

<!-- 作者姓名入文 -->
Ho和McKay<sup><a href="#ref-1">[1]</a></sup>提出了准二阶动力学模型。
```

### 编号规则
- 按正文中首次出现顺序排列（1, 2, 3…）
- 同一文献多次引用，编号不变
- 参考文献列表与正文编号严格对应

---

## 四、HTML参考文献节完整模板

```html
<section id="references" class="references">
  <h2>参考文献</h2>
  <ol>
    <li id="ref-1">
      Ho Y S, McKay G. Pseudo-second order model for sorption processes[J].
      <em>Process Biochemistry</em>, 1999, 34(5): 451-465.
      <a href="https://doi.org/10.1016/S0032-9592(98)00112-5" target="_blank">
        https://doi.org/10.1016/S0032-9592(98)00112-5
      </a>
    </li>
    <li id="ref-2">
      朱明, 张华伟, 李婷. 活性炭对水溶液中亚甲基蓝的吸附动力学研究[J].
      环境科学学报, 2021, 41(8): 3012-3020.
      <a href="https://doi.org/10.13671/j.hjkxxb.2021.0231" target="_blank">
        https://doi.org/10.13671/j.hjkxxb.2021.0231
      </a>
    </li>
    <li id="ref-3">
      朱文涛. 物理化学[M]. 4版. 北京: 清华大学出版社, 2019: 156-162.
    </li>
    <li id="ref-4">
      GB/T 7714-2015. 信息与文献 参考文献著录规则[S].
      中国国家标准化管理委员会, 2015.
      <a href="https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D8055ED3A7E05397BE0A0AB82A" target="_blank">
        https://std.samr.gov.cn/...
      </a>
    </li>
  </ol>
</section>
```

---

## 五、搜索策略速查

### 按实验类型推荐搜索入口

| 实验类型 | 优先搜索入口 | 搜索关键词示例 |
|----------|-------------|---------------|
| 化学/化工 | CNKI + ACS Publications | `[反应名] kinetics mechanism` |
| 物理 | AIP / APS / Web of Science | `[物理现象] experimental study` |
| 生物/生化 | PubMed + 中国知网 | `[酶名] activity assay protocol` |
| 环境工程 | CNKI + ScienceDirect | `[污染物] removal efficiency` |
| 材料科学 | Elsevier + Web of Science | `[材料] characterization XRD SEM` |
| 电学/电子 | IEEE Xplore | `[器件] performance measurement` |
| 水处理 | CNKI + Water Research | `[工艺] wastewater treatment` |
| 标准方法 | std.samr.gov.cn / iso.org | `GB/T [方法名]` |

### 搜索URL模板

```
CNKI:        https://www.cnki.net/  → 高级搜索 → 主题词
Google Scholar: https://scholar.google.com/scholar?q=[关键词]
PubMed:      https://pubmed.ncbi.nlm.nih.gov/?term=[关键词]
国家标准全文: https://std.samr.gov.cn/gb/search/gbQueryPage
ACS:         https://pubs.acs.org/action/doSearch?query=[关键词]
ScienceDirect: https://www.sciencedirect.com/search?query=[关键词]
```

---

## 六、常见错误对照

| 错误写法 | 正确写法 |
|---------|---------|
| 张三等人[1]指出… | 张三等<sup>[1]</sup>指出… |
| [参考文献1] | <sup><a href="#ref-1">[1]</a></sup> |
| DOI: 10.xxxx | https://doi.org/10.xxxx |
| 刊名不标斜体（英文） | *Journal Name*（英文刊名斜体） |
| 缺少卷/期/页码 | 期刊论文必须有卷(期):页码 |
| 网址无访问日期（EB/OL） | 必须注明[引用日期] |
| 虚构文献信息 | 找不到就不引，不可编造 |
