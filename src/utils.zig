const std = @import("std");

pub fn mktree(allocator: std.mem.Allocator, path: []const u8) !void {
    try std.fs.cwd().makePath(path);
}

pub fn scantree(
    allocator: std.mem.Allocator,
    path: []const u8,
    extension: ?[]const u8,
) !std.ArrayList([]u8) {
    var files = std.ArrayList([]u8).init(allocator);
    var walker = try std.fs.cwd().walk(allocator);
    defer walker.deinit();

    var it = walker.walk();
    while (try it.next()) |entry| {
        if (entry.kind == .file) {
            if (extension == null or std.mem.endsWith(u8, entry.path, extension.?)) {
                try files.append(try allocator.dupe(u8, entry.path));
            }
        }
    }

    return files;
}

pub fn toKebab(allocator: std.mem.Allocator, input: []const u8) ![]u8 {
    var result = std.ArrayList(u8).init(allocator);
    for (input) |char| {
        if (char == '_') {
            try result.append('-');
        } else {
            try result.append(char);
        }
    }
    return result.toOwnedSlice();
}

pub fn formatDate(input: []const u8) !?std.time.datetime.DateTime {
    // Parse YYYY/MM/DD format
    if (input.len != 10) return null;

    const year_str = input[0..4];
    const month_str = input[5..7];
    const day_str = input[8..10];

    const year = try std.fmt.parseInt(u16, year_str, 10);
    const month = try std.fmt.parseInt(u8, month_str, 10);
    const day = try std.fmt.parseInt(u8, day_str, 10);

    return std.time.datetime.DateTime{
        .year = year,
        .month = month,
        .day = day,
        .hour = 0,
        .minute = 0,
        .second = 0,
        .millisecond = 0,
    };
}

pub fn urlFor(route: []const u8, slug: ?[]const u8, filename: []const u8) []const u8 {
    if (std.mem.eql(u8, route, "index")) {
        return "/";
    } else if (std.mem.eql(u8, route, "post")) {
        // This is simplified - in reality would need to format the slug
        return slug orelse "";
    } else if (std.mem.eql(u8, route, "static")) {
        // Return "static/{filename}"
        return filename;
    }
    return "";
}

pub fn getDomain(url: []const u8, include_ext: bool) ![]u8 {
    // Simple URL parsing - extract domain from URL
    var result = std.ArrayList(u8).init(std.heap.page_allocator);

    // Skip protocol
    var start: usize = 0;
    if (std.mem.startsWith(u8, url, "http://")) {
        start = 7;
    } else if (std.mem.startsWith(u8, url, "https://")) {
        start = 8;
    }

    var end = start;
    while (end < url.len and url[end] != '/' and url[end] != ':') {
        end += 1;
    }

    const domain = url[start..end];
    var parts = std.mem.splitBackwardsSequence(u8, domain, ".");

    if (parts.next()) |part| {
        if (!include_ext) {
            if (parts.next()) |second_part| {
                try result.appendSlice(second_part);
            }
        } else {
            try result.appendSlice(domain);
        }
    }

    return result.toOwnedSlice();
}

pub fn hashContent(allocator: std.mem.Allocator, content: []const u8) ![32]u8 {
    var hash: [32]u8 = undefined;
    var hasher = std.crypto.hash.sha2.Sha256.init(.{});
    hasher.update(content);
    hasher.final(&hash);
    return hash;
}

pub fn removeListMeta(allocator: std.mem.Allocator, meta: std.StringHashMap([]const u8)) !std.StringHashMap([]const u8) {
    // In Python, this extracts first element of list items
    // For now, simplified implementation
    return meta;
}
