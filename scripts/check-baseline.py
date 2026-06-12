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
PREVIOUS_POINT_PLAN = ROOT / "docs/plans/2026-06-10-previous-point-initialization.md"
CI_PLAN = ROOT / "docs/plans/2026-06-10-ci-baseline.md"
HOSTED_VALIDATION_PLAN = ROOT / "docs/plans/2026-06-10-hosted-project-validation.md"
CORRECTED_COLLISION_PLAN = ROOT / "docs/plans/2026-06-10-corrected-collision-build.md"
MAIN_THREAD_MOTION_PLAN = ROOT / "docs/plans/2026-06-12-main-thread-motion-handoff.md"
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
        ".github/workflows/check.yml",
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
        "docs/plans/2026-06-10-previous-point-initialization.md",
        "docs/plans/2026-06-10-ci-baseline.md",
        "docs/plans/2026-06-10-hosted-project-validation.md",
        "docs/plans/2026-06-10-corrected-collision-build.md",
        "docs/plans/2026-06-12-main-thread-motion-handoff.md",
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
    ci_workflow = read(".github/workflows/check.yml")
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
    previous_point_plan = PREVIOUS_POINT_PLAN.read_text(encoding="utf-8") if PREVIOUS_POINT_PLAN.exists() else ""
    ci_plan = CI_PLAN.read_text(encoding="utf-8") if CI_PLAN.exists() else ""
    hosted_validation_plan = HOSTED_VALIDATION_PLAN.read_text(encoding="utf-8") if HOSTED_VALIDATION_PLAN.exists() else ""
    corrected_collision_plan = CORRECTED_COLLISION_PLAN.read_text(encoding="utf-8") if CORRECTED_COLLISION_PLAN.exists() else ""
    main_thread_motion_plan = MAIN_THREAD_MOTION_PLAN.read_text(encoding="utf-8") if MAIN_THREAD_MOTION_PLAN.exists() else ""

    shell_result = subprocess.run(["sh", "-n", "build.sh"], cwd=str(ROOT), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(shell_result.returncode == 0,
            f"build.sh must pass POSIX shell syntax checks: {shell_result.stderr.strip()}",
            failures)
    require("function ci_build" not in build_script,
            "build.sh must remain POSIX-compatible", failures)
    require("command -v xcodebuild" in build_script and "xcodebuild unavailable" in build_script,
            "build.sh must skip cleanly on hosts without Xcode",
            failures)
    require('xcodebuild -project "Maze.xcodeproj"' in build_script and '-scheme "Maze"' in build_script and
            '-destination "generic/platform=iOS Simulator"' in build_script and '-configuration "Debug"' in build_script and
            "CODE_SIGNING_ALLOWED=NO" in build_script,
            "build.sh must compile the unsigned Maze Debug target for a generic simulator",
            failures)

    require(app_plist.get("CFBundleIdentifier") == "$(PRODUCT_BUNDLE_IDENTIFIER)",
            "Maze Info.plist must keep bundle identifier delegated to Xcode settings",
            failures)
    require(app_plist.get("NSMainNibFile") == "APPViewController",
            "Maze Info.plist must keep the XIB entry point",
            failures)
    require(project.count("IPHONEOS_DEPLOYMENT_TARGET = 12.0;") == 4 and
            'INFOPLIST_FILE = "Maze/Maze-Info.plist";' in project,
            "Xcode project must use iOS 12 project and target deployment settings and preserve Info.plist wiring",
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
    sample_capture_index = view_controller.find("CMAcceleration acceleration = accelerometerData.acceleration;")
    main_dispatch_index = view_controller.find("dispatch_async(dispatch_get_main_queue(), ^{")
    strong_capture_index = view_controller.find("APPViewController *strongSelf = weakSelf;", main_dispatch_index)
    sample_assignment_index = view_controller.find("strongSelf.acceleration = acceleration;", main_dispatch_index)
    update_index = view_controller.find("[strongSelf update];", main_dispatch_index)
    require("__weak APPViewController *weakSelf = self;" in source and
            sample_capture_index != -1 and main_dispatch_index != -1 and
            strong_capture_index != -1 and sample_assignment_index != -1 and update_index != -1 and
            sample_capture_index < main_dispatch_index < strong_capture_index < sample_assignment_index < update_index and
            "performSelectorOnMainThread" not in source,
            "accelerometer samples must resolve weak capture, assign state, and update together on the main thread",
            failures)
    require("NSTimeInterval secondsSinceLastDraw = -([self.lastUpdateTime timeIntervalSinceNow]);" in source and
            "secondsSinceLastDraw = MAX(0, MIN(secondsSinceLastDraw, 0.1));" in source,
            "gameplay updates must clamp frame time deltas before integrating accelerometer velocity",
            failures)
    require("self.currentPoint  = CGPointMake(0, 144);\n    self.previousPoint = self.currentPoint;" in view_controller,
            "viewDidLoad must initialize previousPoint to the starting position before wall collisions can roll back movement",
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
    move_index = view_controller.find("- (void)movePacman")
    boundary_index = view_controller.find("[self collisionWithBoundaries];", move_index)
    wall_index = view_controller.find("[self collisionWithWalls];", move_index)
    candidate_index = view_controller.find("CGRect candidateFrame = [self candidatePacmanFrame];", move_index)
    exit_index = view_controller.find("[self collisionWithExit:candidateFrame];", move_index)
    completion_guard_index = view_controller.find("if (!self.gameCompleted) {", move_index)
    ghost_index = view_controller.find("[self collisionWithGhosts:candidateFrame];", move_index)
    require(move_index != -1 and boundary_index < wall_index < candidate_index < exit_index < completion_guard_index < ghost_index,
            "movement must resolve boundaries and walls before evaluating one corrected outcome frame and stop ghost checks after a win",
            failures)
    require("- (CGRect)candidatePacmanFrame" in view_controller and "frame.origin = self.currentPoint;" in view_controller and
            "- (void)collisionWithExit:(CGRect)pacmanFrame" in view_controller and
            "- (void)collisionWithGhosts:(CGRect)pacmanFrame" in view_controller and
            view_controller.count("CGRectIntersectsRect(pacmanFrame,") == 4 and "collsionWithWalls" not in view_controller,
            "outcome collisions must use the corrected candidate frame and the wall handler must keep its corrected spelling",
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
    require(".PHONY: build check lint test" in makefile and "lint test build: check" in makefile and
            "check:\n\tpython3 scripts/check-baseline.py\n\t./build.sh" in makefile,
            "Makefile must expose lint, test, and build aliases and compile through the check gate when Xcode is available",
            failures)
    require("make lint" in readme and "make test" in readme and "make build" in readme and "make check" in readme and "build.sh" in readme and "Maze.xcodeproj" in readme,
            "README must document static verification, build script, and project usage",
            failures)
    require("GitHub Actions" in readme,
            "README must document the hosted GitHub Actions baseline",
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
    require("previous position" in readme.lower(),
            "README must document previous-position initialization behavior",
            failures)
    require("scripts/check-baseline.py" in vision and "make lint" in vision and "make test" in vision and "make build" in vision and "asset" in vision.lower() and
            "time delta" in vision.lower() and "collision alert" in vision.lower() and "alert pause" in vision.lower(),
            "VISION must describe the current static Objective-C game baseline",
            failures)
    require("GitHub Actions" in vision,
            "VISION must document the hosted verification baseline",
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
    require("previous position" in vision.lower(),
            "VISION must describe previous-position initialization behavior",
            failures)
    require("build.sh" in security and "make check" in security and "collision alert" in security.lower() and
            "alert pause" in security.lower() and "frame clock" in security.lower(),
            "SECURITY must document build script and static baseline guardrails",
            failures)
    require("GitHub Actions" in security,
            "SECURITY must document the hosted static baseline",
            failures)
    require("velocity reset" in security.lower(),
            "SECURITY must document failure velocity reset guardrails",
            failures)
    require("win completion" in security.lower(),
            "SECURITY must document terminal win-completion update guardrails",
            failures)
    require("previous position" in security.lower(),
            "SECURITY must document previous-position initialization guardrails",
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
    require("previous position" in changes.lower(),
            "CHANGES must record previous-position initialization behavior",
            failures)
    require("GitHub Actions" in changes,
            "CHANGES must record hosted baseline coverage",
            failures)
    require("corrected candidate frame" in changes and "unsigned generic-simulator" in changes,
            "CHANGES must record corrected collision and hosted build behavior",
            failures)
    require("actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065" in ci_workflow and
            'python-version: "3.12"' in ci_workflow and
            "persist-credentials: false" in ci_workflow and
            "make check" in ci_workflow,
            "GitHub Actions workflow must use credential-free checkout, pinned Python 3.12, and make check",
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
    require("status: completed" in previous_point_plan,
            "previous point initialization plan must be marked completed",
            failures)
    require("status: completed" in ci_plan and "make check" in ci_plan and
            "Python" in ci_plan and "3.12" in ci_plan and "credential persistence disabled" in ci_plan and
            "generic-simulator" in ci_plan,
            "CI baseline plan must document completed credential-free Python and simulator validation",
            failures)
    require("status: completed" in hosted_validation_plan and "make check" in hosted_validation_plan and
            "Python 3.12" in hosted_validation_plan and "generic iOS simulator" in hosted_validation_plan,
            "hosted validation plan must document completed Python and simulator validation", failures)
    require("status: completed" in corrected_collision_plan and "generic iOS simulator" in corrected_collision_plan,
            "corrected collision build plan must be completed", failures)
    require("status: completed" in main_thread_motion_plan and "mutation" in main_thread_motion_plan.lower(),
            "main-thread motion handoff plan must record completed mutation verification", failures)
    require(ci_workflow.count("permissions:\n  contents: read") == 1 and
            not re.search(r"(?m)^\s{2,}permissions:\s*$", ci_workflow) and
            not re.search(r"(?m)^\s+[A-Za-z0-9_-]+:\s*write\s*$", ci_workflow) and
            "cancel-in-progress: true" in ci_workflow and
            "runs-on: macos-15" in ci_workflow and "timeout-minutes: 10" in ci_workflow and
            ci_workflow.count("uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10") == 1 and
            "persist-credentials: false" in ci_workflow and
            ci_workflow.count("uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065") == 1 and
            'python-version: "3.12"' in ci_workflow and
            "run: make check" in ci_workflow,
            "Check workflow contract must stay pinned, read-only, and bounded", failures)

    if shutil.which("xcodebuild"):
        result = subprocess.run(["xcodebuild", "-list", "-project", "Maze.xcodeproj"], cwd=ROOT,
                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        require(result.returncode == 0, "xcodebuild could not parse Maze.xcodeproj: " + result.stderr.strip(), failures)
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
