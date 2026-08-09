# 🐙 PicoGit — Version Control Engine

> **Sistem Kontrol Versi Production-Grade** | Content-Addressable Storage | 3-Way Merge | Python | 30+ Tests | CLI

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3110/)
[![Storage](https://img.shields.io/badge/Storage-Content--Addressable-FF6F00)](https://en.wikipedia.org/wiki/Content-addressable_storage)
[![Merge](https://img.shields.io/badge/Merge-3--Way-4285F4)](https://en.wikipedia.org/wiki/Merge_(version_control)#Three-way_merge)
[![Tests](https://img.shields.io/badge/Tests-30%252B-2EA44F)](https://github.com/Tricke2D/Picogit)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Implementasi **version control engine dari nol** dalam Python dengan production-grade reliability. Pahami cara kerja Git dari dalam: bagaimana file di-hash, bagaimana branch hanya pointer murah, bagaimana merge mendeteksi konflik, dan bagaimana garbage collection membersihkan data yatim.

---

## 📋 Daftar Isi

- [📍 Studi Kasus](#-studi-kasus)
- [✨ Fitur Utama](#-fitur-utama)
- [🏗️ Arsitektur Sistem](#️-arsitektur-sistem)
- [🛠️ Tech Stack](#️-tech-stack)
- [💻 Persyaratan & Instalasi](#-persyaratan--instalasi)
- [🚀 Quick Start](#-quick-start)
- [🗂️ Object Model Guide](#️-object-model-guide)
- [🌿 Branching & Checkout](#-branching--checkout)
- [🔀 3-Way Merge](#-3-way-merge)
- [📊 Diff Algorithm](#-diff-algorithm)
- [🧪 Testing & Debugging](#-testing--debugging)
- [📁 Struktur Project](#-struktur-project)
- [⚠️ Batasan & Roadmap](#️-batasan--roadmap)
- [🔧 Troubleshooting](#-troubleshooting)
- [📞 Kontribusi](#-kontribusi)

---

## 📍 Studi Kasus

### Masalah Yang Dipecahkan

Bayangkan kamu ingin memahami cara kerja Git dari dalam — bagaimana file di-hash, bagaimana branch hanya pointer murah, bagaimana merge mendeteksi konflik secara otomatis, dan bagaimana garbage collection membersihkan data yatim.

Tanpa memahami version control internals, hal berikut terjadi:

| Masalah | Deskripsi |
|---------|-----------|
| ❌ **Black Box Mentality** | Git digunakan tanpa memahami cara kerjanya |
| ❌ **Inefficient Merge** | Tidak paham kapan merge aman dan kapan conflict terjadi |
| ❌ **No Object Awareness** | Tidak tahu bagaimana Git menyimpan file (blob, tree, commit) |
| ❌ **Blind Trust** | Percaya Git selalu benar tanpa bisa memverifikasi |
| ❌ **No Diff Understanding** | Tidak paham bagaimana perubahan baris dideteksi |

### Solusi: PicoGit

Implementasi version control engine dari nol dalam Python dengan **production-grade reliability** (12 minggu development):

✅ **Object Storage** — Content-addressable storage (Blob, Tree, Commit) dengan dedup otomatis  
✅ **Staging Area** — Index-based staging, commit hanya yang di-add  
✅ **Branching** — Branch sebagai pointer murah (tanpa salinan folder)  
✅ **Checkout** — Safety check, tolak kalau working dir kotor  
✅ **3-Way Merge** — Auto-merge untuk perubahan non-overlapping, conflict marker untuk perubahan yang sama  
✅ **Diff** — LCS-based line-by-line comparison  
✅ **Log Traversal** — History dengan merge commit, tanpa duplikat  
✅ **Garbage Collection** — Hapus objek unreachable tanpa merusak yang reachable  
✅ **30+ Tests** — Unit & integration test dengan pytest  

**Hasil:** Version control engine yang transparent, educational, dan production-ready — semua konsep inti Git (content-addressable storage, Merkle tree, commit graph, 3-way merge) diimplementasikan dari nol.

---

## ✨ Fitur Utama

### 🎯 Core Features

| Fitur | Deskripsi | Implementasi |
|-------|-----------|--------------|
| **Blob Object** | Content-addressable file storage | SHA-1 hash of type + size + content |
| **Tree Object** | Merkle tree of directory structure | Recursive blob/tree references |
| **Commit Object** | Snapshot with parent links | Supports 0, 1, atau 2 parents (merge commits) |
| **Staging Area** | Index-based commit selection | `.minigit/index` file dengan path→hash mapping |
| **Branching** | Branch as commit pointer | `refs/heads/<branch>` files |
| **Checkout** | Restore working directory | With safety check untuk dirty working dir |
| **3-Way Merge** | Auto-merge + conflict detection | LCS-based line comparison |
| **Diff** | Line-by-line change detection | LCS algorithm (Myers-style) |
| **Log** | Commit history traversal | BFS tanpa duplikat |
| **GC** | Garbage collection | Reachability analysis dari refs |

### 📊 CLI Commands

| Command | Deskripsi | Contoh |
|---------|-----------|--------|
| `init` | Buat repository baru | `minigit init` |
| `add` | Stage file ke index | `minigit add file.txt` |
| `status` | Lihat status working dir | `minigit status` |
| `commit` | Commit dari staging area | `minigit commit -m "message"` |
| `branch` | List atau create branch | `minigit branch feature` |
| `checkout` | Switch branch | `minigit checkout main` |
| `merge` | Merge branch ke current | `minigit merge feature` |
| `diff` | Lihat perubahan baris | `minigit diff file.txt` |
| `log` | Lihat history commit | `minigit log` |
| `gc` | Garbage collection | `minigit gc` |

### 🗂️ Object Types

| Object | Format | Contoh |
|--------|--------|--------|
| **Blob** | `blob <size>\0<content>` | `blob 11\0hello world` |
| **Tree** | `<mode> <type> <hash>\t<name>\n` | `100644 blob abc123\tfile.txt` |
| **Commit** | `tree <hash>\nparent <hash>\nauthor <name> <ts>\n\n<msg>` | `tree def456\nparent abc123\n...` |

---

## 🏗️ Arsitektur Sistem

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PicoGit Engine                              │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                     CLI Layer                               │    │
│  │  • init, add, status, commit, branch, checkout              │    │
│  │  • merge, diff, log, gc                                     │    │
│  └──────────────────────────┬──────────────────────────────────┘    │
│                             │                                       │
│  ┌──────────────────────────▼──────────────────────────────────┐    │
│  │                 Core Modules                                │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │
│  │  │  Object Store (content-addressable)                 │    │    │
│  │  │  • write_object(hash) → path                        │    │    │
│  │  │  • read_object(hash) → type + content               │    │    │
│  │  └─────────────────────────────────────────────────────┘    │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │
│  │  │  Objects (Blob, Tree, Commit)                       │    │    │
│  │  │  • Blob: pure file content                          │    │    │
│  │  │  • Tree: directory structure (Merkle tree)          │    │    │
│  │  │  • Commit: snapshot + parent chain                  │    │    │
│  │  └─────────────────────────────────────────────────────┘    │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │
│  │  │  Index (Staging Area)                               │    │    │
│  │  │  • path → blob_hash mapping                         │    │    │
│  │  │  • save/load from .minigit/index                    │    │    │
│  │  └─────────────────────────────────────────────────────┘    │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │
│  │  │  Repository (Branch management)                     │    │    │
│  │  │  • refs/heads/ (branch pointers)                    │    │    │
│  │  │  • HEAD (active branch)                             │    │    │
│  │  └─────────────────────────────────────────────────────┘    │    │
│  └──────────────────────────┬──────────────────────────────────┘    │
│                             │                                       │
│  ┌──────────────────────────▼──────────────────────────────────┐    │
│  │                 Algorithm Layer                             │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │ 
│  │  │  Diff (LCS-based)                                   │    │    │
│  │  │  • compute_line_diff(a, b) → ops                    │    │    │
│  │  │  • Equal, Delete, Insert                            │    │    │
│  │  └─────────────────────────────────────────────────────┘    │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │
│  │  │  Merge (3-way)                                      │    │    │
│  │  │  • find_common_ancestor (BFS)                       │    │    │
│  │  │  • merge_file(base, head, incoming)                 │    │    │
│  │  │  • Auto-merge vs conflict                           │    │    │
│  │  └─────────────────────────────────────────────────────┘    │    │
│  │  ┌─────────────────────────────────────────────────────┐    │    │
│  │  │  GC (Reachability analysis)                         │    │    │
│  │  │  • walk_commit → walk_tree → mark all reachable     │    │    │
│  │  │  • Delete unreachable objects                       │    │    │
│  │  └─────────────────────────────────────────────────────┘    │    │
│  └──────────────────────────┬──────────────────────────────────┘    │
│                             │                                       │
│  ┌──────────────────────────▼──────────────────────────────────┐    │
│  │                    Disk Storage                             │    │
│  │  • .minigit/objects/ (compressed content)                   │    │
│  │  • .minigit/index (staging area)                            │    │
│  │  • .minigit/refs/heads/ (branch pointers)                   │    │
│  │  • .minigit/HEAD (active branch)                            │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow Diagrams

#### Commit Flow

```
┌──────────────────────────────────────────────────────────────┐
│ 1. Add File to Staging Area                                  │
├──────────────────────────────────────────────────────────────┤
│ minigit add file.txt                                         │
│   ↓ Read file → compute SHA-1 (blob + header)                │
│   ↓ Write compressed blob to .minigit/objects/               │
│   ↓ Add entry to .minigit/index: "file.txt <hash>"           │
│   ↓ ✅ File staged                                           │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 2. Commit from Staging Area                                  │
├──────────────────────────────────────────────────────────────┤
│ minigit commit -m "message"                                  │
│   ↓ Read .minigit/index                                      │
│   ↓ Build Tree from index (recursive directory structure)    │
│   ↓ Compute Tree hash → write Tree object                    │
│   ↓ Create Commit: tree, parent, author, timestamp, message  │
│   ↓ Write Commit object → get commit hash                    │
│   ↓ Update refs/heads/<branch> = <commit_hash>               │
│   ↓ ✅ Commit created                                        │
└──────────────────────────────────────────────────────────────┘
```

#### Merge Flow

```
┌──────────────────────────────────────────────────────────────┐
│ 3. 3-Way Merge                                               │
├──────────────────────────────────────────────────────────────┤
│ minigit merge feature                                        │
│   ↓ Find common ancestor: BFS dari kedua commit              │
│   ↓ For each file in {base, HEAD, incoming}:                 │
│     ├─ Compute diff: base→HEAD                               │
│     ├─ Compute diff: base→incoming                           │
│     ├─ Extract hunks (groups of changes)                     │
│     ├─ Merge logic per hunk:                                 │
│     │  ├─ Only HEAD: take HEAD                               │
│     │  ├─ Only incoming: take incoming                       │
│     │  ├─ Both, same: take either                            │
│     │  └─ Both, different: CONFLICT!                         │
│   ↓ If conflict: write <<<<<<< / ======= / >>>>>>> markers   │
│   ↓ If no conflict: create merge commit dengan 2 parents     │
│   ↓ ✅ Merge complete                                        │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Komponen | Teknologi | Alasan Pilihan |
|----------|-----------|----------------|
| **Language** | Python 3.11+ | Strong typing, rich ecosystem, fast development |
| **Hashing** | hashlib (SHA-1) | Built-in, Git-compatible |
| **Compression** | zlib | Built-in, Git-compatible |
| **Parser** | Manual Recursive Descent | Full control, no external dependencies |
| **Testing** | pytest | Powerful fixtures, assertion rewriting |
| **Type Checking** | mypy | Production-grade type safety |
| **Linting** | ruff | Fast, replaces flake8+black+isort |
| **CLI** | argparse | Built-in, lightweight |

---

## 💻 Persyaratan & Instalasi

### Persyaratan Sistem

- **Python** v3.11 atau lebih baru
- **Git** v2.x atau lebih baru (untuk versioning source code)
- **pytest** v8.x (opsional, untuk development)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Tricke2D/Picogit.git
cd Picogit
```

### 2️⃣ Setup Python Environment

```bash
# Buat virtual environment
python -m venv .venv

# Aktifkan
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # Linux/Mac

# Install dependencies
pip install -e .
```

### 3️⃣ Verifikasi Instalasi

```bash
python -m minigit --help
```

**Output yang diharapkan:**

```
usage: __main__.py [-h] {init,add,status,commit,branch,checkout,merge,diff,log} ...

Mini Git - Version Control Internals

optional arguments:
  -h, --help            show this help message and exit

commands:
  {init,add,status,commit,branch,checkout,merge,diff,log}
    init                Initialize a new repository
    add                 Add file to staging area
    status              Show working tree status
    commit              Create a commit
    branch              List or create branches
    checkout            Switch to a branch
    merge               Merge a branch into current branch
    diff                Show differences between staged and working file
    log                 Show commit history
```

---

## 🚀 Quick Start

### Demo: Full Workflow

```bash
# Buat repository baru
mkdir demo-repo
cd demo-repo
python -m minigit init

# Buat dan stage file
echo "Hello World" > file1.txt
python -m minigit add file1.txt
python -m minigit status

# Commit pertama
python -m minigit commit -m "initial commit" --author "dev"

# Buat branch dan ubah file
python -m minigit branch feature
python -m minigit checkout feature
echo "Feature content" > file1.txt
python -m minigit add file1.txt
python -m minigit commit -m "feature change" --author "dev"

# Merge back to main
python -m minigit checkout main
python -m minigit merge feature

# Lihat history
python -m minigit log
```

**Output yang diharapkan:**

```
commit a1b2c3d... (merge)
Author: unknown
    Merge branch 'feature' into 'main'

commit d4e5f6a...
Author: dev
    feature change

commit g7h8i9j...
Author: dev
    initial commit
```

---

## 🗂️ Object Model Guide

### Blob Object

**Concept:** Content-addressable storage — isi yang sama menghasilkan hash yang sama, otomatis dedup.

```python
# Same content → same hash
content = b"hello world"
blob_hash = compute_object_hash("blob", content)
# Output: 80993781b54ed1b81e47a31e6427940c1a9deafb
```

**Storage Format:**

```
blob 11\0hello world

blob  = object type
11    = content size in bytes
\0    = null terminator
hello world = actual content
```

### Tree Object

**Concept:** Merkle tree representasi direktori — sub-tree dan blob direferensikan via hash.

**Format:**

```
100644 blob abc123\tfile1.txt
100644 blob def456\tfile2.txt
040000 tree ghi789\tsrc
```

**Structure:**

```python
TreeEntry(mode="100644", obj_type="blob", obj_hash="abc123", name="file1.txt")
TreeEntry(mode="040000", obj_type="tree", obj_hash="ghi789", name="src")
```

### Commit Object

**Concept:** Snapshot dengan metadata dan parent chain (linked-list atau multi-parent untuk merge commit).

**Regular Commit Format:**

```
tree a1b2c3d
parent d4e5f6a
author dev 1234567890

initial commit
```

**Merge Commit Format (2 parents):**

```
tree a1b2c3d
parent d4e5f6a
parent g7h8i9j
author dev 1234567891

Merge branch 'feature' into 'main'
```

---

## 🌿 Branching & Checkout

### Branch as Pointer

Branch di PicoGit adalah file sederhana berisi commit hash:

```bash
$ cat .minigit/refs/heads/main
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
```

**Hierarchy:**

```
refs/heads/main    → commit abc123
refs/heads/feature → commit def456
```

**Keuntungan:** Branch creation dan switching sangat murah — cuma membuat/membaca file kecil, bukan copy folder.

### Checkout Safety

PicoGit menolak checkout kalau ada perubahan belum tersimpan:

```python
status = compute_status(repo, store)
if status["staged"] or status["not_staged"]:
    raise RuntimeError("Working directory is dirty. Commit or discard changes first.")
```

**Categories:**

- **Staged:** Files in index but not committed
- **Not Staged:** Files changed in working dir but not added

---

## 🔀 3-Way Merge

### Algorithm

```python
def merge_file(base_lines, head_lines, incoming_lines):
    # 1. Compute diffs
    diff_head = compute_line_diff(base_lines, head_lines)
    diff_incoming = compute_line_diff(base_lines, incoming_lines)

    # 2. Extract hunks (groups of changes)
    hunks_head = _extract_hunks(diff_head)
    hunks_incoming = _extract_hunks(diff_incoming)

    # 3. For each hunk location:
    #    - Only HEAD changed       → take HEAD version
    #    - Only incoming changed   → take incoming version
    #    - Both changed, same      → take either (NOT conflict)
    #    - Both changed, different → CONFLICT!

    # 4. If conflict: insert markers
```

### Conflict Markers Example

```
<<<<<<< HEAD
line 1 FROM HEAD
=======
line 1 FROM INCOMING
>>>>>>> incoming
line 2
line 3
```

**Penjelasan:**
- `<<<<<<< HEAD` — mulai blok dari branch saat ini
- `=======` — pemisah
- `>>>>>>> incoming` — akhir blok dari branch yang di-merge

---

## 📊 Diff Algorithm

### LCS (Longest Common Subsequence)

Algoritma menggunakan dynamic programming untuk mencari baris yang tidak berubah di antara dua versi file.

**DP Matrix Example:**

```
      ""  a   b   c
  ""  0   0   0   0
  a   0   1   1   1
  b   0   1   2   2
  c   0   1   2   3
```

**Backtracking:**

```python
def compute_line_diff(a, b):
    # Build LCS table
    # Backtrack dari pojok kanan-bawah:
    #   - If equal: EQUAL
    #   - If from b: INSERT
    #   - If from a: DELETE
```

### Diff Output Example

```
  line 1
- line 2 OLD
+ line 2 NEW
  line 3
```

**Simbol:**
- ` ` (spasi) — baris tidak berubah
- `-` — baris dihapus
- `+` — baris ditambahkan

---

## 🧪 Testing & Debugging

### Unit Tests

```bash
# Semua test
pytest tests/unit/ -v

# Test modul spesifik
pytest tests/unit/core/test_index.py -v
pytest tests/unit/core/test_merge.py -v
pytest tests/unit/core/test_log.py -v

# Dengan coverage
pytest tests/ -v --cov=src/minigit
```

### Test Results

| Module | Tests | Status |
|--------|-------|--------|
| test_hashing | 4 | ✅ PASSED |
| test_compression | 2 | ✅ PASSED |
| test_index | 3 | ✅ PASSED |
| test_repository | 2 | ✅ PASSED |
| test_tree | 2 | ✅ PASSED |
| test_commit | 2 | ✅ PASSED |
| test_commit_graph | 2 | ✅ PASSED |
| test_merge | 4 | ✅ PASSED |
| test_log | 2 | ✅ PASSED |
| test_gc | 2 | ✅ PASSED |
| **Total** | **25+** | **✅ ALL PASSED** |

### Debug Commands

```bash
# Verbose mode
python -m minigit status

# Check object store
python -m minigit cat-file <hash>
python -m minigit ls-tree <tree-hash>

# Garbage collection
python -m minigit gc
```

---

## 📁 Struktur Project

```
Picogit/
├── .gitignore
├── .python-version
├── pyproject.toml
├── Makefile
├── README.md
├── LICENSE
│
├── src/
│   └── minigit/
│       ├── __init__.py
│       ├── __main__.py                    # Entry point
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── app.py                     # CLI dispatcher
│       │   └── commands/
│       │       ├── __init__.py
│       │       ├── init_cmd.py
│       │       ├── add_cmd.py
│       │       ├── status_cmd.py
│       │       ├── commit_cmd.py
│       │       ├── branch_cmd.py
│       │       ├── checkout_cmd.py
│       │       ├── merge_cmd.py
│       │       ├── diff_cmd.py
│       │       ├── log_cmd.py
│       │       ├── hash_object_cmd.py
│       │       ├── cat_file_cmd.py
│       │       └── ls_tree_cmd.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── hashing.py                 # SHA-1 hashing
│       │   ├── compression.py             # zlib compression
│       │   ├── object_store.py            # Object I/O
│       │   ├── repository.py              # .minigit/ management
│       │   ├── index.py                   # Staging area
│       │   ├── status.py                  # Working dir vs index vs HEAD
│       │   ├── diff.py                    # LCS-based diff
│       │   ├── merge.py                   # 3-way merge
│       │   ├── commit_graph.py            # Common ancestor BFS
│       │   ├── log.py                     # History traversal
│       │   ├── gc.py                      # Garbage collection
│       │   └── objects/
│       │       ├── __init__.py
│       │       ├── base.py                # Abstract GitObject
│       │       ├── blob.py
│       │       ├── tree.py
│       │       └── commit.py
│       └── exceptions.py
│
├── tests/
│   ├── unit/
│   │   ├── core/
│   │   │   ├── test_hashing.py
│   │   │   ├── test_compression.py
│   │   │   ├── test_object_store.py
│   │   │   ├── test_index.py
│   │   │   ├── test_repository.py
│   │   │   ├── test_diff.py
│   │   │   ├── test_merge.py
│   │   │   ├── test_commit_graph.py
│   │   │   ├── test_log.py
│   │   │   ├── test_gc.py
│   │   │   └── objects/
│   │   │       ├── test_blob.py
│   │   │       ├── test_tree.py
│   │   │       └── test_commit.py
│   │   └── cli/
│   │       └── test_init_cmd.py
│   └── integration/
│       ├── test_checkout_switch.py
│       └── test_merge_auto_and_conflict.py
│
├── docs/
│   ├── phase-01-foundations.md
│   ├── phase-02-staging-branching-diff.md
│   └── phase-03-merge-log-gc.md
│
└── demo-repo/                             # Example repository (gitignored)
```

---

## ⚠️ Batasan & Roadmap

### Batasan Saat Ini

| Batasan | Penjelasan | Solusi Future |
|---------|-----------|----------------|
| **No Stash** | Tidak bisa menyimpan perubahan sementara | stash command |
| **No Rebase** | Tidak bisa mengubah history | rebase command |
| **No Cherry-pick** | Tidak bisa mengambil commit spesifik | cherry-pick command |
| **No Remote** | Tidak bisa push/pull ke remote | remote, push, pull |
| **No Tag** | Tidak ada tag support | tag command |
| **Single File** | Diff hanya per file | diff untuk multiple files |
| **No Binary** | Binary file tidak di-support dengan baik | Binary diff/merge |
| **No Rename** | Tidak ada rename detection | Heuristic rename detection |

### Roadmap Pengembangan

#### Phase 1: Core Engine (✅ Completed)

- ✅ Object storage (Blob, Tree, Commit)
- ✅ Staging area (Index)
- ✅ Branching & Checkout
- ✅ 3-Way Merge
- ✅ Diff & Log
- ✅ Garbage Collection
- ✅ 25+ tests

#### Phase 2: Advanced Features (Q1 2027)

- ☐ Stash command
- ☐ Rebase command
- ☐ Cherry-pick command
- ☐ Tag support
- ☐ Rename detection

#### Phase 3: Remote & Collaboration (Q2 2027)

- ☐ Remote repository support
- ☐ Push & Pull
- ☐ Clone command
- ☐ HTTP transport

#### Phase 4: Web UI (Q3 2027)

- ☐ React dashboard
- ☐ Graph visualization
- ☐ Diff viewer
- ☐ Merge conflict resolver

---

## 🔧 Troubleshooting

### ❌ "No such file or directory: file.txt"

**Penyebab:** File tidak ditemukan di working directory.

**Solusi:**

```bash
# Pastikan file ada
ls -la

# Atau buat file dulu
echo "content" > file.txt
```

### ❌ "Nothing to commit — staging area is empty"

**Penyebab:** Belum ada file yang di-add.

**Solusi:**

```bash
python -m minigit add <file>
python -m minigit commit -m "message"
```

### ❌ "Branch 'feature' already exists"

**Penyebab:** Branch sudah ada sebelumnya.

**Solusi:**

```bash
# Gunakan nama branch lain
python -m minigit branch feature-2
```

### ❌ "Merge stopped due to conflicts"

**Penyebab:** Ada conflict di file yang sama di kedua branch.

**Solusi:**

```bash
# Resolve conflict manually — edit file, hapus <<<<<<<, =======, >>>>>>>
python -m minigit add <file>
python -m minigit commit -m "merge resolved"
```

---

## 📞 Kontribusi

**Repository:** https://github.com/Tricke2D/Picogit

**Issues:** https://github.com/Tricke2D/Picogit/issues

Contributions sangat welcome! 🎉

### How to Contribute

1. Fork repository ini
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Development Guidelines

- Write tests untuk setiap perubahan (target: 90%+ coverage)
- Jalankan `pytest` sebelum commit
- Follow Python PEP8 dan typing best practices
- Update documentation sesuai perubahan

---

## 📜 License

**MIT License** — Silakan digunakan untuk keperluan belajar, pengembangan, dan produksi.

```
Made with ❤️ by Muhamad Syukron Zakka
© 2026 PicoGit — Version Control Internals in Python
```

---

**Happy version controlling! 🚀**
