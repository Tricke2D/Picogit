"""
CLI entry point for Mini Git.
"""

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Mini Git - Version Control Internals",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  minigit init
  minigit add file.txt
  minigit status
  minigit commit -m "message" --author "name"
  minigit branch
  minigit branch feature
  minigit checkout main
  minigit merge feature
  minigit diff file.txt
  minigit log
  minigit hash-object file.txt
  minigit cat-file <hash>
  minigit ls-tree <tree-hash>
"""
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # ============================================================
    # init command
    # ============================================================
    subparsers.add_parser("init", help="Initialize a new repository")

    # ============================================================
    # add command (WEEK 5)
    # ============================================================
    add_parser = subparsers.add_parser("add", help="Add file to staging area")
    add_parser.add_argument("file", help="File to add")

    # ============================================================
    # status command (WEEK 5)
    # ============================================================
    subparsers.add_parser("status", help="Show working tree status")

    # ============================================================
    # commit command
    # ============================================================
    commit_parser = subparsers.add_parser("commit", help="Create a commit")
    commit_parser.add_argument("-m", "--message", required=True, help="Commit message")
    commit_parser.add_argument("--author", default="unknown", help="Author name")

    # ============================================================
    # branch command (WEEK 6)
    # ============================================================
    branch_parser = subparsers.add_parser("branch", help="List or create branches")
    branch_parser.add_argument("name", nargs="?", help="Branch name to create (optional)")

    # ============================================================
    # checkout command (WEEK 7)
    # ============================================================
    checkout_parser = subparsers.add_parser("checkout", help="Switch to a branch")
    checkout_parser.add_argument("ref", help="Branch name to checkout")

    # ============================================================
    # merge command (WEEK 10)
    # ============================================================
    merge_parser = subparsers.add_parser("merge", help="Merge a branch into current branch")
    merge_parser.add_argument("branch", help="Branch to merge")
    merge_parser.add_argument("--author", default="unknown", help="Author for merge commit")

    # ============================================================
    # diff command (WEEK 8)
    # ============================================================
    diff_parser = subparsers.add_parser("diff", help="Show differences between staged and working file")
    diff_parser.add_argument("file", help="File to diff")

    # ============================================================
    # log command
    # ============================================================
    subparsers.add_parser("log", help="Show commit history")

    # ============================================================
    # hash-object command
    # ============================================================
    hash_parser = subparsers.add_parser("hash-object", help="Compute object hash and store")
    hash_parser.add_argument("file", help="File to hash")

    # ============================================================
    # cat-file command
    # ============================================================
    cat_parser = subparsers.add_parser("cat-file", help="Display object content")
    cat_parser.add_argument("hash", help="Object hash to display")

    # ============================================================
    # ls-tree command
    # ============================================================
    ls_parser = subparsers.add_parser("ls-tree", help="List tree contents")
    ls_parser.add_argument("hash", help="Tree hash to list")
    ls_parser.add_argument("-r", "--recursive", action="store_true", help="Recursively list subtrees")

    args = parser.parse_args()

    # ============================================================
    # Dispatch commands
    # ============================================================

    if args.command == "init":
        from minigit.cli.commands.init_cmd import run_init
        run_init()

    elif args.command == "add":
        from minigit.cli.commands.add_cmd import run_add
        try:
            run_add(args.file)
        except RuntimeError as e:
            print(f"Error: {e}")
        except FileNotFoundError as e:
            print(f"Error: {e}")

    elif args.command == "status":
        from minigit.cli.commands.status_cmd import run_status
        try:
            run_status()
        except RuntimeError as e:
            print(f"Error: {e}")

    elif args.command == "commit":
        from minigit.cli.commands.commit_cmd import run_commit
        try:
            commit_hash = run_commit(args.message, args.author)
            print(f"[{args.author}] commit {commit_hash}")
            print(f"  {args.message}")
        except ValueError as e:
            print(f"Error: {e}")
        except RuntimeError as e:
            print(f"Error: {e}")

    elif args.command == "branch":
        from minigit.cli.commands.branch_cmd import run_branch
        try:
            result = run_branch(args.name)
            if result is not None:
                # List branches
                active_branch = None
                try:
                    from minigit.core.repository import Repository
                    repo = Repository(working_dir=Path.cwd())
                    if repo.is_initialized():
                        active_branch = repo.get_active_branch()
                except:
                    pass
                for branch in result:
                    marker = "* " if branch == active_branch else "  "
                    print(f"{marker}{branch}")
        except RuntimeError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "checkout":
        from minigit.cli.commands.checkout_cmd import run_checkout
        try:
            run_checkout(args.ref)
        except RuntimeError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "merge":
        from minigit.cli.commands.merge_cmd import run_merge
        try:
            commit_hash = run_merge(args.branch, args.author)
            print(f"Merge successful! Commit: {commit_hash}")
        except RuntimeError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "diff":
        from minigit.cli.commands.diff_cmd import run_diff
        try:
            output = run_diff(args.file)
            print(output)
        except RuntimeError as e:
            print(f"Error: {e}")
        except FileNotFoundError as e:
            print(f"Error: {e}")

    elif args.command == "log":
        from minigit.cli.commands.log_cmd import run_log
        try:
            print(run_log())
        except RuntimeError as e:
            print(f"Error: {e}")

    elif args.command == "hash-object":
        from minigit.cli.commands.hash_object_cmd import run_hash_object
        try:
            hash_val = run_hash_object(args.file)
            print(hash_val)
        except RuntimeError as e:
            print(f"Error: {e}")

    elif args.command == "cat-file":
        from minigit.cli.commands.cat_file_cmd import run_cat_file
        try:
            content = run_cat_file(args.hash)
            print(content.decode("utf-8", errors="replace"))
        except FileNotFoundError as e:
            print(f"Error: {e}")

    elif args.command == "ls-tree":
        from minigit.cli.commands.ls_tree_cmd import run_ls_tree
        try:
            run_ls_tree(args.hash, recursive=args.recursive)
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")

    else:
        parser.print_help()