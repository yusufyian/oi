# 题库索引（Question Bank Index）

本目录提供仓库内所有 PDF、DOC、DOCX 习题与试题材料的结构化索引，便于检索历年竞赛题目。

## 数据文件
- `index.json`：包含每个文档的基本信息。
- 生成脚本：`scripts/build_question_bank.py`。

## 字段说明
每条记录都包含以下键：

| 字段        | 说明                                                                   |
| ----------- | ---------------------------------------------------------------------- |
| `path`      | 文档相对仓库根目录的路径。                                             |
| `competition` | 顶层目录推断的赛事名称（如 `NOI`、`CSP-J`），若不存在则为空。           |
| `year`      | 路径中首次出现的年份（1980~2099），无法推断时为空。                     |
| `stage`     | 年份目录之后的子目录路径（如 `Round1`、`day1/task`），缺失则为空。       |
| `title`     | 依据文件名提取的标题（去除扩展名与常见分隔符）。                         |
| `format`    | 文件格式扩展名（`pdf`、`doc`、`docx`）。                                |

## 重新生成
在仓库根目录执行：

```bash
python scripts/build_question_bank.py
```

命令会扫描仓库下所有 PDF、DOC、DOCX 文件，更新 `index.json`。
