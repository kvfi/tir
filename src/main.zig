const std = @import("std");
const Tir = @import("tir.zig").Tir;
const Server = @import("server.zig").Server;
const watcher = @import("watcher.zig");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const args = try std.process.argsAlloc(allocator);
    defer std.process.argsFree(allocator, args);

    if (args.len < 2) {
        printUsage();
        return;
    }

    const command = args[1];

    if (std.mem.eql(u8, command, "init")) {
        try cmdInit(allocator);
    } else if (std.mem.eql(u8, command, "build")) {
        try cmdBuild(allocator);
    } else if (std.mem.eql(u8, command, "watch")) {
        try cmdWatch(allocator);
    } else if (std.mem.eql(u8, command, "server")) {
        try cmdServer(allocator);
    } else if (std.mem.eql(u8, command, "help") or std.mem.eql(u8, command, "-h") or std.mem.eql(u8, command, "--help")) {
        printUsage();
    } else {
        std.debug.print("Unknown command: {s}\n", .{command});
        printUsage();
    }
}

fn printUsage() void {
    const usage =
        \\Tir - A minimal static site generator in Zig
        \\
        \\Usage: tir <command>
        \\
        \\Commands:
        \\  init       Initialize a new Tir project
        \\  build      Build the static site
        \\  watch      Watch for changes and rebuild
        \\  server     Start development server
        \\  help       Show this help message
        \\
    ;
    std.debug.print("{s}", .{usage});
}

fn cmdInit(allocator: std.mem.Allocator) !void {
    var tir = try Tir.init(allocator);
    defer tir.deinit();

    try tir.initProject();
}

fn cmdBuild(allocator: std.mem.Allocator) !void {
    var tir = try Tir.init(allocator);
    defer tir.deinit();

    try tir.build(null);
}

fn cmdWatch(allocator: std.mem.Allocator) !void {
    std.debug.print("Watch command not yet implemented\n", .{});
    // TODO: Implement file watching with watcher module
}

fn cmdServer(allocator: std.mem.Allocator) !void {
    std.debug.print("Server command not yet implemented\n", .{});
    // TODO: Implement HTTP server with Server module
}
