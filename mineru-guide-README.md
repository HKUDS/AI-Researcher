# PDF 转换 Markdown 及行号清理中文指南

本指南详细介绍了将 PDF 文件转换为 Markdown 格式，并随后清理转换过程中可能引入的多余行号的完整工作流程。

## 1. 问题描述

当使用 `mineru` 工具转换特定的 PDF 文件（尤其是格式化的学术论文）时，其光学字符识别（OCR）过程可能会错误地将排版中的行号或页码识别为正文内容。这会导致生成的 Markdown 文件中，在许多行的开头甚至标题中，都混杂着无关的数字，影响了文档的可读性和后续处理。

本项目记录了针对 `2_19093_UniDomain_Pretraining_a_ (1).pdf` 文件进行问题诊断和解决的全过程。

## 2. 环境与工具准备

- **Conda 环境**: 建议在专门的 Conda 环境中进行操作，以有效管理项目依赖。
- **Mineru**: 用于执行初始 PDF 到 Markdown 转换的核心库。
  ```bash
  pip install mineru
  ```

## 3. 完整工作流程

以下是从环境设置到生成最终纯净 Markdown 文件的详细步骤。

### 第一步：激活 Conda 环境

首先，激活您安装了所需工具的 Conda 环境。请将 `your_env_name` 替换为您环境的实际名称。

```bash
conda activate mineru-pdf
```

### 第二步：执行 PDF 到 Markdown 的初始转换

将您的源 PDF 文件放入一个指定的目录（例如 `pdf-files/`）。然后运行 `mineru` 命令进行转换，并用 `-o` 参数指定输出目录（例如 `md-files/`）。

```bash
mineru -p pdf-files/ -o md-files
```

完成此步骤后，您可能会发现部分生成的 Markdown 文件（例如 `md-files/unidomaninPretraining/auto/unidomaninPretraining.md`）中包含了我们不希望出现的多余行号。

### 第三步：使用脚本清理多余行号

为了解决上述问题，我们开发了 `remove_line_numbers_final.py` 脚本。这个 Python 脚本能够智能地移除多余的行号和页码，同时完整保留 Markdown 标题（如 `# 1. 引言`）等合法编号。

**如何使用脚本：**

在终端中执行以下命令，将脚本指向需要清理的文件即可。

```bash
python remove_line_numbers_final.py "md-files/unidomaninPretraining/auto/unidomaninPretraining.md"
```

**推荐用法（创建备份）：**

为确保文件安全，强烈建议在使用时加上 `--backup` 标志。该标志会在执行清理前，自动创建一个原始文件的备份（例如 `unidomaninPretraining.md.backup`）。

```bash
python remove_line_numbers_final.py "md-files/unidomaninPretraining/auto/unidomaninPretraining.md" --backup
```

### 第四步：验证（可选）

运行脚本后，您可以检查文件以确认所有多余行号均已被移除。该脚本被设计为**幂等**的，这意味着您可以安全地对同一个文件重复运行它，而不会产生意外的副作用。

## 4. 关于 `remove_line_numbers_final.py` 脚本

该清理脚本经过了多次迭代和优化，形成了一个健壮的解决方案。其核心逻辑依赖于一系列精准的正则表达式，以应对各种复杂情况：

- **智能处理 Markdown 标题**: 脚本能够区分章节标题和普通文本，专门移除可能嵌入在标题中的页码（例如，`# 142 4.1 章节标题` 会被修正为 `# 4.1 章节标题`）。
- **清理普通文本行**: 移除所有非标题行行首的数字。
- **移除句中页码**: 清理可能出现在句子之间或数学表达式之前的页码。
- **灵活且安全**: 脚本提供了多个命令行参数，方便使用：
    - `input`: 需要处理的单个文件或整个目录的路径。
    - `--backup`: 在处理前创建原始文件的备份。
    - `--dry-run`: 预览将要发生的更改，但不会实际修改文件。
    - `-r, --recursive`: 递归处理一个目录下的所有 `.md` 文件。

这个经过优化的流程确保了最终能获得一个内容纯净、格式正确的 Markdown 文件，为后续的利用打下良好基础。 