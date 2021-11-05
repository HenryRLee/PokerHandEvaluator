const std = @import("std");

pub fn build(b: *std.build.Builder) void {
    // Standard release options allow the person running `zig build` to select
    // between Debug, ReleaseSafe, ReleaseFast, and ReleaseSmall.
    const mode = b.standardReleaseOptions();
    const target = b.standardTargetOptions(.{});
    const lib = b.addStaticLibrary("pheval", null);
    const opts = b.addOptions();
    const dynamic = b.option(bool, "dynamic", "build dynamic or static lib") orelse false;
    opts.addOption(bool, "dynamic", dynamic);

    lib.linkage = if (dynamic) .dynamic else .static;
    lib.setBuildMode(mode);
    lib.setTarget(target);
    lib.addCSourceFiles(
        &.{
            "src/evaluator5.c",
            "src/hashtable5.c",
            "src/evaluator6.c",
            "src/hashtable6.c",
            "src/evaluator7.c",
            "src/hashtable7.c",
            "src/hash.c",
            "src/hashtable.c",
            "src/dptables.c",
            "src/rank.c",
            "src/7462.c",
        },
        &.{"-std=c99"},
    );
    lib.addCSourceFiles(
        &.{
            "src/evaluator.cc",
            "src/hand.cc",
        },
        &.{"-std=c++14"},
    );
    lib.addIncludeDir("include");
    lib.linkLibCpp();
    lib.install();

    var main_tests = b.addTest("src/main.zig");
    main_tests.setBuildMode(mode);

    const test_step = b.step("test", "Run library tests");
    test_step.dependOn(&main_tests.step);
}
