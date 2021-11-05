const std = @import("std");

pub fn build(b: *std.build.Builder) void {
    // Standard release options allow the person running `zig build` to select
    // between Debug, ReleaseSafe, ReleaseFast, and ReleaseSmall.
    const mode = b.standardReleaseOptions();
    const target = b.standardTargetOptions(.{});

    const opts = b.addOptions();
    const dynamic = b.option(bool, "dynamic", "build a dynamic .so or .dll") orelse false;
    opts.addOption(bool, "dynamic", dynamic);
    const omaha = b.option(bool, "omaha", "build omaha lib (libphevalomaha)") orelse false;
    opts.addOption(bool, "omaha", omaha);

    const lib_name = if (omaha) "phevalomaha" else "pheval";
    const lib = b.addStaticLibrary(lib_name, null);

    lib.linkage = if (dynamic) .dynamic else .static;
    lib.setBuildMode(mode);
    lib.setTarget(target);
    const c_sources: []const []const u8 = if (omaha)
        &.{
            "src/dptables.c",
            "src/tables_omaha.c",
            "src/evaluator_omaha.c",
            "src/hash.c",
            "src/hashtable.c",
            "src/rank.c",
            "src/7462.c",
        }
    else
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
        };
    lib.addCSourceFiles(c_sources, &.{"-std=c99"});
    const cpp_sources: []const []const u8 = if (omaha)
        &.{
            "src/evaluator_omaha.cc",
            "src/hand.cc",
        }
    else
        &.{
            "src/evaluator.cc",
            "src/hand.cc",
        };
    lib.addCSourceFiles(
        cpp_sources,
        &.{"-std=c++14"},
    );
    lib.addIncludeDir("include");
    lib.linkLibCpp();

    // TODO: test building on windows with msvc abi
    // if (target.isWindows())
    //     if (target.abi) |abi| if (abi == .msvc) lib.linkLibC();
    lib.install();

    // TODO: add tests step
    // var main_tests = b.addTest("src/main.zig");
    // main_tests.setBuildMode(mode);

    // const test_step = b.step("test", "Run library tests");
    // test_step.dependOn(&main_tests.step);

    // TODO add 'build examples' step
    //   - this can be done manually with the following commands
    // $ zig run examples/c_example.c -lc -Iinclude -Lzig-out/lib -lpheval
    // $ zig run examples/cpp_example.cc -lc++ -Iinclude -Lzig-out/lib -lpheval
    // $ zig run examples/omaha_example.cc -lc++ -Iinclude -Lzig-out/lib -lphevalomaha

}
