"""
Repository representation - .minigit/ directory structure.
"""

from pathlib import Path


class Repository:
    """Merepresentasikan satu repository Mini Git di disk."""

    MINIGIT_DIR = ".minigit"

    def __init__(self, working_dir: Path) -> None:
        self.working_dir = working_dir
        self.minigit_dir = working_dir / self.MINIGIT_DIR
        self.objects_dir = self.minigit_dir / "objects"
        self.refs_dir = self.minigit_dir / "refs" / "heads"
        self.head_file = self.minigit_dir / "HEAD"
        self.index_file = self.minigit_dir / "index"

    def initialize(self) -> None:
        """Membuat struktur folder awal sebuah repo baru."""
        self.objects_dir.mkdir(parents=True, exist_ok=True)
        self.refs_dir.mkdir(parents=True, exist_ok=True)
        self.head_file.write_text("ref: refs/heads/main\n")

    def is_initialized(self) -> bool:
        """Mengecek apakah folder saat ini sudah punya .minigit/."""
        return self.minigit_dir.exists()

    def get_active_branch(self) -> str:
        """
        Membaca HEAD, mengembalikan nama branch aktif (misal "main").
        
        Format HEAD: "ref: refs/heads/main" atau langsung hash commit (detached HEAD)
        """
        head_content = self.head_file.read_text().strip()
        if head_content.startswith("ref: "):
            ref_path = head_content.removeprefix("ref: ")
            # ref_path = "refs/heads/main" -> ambil "main"
            return ref_path.split("/")[-1]
        # Detached HEAD - return hash
        return head_content

    def get_branch_commit_hash(self, branch_name: str) -> str | None:
        """
        Membaca hash commit terakhir dari sebuah branch.
        Returns None jika branch belum punya commit.
        """
        ref_path = self.refs_dir / branch_name
        if not ref_path.exists():
            return None
        return ref_path.read_text().strip()

    def update_branch_ref(self, branch_name: str, commit_hash: str) -> None:
        """Menulis ulang pointer sebuah branch ke commit hash baru."""
        ref_path = self.refs_dir / branch_name
        ref_path.write_text(commit_hash + "\n")

    def get_head_commit_hash(self) -> str | None:
        """
        Mendapatkan hash commit yang sedang di-checkout (HEAD).
        Returns None jika HEAD belum punya commit.
        """
        head_content = self.head_file.read_text().strip()
        
        if head_content.startswith("ref: "):
            # HEAD points to branch -> read branch ref
            ref_path = head_content.removeprefix("ref: ").strip()
            full_path = self.minigit_dir / ref_path
            if full_path.exists():
                return full_path.read_text().strip()
            return None
        else:
            # Detached HEAD - direct commit hash
            return head_content

    def set_head(self, ref: str) -> None:
        """
        Mengatur HEAD ke branch atau commit hash.
        Format: "ref: refs/heads/main" untuk branch, atau langsung hash untuk detached.
        """
        if ref.startswith("refs/heads/"):
            self.head_file.write_text(f"ref: {ref}\n")
        elif len(ref) == 40 and all(c in "0123456789abcdef" for c in ref):
            # Detached HEAD
            self.head_file.write_text(ref + "\n")
        else:
            # Assume branch name
            self.head_file.write_text(f"ref: refs/heads/{ref}\n")

    def create_branch(self, branch_name: str) -> None:
        """
        Membuat branch baru menunjuk ke commit HEAD saat ini.
        """
        active_branch = self.get_active_branch()
        current_commit_hash = self.get_branch_commit_hash(active_branch)
        if current_commit_hash is None:
            raise ValueError("Tidak bisa membuat branch: belum ada commit sama sekali.")
        self.update_branch_ref(branch_name, current_commit_hash)

    def list_branches(self) -> list[str]:
        """
        Mengembalikan daftar semua nama branch yang ada di refs/heads/.
        """
        if not self.refs_dir.exists():
            return []
        return sorted(p.name for p in self.refs_dir.iterdir() if p.is_file())

    def switch_head_to_branch(self, branch_name: str) -> None:
        """
        Mengubah HEAD supaya menunjuk ke branch lain.
        """
        if branch_name not in self.list_branches():
            raise ValueError(f"Branch '{branch_name}' tidak ditemukan.")
        self.head_file.write_text(f"ref: refs/heads/{branch_name}\n")