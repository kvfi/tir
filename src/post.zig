const std = @import("std");
const Config = @import("config.zig").Config;

pub const PostMeta = struct {
    title: []const u8 = "",
    slug: []const u8 = "",
    date: ?[]const u8 = null,
    created: ?[]const u8 = null,
    updated: ?[]const u8 = null,
    status: ?[]const u8 = null,
    confidence: ?[]const u8 = null,
    difficulty: ?[]const u8 = null,
    contents: ?[]const u8 = null,
};

pub const Post = struct {
    source: []const u8,
    target_path: ?[]const u8 = null,
    file_base_name: []const u8,
    meta: ?PostMeta = null,
    raw_content: []const u8 = "",
    html_content: []const u8 = "",
    allocator: std.mem.Allocator,

    pub fn init(allocator: std.mem.Allocator, source_path: []const u8) !Post {
        const file = try std.fs.cwd().openFile(source_path, .{});
        defer file.close();

        const raw_content = try file.readToEndAlloc(allocator, 1024 * 1024);

        const filename_start = std.mem.lastIndexOfScalar(u8, source_path, '/') orelse 0;
        const filename_with_ext = source_path[filename_start..];
        const dot_index = std.mem.lastIndexOfScalar(u8, filename_with_ext, '.') orelse filename_with_ext.len;
        const file_base_name = try allocator.dupe(u8, filename_with_ext[0..dot_index]);

        var post: Post = .{
            .source = try allocator.dupe(u8, source_path),
            .file_base_name = file_base_name,
            .raw_content = raw_content,
            .allocator = allocator,
        };

        try post.parse();
        return post;
    }

    pub fn parse(self: *Post) !void {
        if (self.raw_content.len == 0) return;

        // Parse YAML frontmatter if present
        self.meta = try self.extractMetadata();

        // Parse markdown to HTML using koino
        // For now, simplified implementation - just store raw content as HTML
        self.html_content = try self.allocator.dupe(u8, self.raw_content);
    }

    fn extractMetadata(self: *Post) !?PostMeta {
        // Check if content starts with --- for YAML frontmatter
        if (!std.mem.startsWith(u8, self.raw_content, "---")) {
            // No frontmatter, create minimal meta with slug from filename
            return PostMeta{
                .slug = try self.allocator.dupe(u8, self.file_base_name),
            };
        }

        // Find second --- delimiter
        const first_delimiter_end = "---".len;
        const content_after_first = self.raw_content[first_delimiter_end..];

        const second_delimiter_idx = std.mem.indexOf(u8, content_after_first, "---") orelse {
            return PostMeta{
                .slug = try self.allocator.dupe(u8, self.file_base_name),
            };
        };

        const frontmatter = content_after_first[0..second_delimiter_idx];
        var meta = PostMeta{
            .slug = try self.allocator.dupe(u8, self.file_base_name),
        };

        // Parse YAML frontmatter line by line
        var lines = std.mem.splitSequence(u8, frontmatter, "\n");
        while (lines.next()) |line| {
            const trimmed = std.mem.trim(u8, line, " \t");
            if (trimmed.len == 0) continue;

            const colon_idx = std.mem.indexOf(u8, trimmed, ":") orelse continue;
            const key = std.mem.trim(u8, trimmed[0..colon_idx], " \t");
            const value = std.mem.trim(u8, trimmed[colon_idx + 1 ..], " \t");

            if (std.mem.eql(u8, key, "title")) {
                meta.title = try self.allocator.dupe(u8, value);
            } else if (std.mem.eql(u8, key, "slug")) {
                meta.slug = try self.allocator.dupe(u8, value);
            } else if (std.mem.eql(u8, key, "date")) {
                meta.date = try self.allocator.dupe(u8, value);
            } else if (std.mem.eql(u8, key, "created")) {
                meta.created = try self.allocator.dupe(u8, value);
            } else if (std.mem.eql(u8, key, "updated")) {
                meta.updated = try self.allocator.dupe(u8, value);
            } else if (std.mem.eql(u8, key, "status")) {
                meta.status = try self.allocator.dupe(u8, value);
            } else if (std.mem.eql(u8, key, "confidence")) {
                meta.confidence = try self.allocator.dupe(u8, value);
            } else if (std.mem.eql(u8, key, "difficulty")) {
                meta.difficulty = try self.allocator.dupe(u8, value);
            }
        }

        // Extract content after frontmatter
        const content_start = first_delimiter_end + second_delimiter_idx + "---".len;
        self.raw_content = std.mem.trim(u8, self.raw_content[content_start..], " \t\n");

        return meta;
    }

    pub fn write(self: *Post, template_name: []const u8, output_path: []const u8) !void {
        const dir = std.fs.path.dirname(output_path) orelse ".";
        try std.fs.cwd().makePath(dir);

        const file = try std.fs.cwd().createFile(output_path, .{});
        defer file.close();

        // For now, write raw HTML content
        try file.writeAll(self.html_content);
    }

    pub fn deinit(self: *Post) void {
        self.allocator.free(self.source);
        self.allocator.free(self.file_base_name);
        self.allocator.free(self.raw_content);
        self.allocator.free(self.html_content);
        if (self.meta) |meta| {
            self.allocator.free(meta.title);
            self.allocator.free(meta.slug);
            if (meta.date) |d| self.allocator.free(d);
            if (meta.created) |c| self.allocator.free(c);
            if (meta.updated) |u| self.allocator.free(u);
            if (meta.status) |s| self.allocator.free(s);
            if (meta.confidence) |c| self.allocator.free(c);
            if (meta.difficulty) |d| self.allocator.free(d);
            if (meta.contents) |c| self.allocator.free(c);
        }
    }
};
