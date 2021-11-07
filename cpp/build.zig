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

    const lib = addStaticLib(b, mode, target, dynamic, omaha);
    lib.install();

    // TODO: add tests step
    // var main_tests = b.addTest("src/main.zig");
    // main_tests.setBuildMode(mode);

    // const test_step = b.step("test", "Run library tests");
    // test_step.dependOn(&main_tests.step);

    // 'build examples' step - builds examples/ and installs them to zig-out/bin
    //   - also installs libphe and libpheomaha to zig-out/lib
    //   - these can be built and run manually with the following commands
    //     $ zig run examples/c_example.c -lc -Iinclude -Lzig-out/lib -lpheval
    //     $ zig run examples/cpp_example.cc -lc++ -Iinclude -Lzig-out/lib -lpheval
    //     $ zig run examples/omaha_example.cc -lc++ -Iinclude -Lzig-out/lib -lphevalomaha
    const examples_step = b.step("examples", "build executables in examples folder");
    const example_files: []const []const u8 = &.{ "c_example.c", "cpp_example.cc", "omaha_example.cc" };
    inline for (example_files) |example_file| {
        const exe = b.addExecutable(std.mem.trimRight(u8, example_file, ".c"), null);
        exe.addCSourceFiles(&.{"examples/" ++ example_file}, &.{});
        exe.addIncludeDir("include");
        const want_omaha = std.mem.startsWith(u8, example_file, "omaha");
        const deplib = if (!omaha and want_omaha) addStaticLib(b, mode, target, dynamic, true) else lib;
        exe.linkLibrary(deplib);
        if (std.mem.endsWith(u8, example_file, ".cc")) exe.linkLibCpp() else exe.linkLibC();
        // install the deplib to zig-out/lib - without this 'zig build examples'
        // won't install libs to zig-out/lib
        const deplib_install_step = b.addInstallArtifact(deplib);
        examples_step.dependOn(&deplib_install_step.step);
        // install the example exe to zig-out/bin
        const exe_install_step = b.addInstallArtifact(exe);
        examples_step.dependOn(&exe_install_step.step);
    }
}

fn addStaticLib(b: *std.build.Builder, mode: std.builtin.Mode, target: std.zig.CrossTarget, dynamic: bool, omaha: bool) *std.build.LibExeObjStep {
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
    return lib;
}
