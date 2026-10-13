#!/usr/bin/env python3
"""Execute README install/uninstall examples only inside a disposable fixture.

No model dispatch, real install, HOME mutation or prose assertions. The source
checkout and skill-directory inputs alone are redirected to temporary paths.
"""
import os
from pathlib import Path
import re
import shlex
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[4]
README = (ROOT / "README.md").read_text()


def snippet(start, end, index):
    section = README.split(start, 1)[1].split(end, 1)[0]
    return re.findall(r"```bash\n(.*?)```", section, re.S)[index]


INSTALL = snippet("### 2. 安装", "### 3. 使用", 1)
UNINSTALL = snippet("## 卸载", "## 贡献", 0)


def run(script, fixture_checkout, fixture_skills):
    # Baseline tilde commands need the same path-only adaptation as the fixed
    # parameterized examples. Never assign HOME, home or CODEX_HOME.
    script = script.replace("~/grill-autopilot/skills/grill-autopilot", shlex.quote(str(fixture_checkout / "skills" / "grill-autopilot")))
    script = script.replace("~/.claude/skills/grill-autopilot", shlex.quote(str(fixture_skills / "grill-autopilot")))
    script = script.replace("~/.codex/skills/grill-autopilot", shlex.quote(str(fixture_skills / "grill-autopilot")))
    env = dict(os.environ, autopilot_checkout=str(fixture_checkout),
               autopilot_skills=str(fixture_skills))
    result = subprocess.run(["bash", "-c", script], env=env, text=True,
                            capture_output=True, timeout=10)
    print(f"shell exit={result.returncode}; {result.stdout.strip()} {result.stderr.strip()}")
    return result.returncode


with tempfile.TemporaryDirectory(prefix="grill-autopilot-12-") as temporary:
    fixture_home = Path(temporary) / "fixture home"
    fixture_checkout = fixture_home / "grill-autopilot"
    fixture_source = fixture_checkout / "skills" / "grill-autopilot"
    fixture_source.mkdir(parents=True)
    (fixture_source / "SKILL.md").write_text("fixture source remains intact\n")
    for runtime in (".codex", ".claude"):
        fixture_skills = fixture_home / runtime / "skills"
        target = fixture_skills / "grill-autopilot"
        print(f"CASE {runtime}: empty directory install")
        assert run(INSTALL, fixture_checkout, fixture_skills) == 0
        assert target.is_symlink() and target.readlink() == fixture_source
        print("CASE owned repeated install")
        assert run(INSTALL, fixture_checkout, fixture_skills) == 0
        assert target.readlink() == fixture_source
        assert sorted(p.name for p in fixture_source.iterdir()) == ["SKILL.md"]
        print("CASE owned uninstall and absent uninstall")
        assert run(UNINSTALL, fixture_checkout, fixture_skills) == 0
        assert not target.is_symlink() and not target.exists()
        assert run(UNINSTALL, fixture_checkout, fixture_skills) == 0
        assert (fixture_source / "SKILL.md").read_text() == "fixture source remains intact\n"
        for kind in ("file", "directory", "foreign-link", "dangling-link"):
            print(f"CASE conflicting {kind}: install + uninstall preserve")
            foreign = fixture_home / f"{runtime}-{kind}"
            if kind == "file":
                target.write_bytes(b"independent user content\x00")
            elif kind == "directory":
                target.mkdir()
                (target / "keep").write_text("keep")
            else:
                if kind == "foreign-link":
                    foreign.mkdir()
                    (foreign / "keep").write_text("foreign content")
                target.symlink_to(foreign)
            assert run(INSTALL, fixture_checkout, fixture_skills) != 0
            assert run(UNINSTALL, fixture_checkout, fixture_skills) != 0
            if kind == "file":
                assert target.read_bytes() == b"independent user content\x00"
                target.unlink()
            elif kind == "directory":
                assert (target / "keep").read_text() == "keep"
                (target / "keep").unlink()
                target.rmdir()
            else:
                assert target.is_symlink() and target.readlink() == foreign
                if kind == "foreign-link":
                    assert sorted(p.name for p in foreign.iterdir()) == ["keep"]
                    assert (foreign / "keep").read_text() == "foreign content"
                target.unlink()
        print("CASE owned dangling uninstall")
        target.symlink_to(fixture_skills / "missing-checkout" / "skills" / "grill-autopilot")
        missing_checkout = fixture_skills / "missing-checkout"
        assert run(UNINSTALL, missing_checkout, fixture_skills) == 0
        assert not target.is_symlink()
        print("CASE missing source install refuses")
        assert run(INSTALL, missing_checkout, fixture_skills) != 0
        assert not target.is_symlink() and not target.exists()
    print("PASS: 28 shell operations; both runtime directories; fixture removed on exit")
