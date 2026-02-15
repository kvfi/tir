const std = @import("std");

pub const Watcher = struct {
    paths: [][]const u8,
    patterns: ?[][]const u8 = null,
    ignore_patterns: ?[][]const u8 = null,
    allocator: std.mem.Allocator,

    pub fn init(
        allocator: std.mem.Allocator,
        paths: [][]const u8,
        patterns: ?[][]const u8,
        ignore_patterns: ?[][]const u8,
    ) !Watcher {
        return .{
            .paths = paths,
            .patterns = patterns,
            .ignore_patterns = ignore_patterns,
            .allocator = allocator,
        };
    }

    pub fn watch(
        self: *Watcher,
        callback: *const fn (path: []const u8) anyerror!void,
    ) !void {
        std.debug.print("Watching directories...\n", .{});
        for (self.paths) |path| {
            std.debug.print("Watching: {s}\n", .{path});
        }

        // Note: Zig standard library doesn't have built-in file watching
        // This is a simplified implementation that polls for changes
        // For production, use OS-specific APIs (FSEvents on macOS, inotify on Linux, etc)

        var last_mtimes = std.StringHashMap(i64).init(self.allocator);
        defer last_mtimes.deinit();

        while (true) {
            var found_change = false;

            for (self.paths) |dir_path| {
                var walker = try std.fs.cwd().walk(self.allocator);
                defer walker.deinit();

                var it = walker.walk();
                while (try it.next()) |entry| {
                    if (entry.kind == .file) {
                        // Check if file matches patterns
                        if (self.shouldWatch(entry.path)) {
                            const full_path = try std.fmt.allocPrint(
                                self.allocator,
                                "{s}/{s}",
                                .{ dir_path, entry.path },
                            );
                            defer self.allocator.free(full_path);

                            const file = std.fs.cwd().openFile(full_path, .{}) catch continue;
                            defer file.close();

                            const stat = try file.stat();
                            const mtime = stat.mtime;

                            if (last_mtimes.get(full_path)) |old_mtime| {
                                if (old_mtime != mtime) {
                                    std.debug.print("File changed: {s}\n", .{full_path});
                                    try callback(full_path);
                                    found_change = true;
                                }
                            }

                            try last_mtimes.put(
                                try self.allocator.dupe(u8, full_path),
                                mtime,
                            );
                        }
                    }
                }
            }

            // Poll every 500ms
            std.time.sleep(500 * std.time.ns_per_ms);
        }
    }

    fn shouldWatch(self: *Watcher, path: []const u8) bool {
        // Check if path should be ignored
        if (self.ignore_patterns) |patterns| {
            for (patterns) |pattern| {
                if (self.matchesPattern(path, pattern)) {
                    return false;
                }
            }
        }

        // If patterns are specified, only watch matching files
        if (self.patterns) |patterns| {
            for (patterns) |pattern| {
                if (self.matchesPattern(path, pattern)) {
                    return true;
                }
            }
            return false;
        }

        return true;
    }

    fn matchesPattern(self: *Watcher, path: []const u8, pattern: []const u8) bool {
        // Simple glob matching
        if (std.mem.eql(u8, pattern, "*")) {
            return true;
        }

        if (std.mem.startsWith(u8, pattern, "*.")) {
            const extension = pattern[1..];
            return std.mem.endsWith(u8, path, extension);
        }

        if (std.mem.endsWith(u8, pattern, "/*")) {
            const dir_pattern = pattern[0 .. pattern.len - 2];
            return std.mem.startsWith(u8, path, dir_pattern);
        }

        return std.mem.containsAtLeast(u8, path, 1, pattern);
    }

    pub fn deinit(self: *Watcher) void {
        _ = self;
    }
};

pub fn watchDirectories(
    allocator: std.mem.Allocator,
    paths: [][]const u8,
    patterns: ?[][]const u8,
    ignore_patterns: ?[][]const u8,
    callback: *const fn (path: []const u8) anyerror!void,
) !void {
    var watcher = try Watcher.init(allocator, paths, patterns, ignore_patterns);
    try watcher.watch(callback);
    watcher.deinit();
}
