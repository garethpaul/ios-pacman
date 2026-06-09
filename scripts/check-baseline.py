#!/usr/bin/env python3
from pathlib import Path
import plistlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BASELINE_PLAN = ROOT / "docs/plans/2026-06-08-objective-c-game-baseline.md"
MAKE_GATES_PLAN = ROOT / "docs/plans/2026-06-09-make-gate-aliases.md"
MOTION_CAPTURE_PLAN = ROOT / "docs/plans/2026-06-08-motion-capture-lifecycle.md"
TIME_DELTA_PLAN = ROOT / "docs/plans/2026-06-08-frame-delta-clamp.md"
COLLISION_ALERT_PLAN = ROOT / "docs/plans/2026-06-08-collision-alert-guard.md"
ALERT_PAUSE_PLAN = ROOT / "docs/plans/2026-06-09-alert-update-pause.md"
ALERT_CLOCK_PLAN = ROOT / "docs/plans/2026-06-09-alert-frame-clock-reset.md"
FAILURE_VELOCITY_PLAN = ROOT / "docs/plans/2026-06-09-failure-velocity-reset.md"
WIN_COMPLETION_PLAN = ROOT / "docs/plans/2026-06-09-win-completion-update-guard.md"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def strip_c_line_comments(text):
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def parse_xml(relative_path, failures):
    try:
        ET.parse(str(ROOT / relative_path))
    except ET.ParseError as error:
        failures.append(f"{relative_path} is not well-formed XML: {error}")


def parse_plist(relative_path, failures):
    try:
        with (ROOT / relative_path).open("rb") as file:
            return plistlib.load(file)
    except Exception as error:
        failures.append(f"{relative_path} is not a readable plist: {error}")
        return {}


def check_png(relative_path, failures):
    path = ROOT / relative_path
    try:
        with path.open("rb") as file:
            signature = file.read(len(PNG_SIGNATURE))
        require(signature == PNG_SIGNATURE, f"{relative_path} must be a PNG image", failures)
        require(path.stat().st_size > 100, f"{relative_path} must not be empty", failures)
    except OSError as error:
        failures.append(f"{relative_path} could not be read: {error}")


def main():
    failures = []
    required_files = [
        ".gitignore",
        ".travis.yml",
        "CHANGES.md",
        "Makefile",
        "README.md",
        "SECURITY.md",
        "VISION.md",
        "build.sh",
        "Maze.xcodeproj/project.pbxproj",
        "Maze.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
        "Maze.xcodeproj/xcshareddata/xcschemes/Maze.xcscheme",
        "Maze/Maze-Info.plist",
        "Maze/APPAppDelegate.h",
        "Maze/APPAppDelegate.m",
        "Maze/APPViewController.h",
        "Maze/APPViewController.m",
        "Maze/main.m",
        "Maze/en.lproj/APPViewController.xib",
        "Maze/en.lproj/InfoPlist.strings",
        "Maze/pacman.png",
        "Maze/wall.png",
        "Maze/squareWall.png",
        "Maze/exit.png",
        "Maze/ghost.png",
        "Maze/Default.png",
        "Maze/Default@2x.png",
        "Maze/Default-568h@2x.png",
        "screenshots/screenshot01.png",
        "docs/plans/2026-06-08-objective-c-game-baseline.md",
        "docs/plans/2026-06-09-make-gate-aliases.md",
        "docs/plans/2026-06-08-motion-capture-lifecycle.md",
        "docs/plans/2026-06-08-frame-delta-clamp.md",
        "docs/plans/2026-06-08-collision-alert-guard.md",
        "docs/plans/2026-06-09-alert-update-pause.md",
        "docs/plans/2026-06-09-alert-frame-clock-reset.md",
        "docs/plans/2026-06-09-failure-velocity-reset.md",
        "docs/plans/2026-06-09-win-completion-update-guard.md",
        "docs/readme-overview.svg",
    ]

    for relative_path in required_files:
        require((ROOT / relative_path).is_file(), f"Required file missing: {relative_path}", failures)

    for xml_file in [
        "Maze.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
        "Maze.xcodeproj/xcshareddata/xcschemes/Maze.xcscheme",
        "Maze/en.lproj/APPViewController.xib",
        "docs/readme-overview.svg",
    ]:
        parse_xml(xml_file, failures)

    for image_file in [
        "Maze/pacman.png",
        "Maze/wall.png",
        "Maze/squareWall.png",
        "Maze/exit.png",
        "Maze/ghost.png",
        "Maze/Default.png",
        "Maze/Default@2x.png",
        "Maze/Default-568h@2x.png",
        "screenshots/screenshot01.png",
    ]:
        check_png(image_file, failures)

    app_plist = parse_plist("Maze/Maze-Info.plist", failures)
    project = read("Maze.xcodeproj/project.pbxproj")
    xib = read("Maze/en.lproj/APPViewController.xib")
    build_script = read("build.sh")
    view_header = read("Maze/APPViewController.h")
    view_controller = read("Maze/APPViewController.m")
    source = "\n".join(strip_c_line_comments(path.read_text(encoding="utf-8", errors="replace"))
                       for path in sorted((ROOT / "Maze").glob("*.m")))
    readme = read("README.md")
    vision = read("VISION.md")
    security = read("SECURITY.md")
    changes = read("CHANGES.md")
    gitignore = read(".gitignore")
    makefile = read("Makefile")
    baseline_plan = BASELINE_PLAN.read_text(encoding="utf-8") if BASELINE_PLAN.exists() else ""
    make_gates_plan = MAKE_GATES_PLAN.read_text(encoding="utf-8") if MAKE_GATES_PLAN.exists() else ""
    motion_capture_plan = MOTION_CAPTURE_PLAN.read_text(encoding="utf-8") if MOTION_CAPTURE_PLAN.exists() else ""
    time_delta_plan = TIME_DELTA_PLAN.read_text(encoding="utf-8") if TIME_DELTA_PLAN.exists() else ""
    collision_alert_plan = COLLISION_ALERT_PLAN.read_text(encoding="utf-8") if COLLISION_ALERT_PLAN.exists() else ""
    alert_pause_plan = ALERT_PAUSE_PLAN.read_text(encoding="utf-8") if ALERT_PAUSE_PLAN.exists() else ""
    alert_clock_plan = ALERT_CLOCK_PLAN.read_text(encoding="utf-8") if ALERT_CLOCK_PLAN.exists() else ""
    failure_velocity_plan = FAILURE_VELOCITY_PLAN.read_text(encoding="utf-8") if FAILURE_VELOCITY_PLAN.exists() else ""
    win_completion_plan = WIN_COMPLETION_PLAN.read_text(encoding="utf-8") if WIN_COMPLETION_PLAN.exists() else ""

    shell_result = subprocess.run(["sh", "-n", "build.sh"], cwd=str(ROOT), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(shell_result.returncode == 0,
            f"build.sh must pass POSIX shell syntax checks: {shell_result.stderr.strip()}",
            failures)
    require("function ci_build" not in build_script and "ci_build() {" in build_script,
            "build.sh must use POSIX-compatible function syntax",
            failures)
    require("command -v xcodebuild" in build_script and "xcodebuild unavailable" in build_script,
            "build.sh must skip cleanly on hosts without Xcode",
            failures)
    require('xcodebuild -project "Maze.xcodeproj"' in build_script and '-scheme "Maze"' in build_script and '-configuration "Debug"' in build_script,
            "build.sh must preserve the Maze Debug simulator build command",
            failures)

    require(app_plist.get("CFBundleIdentifier") == "$(PRODUCT_BUNDLE_IDENTIFIER)",
            "Maze Info.plist must keep bundle identifier delegated to Xcode settings",
            failures)
    require(app_plist.get("NSMainNibFile") == "APPViewController",
            "Maze Info.plist must keep the XIB entry point",
            failures)
    require("IPHONEOS_DEPLOYMENT_TARGET = 10.0;" in project and 'INFOPLIST_FILE = "Maze/Maze-Info.plist";' in project,
            "Xcode project must preserve target deployment and Info.plist wiring",
            failures)
    require("CLANG_ENABLE_OBJC_ARC = YES;" in project and "CoreMotion.framework" in project and "QuartzCore.framework" in project,
            "Xcode project must keep ARC and gameplay framework references",
            failures)
    for resource in ["pacman.png", "wall.png", "squareWall.png", "exit.png", "ghost.png", "APPViewController.xib"]:
        require(resource in project,
                f"Xcode project must keep resource reference: {resource}",
                failures)
    for resource in ["pacman.png", "squareWall.png", "exit.png", "ghost.png"]:
        require(resource in xib,
                f"XIB must keep image reference: {resource}",
                failures)
    require("outletCollection property=\"wall\"" in xib and "property=\"pacman\"" in xib and "property=\"exit\"" in xib,
            "XIB must keep gameplay outlets wired",
            failures)
    require("startAccelerometerUpdatesToQueue" in source and "stopAccelerometerUpdates" in source,
            "Objective-C source must keep accelerometer motion start/stop behavior",
            failures)
    require("error != nil || accelerometerData == nil" in source and "- (void)dealloc" in source,
            "Objective-C source must ignore unavailable motion samples and stop updates during teardown",
            failures)
    require("__weak APPViewController *weakSelf = self;" in source and
            "APPViewController *strongSelf = weakSelf;" in source and
            "strongSelf.acceleration = accelerometerData.acceleration;" in source,
            "accelerometer callback must avoid strongly retaining the view controller",
            failures)
    require("NSTimeInterval secondsSinceLastDraw = -([self.lastUpdateTime timeIntervalSinceNow]);" in source and
            "secondsSinceLastDraw = MAX(0, MIN(secondsSinceLastDraw, 0.1));" in source,
            "gameplay updates must clamp frame time deltas before integrating accelerometer velocity",
            failures)
    require("<UIAlertViewDelegate>" in view_header and "@property (assign, nonatomic) BOOL collisionAlertVisible;" in view_header,
            "APPViewController must expose collision alert visibility state for repeated collision guards",
            failures)
    require("@property (assign, nonatomic) BOOL gameCompleted;" in view_header,
            "APPViewController must expose terminal win-completion state",
            failures)
    require(view_controller.count("if (self.collisionAlertVisible) {") >= 2 and
            view_controller.count("self.collisionAlertVisible = YES;") >= 2 and
            "- (void)alertView:(UIAlertView *)alertView didDismissWithButtonIndex:(NSInteger)buttonIndex" in view_controller and
            "self.collisionAlertVisible = NO;" in view_controller,
            "collision alerts must be gated while visible and reset after dismissal",
            failures)
    exit_collision_index = view_controller.find("- (void)collisionWithExit")
    win_completed_index = view_controller.find("self.gameCompleted = YES;", exit_collision_index)
    win_x_velocity_reset_index = view_controller.find("self.pacmanXVelocity = 0;", exit_collision_index)
    win_y_velocity_reset_index = view_controller.find("self.pacmanYVelocity = 0;", exit_collision_index)
    win_motion_stop_index = view_controller.find("[self.motionManager stopAccelerometerUpdates];", exit_collision_index)
    win_alert_index = view_controller.find('UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Congratulations"', exit_collision_index)
    require(exit_collision_index != -1 and win_completed_index != -1 and
            win_x_velocity_reset_index != -1 and win_y_velocity_reset_index != -1 and
            win_motion_stop_index != -1 and win_alert_index != -1 and
            win_completed_index < win_x_velocity_reset_index < win_y_velocity_reset_index < win_motion_stop_index < win_alert_index,
            "win collision handling must mark completion and stop movement before showing the alert",
            failures)
    ghost_collision_index = view_controller.find("- (void)collisionWithGhosts")
    failure_position_reset_index = view_controller.find("self.currentPoint  = CGPointMake(0, 144);", ghost_collision_index)
    failure_x_velocity_reset_index = view_controller.find("self.pacmanXVelocity = 0;", ghost_collision_index)
    failure_y_velocity_reset_index = view_controller.find("self.pacmanYVelocity = 0;", ghost_collision_index)
    failure_alert_index = view_controller.find('UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Oops!"', ghost_collision_index)
    require(ghost_collision_index != -1 and failure_position_reset_index != -1 and
            failure_x_velocity_reset_index != -1 and failure_y_velocity_reset_index != -1 and
            failure_alert_index != -1 and
            failure_position_reset_index < failure_x_velocity_reset_index < failure_y_velocity_reset_index < failure_alert_index,
            "failure collision handling must reset position and velocities before showing the alert",
            failures)
    alert_dismiss = re.search(r"- \(void\)alertView:\(UIAlertView \*\)alertView didDismissWithButtonIndex:\(NSInteger\)buttonIndex[\s\S]+?\n}", view_controller)
    require(alert_dismiss is not None and
            "self.collisionAlertVisible = NO;" in alert_dismiss.group(0) and
            "self.lastUpdateTime = [NSDate date];" in alert_dismiss.group(0),
            "alert dismissal must reset the frame clock before gameplay resumes",
            failures)
    require("- (void)update {\n    if (self.collisionAlertVisible || self.gameCompleted) {\n        return;\n    }" in view_controller,
            "gameplay updates must pause while collision alerts are visible or the game is completed",
            failures)
    require(not re.search(r"\b(?:NSLog|printf)\s*\(", source),
            "Gameplay source must not use debug console logging",
            failures)
    for forbidden in ["NSURL", "NSURLConnection", "UIWebView", "http://", "https://", "upload", "analytics", "NSUserDefaults"]:
        require(forbidden not in source,
                f"Game sample must not add network, upload, analytics, or persistence behavior: {forbidden}",
                failures)

    require("*.local.xcconfig" in gitignore and ".env" in gitignore and "DerivedData" in gitignore,
            ".gitignore must exclude local config and Xcode build products",
            failures)
    require(".PHONY: build check lint test" in makefile and "lint test build: check" in makefile,
            "Makefile must expose lint, test, and build aliases for the local baseline",
            failures)
    require("make lint" in readme and "make test" in readme and "make build" in readme and "make check" in readme and "build.sh" in readme and "Maze.xcodeproj" in readme,
            "README must document static verification, build script, and project usage",
            failures)
    require("local game" in readme.lower() and "asset" in readme.lower() and
            "accelerometer" in readme.lower() and "time delta" in readme.lower() and "collision alert" in readme.lower() and "alert pause" in readme.lower(),
            "README must document local-only gameplay, asset checks, accelerometer lifecycle, collision-alert, and time delta guardrails",
            failures)
    require("frame clock" in readme.lower(),
            "README must document alert frame clock reset behavior",
            failures)
    require("velocity reset" in readme.lower(),
            "README must document failure velocity reset behavior",
            failures)
    require("win completion" in readme.lower(),
            "README must document terminal win-completion update guard behavior",
            failures)
    require("scripts/check-baseline.py" in vision and "make lint" in vision and "make test" in vision and "make build" in vision and "asset" in vision.lower() and
            "time delta" in vision.lower() and "collision alert" in vision.lower() and "alert pause" in vision.lower(),
            "VISION must describe the current static Objective-C game baseline",
            failures)
    require("frame clock" in vision.lower(),
            "VISION must describe alert frame clock reset behavior",
            failures)
    require("velocity reset" in vision.lower(),
            "VISION must describe failure velocity reset behavior",
            failures)
    require("win completion" in vision.lower(),
            "VISION must describe terminal win-completion update guard behavior",
            failures)
    require("build.sh" in security and "make check" in security and "collision alert" in security.lower() and
            "alert pause" in security.lower() and "frame clock" in security.lower(),
            "SECURITY must document build script and static baseline guardrails",
            failures)
    require("velocity reset" in security.lower(),
            "SECURITY must document failure velocity reset guardrails",
            failures)
    require("win completion" in security.lower(),
            "SECURITY must document terminal win-completion update guardrails",
            failures)
    require("/bin/sh" in changes and "without Xcode" in changes and "accelerometer" in changes and
            "weak" in changes.lower() and "time delta" in changes.lower() and
            "collision alert" in changes.lower() and "alert pause" in changes.lower() and "make check" in changes and "make lint" in changes and "make test" in changes and "make build" in changes,
            "CHANGES must record the shell fix, Xcode skip, motion guard, weak capture, collision-alert guard, time delta clamp, and baseline",
            failures)
    require("frame clock" in changes.lower(),
            "CHANGES must record alert frame clock reset behavior",
            failures)
    require("velocity reset" in changes.lower(),
            "CHANGES must record failure velocity reset behavior",
            failures)
    require("win completion" in changes.lower(),
            "CHANGES must record terminal win-completion update guard behavior",
            failures)
    require("status: completed" in baseline_plan and "status: completed" in motion_capture_plan and
            "status: completed" in time_delta_plan and "status: completed" in collision_alert_plan,
            "plans must be marked completed",
            failures)
    require("status: completed" in make_gates_plan,
            "make gate aliases plan must be marked completed",
            failures)
    require("status: completed" in alert_pause_plan,
            "alert update pause plan must be marked completed",
            failures)
    require("status: completed" in alert_clock_plan,
            "alert frame clock reset plan must be marked completed",
            failures)
    require("status: completed" in failure_velocity_plan,
            "failure velocity reset plan must be marked completed",
            failures)
    require("status: completed" in win_completion_plan,
            "win completion update guard plan must be marked completed",
            failures)

    if shutil.which("xcodebuild"):
        print("xcodebuild is available; run ./build.sh or an Xcode build on macOS before release.")
    else:
        print("xcodebuild unavailable; static iOS baseline only.")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("ios-pacman Objective-C baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
