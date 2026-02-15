const std = @import("std");
const Config = @import("config.zig").Config;
const Post = @import("post.zig").Post;

pub const TemplateLoader = struct {
    layout_dir: []const u8,
    config: *const Config,
    allocator: std.mem.Allocator,

    pub fn init(allocator: std.mem.Allocator, layout_dir: []const u8, config: *const Config) !TemplateLoader {
        return .{
            .layout_dir = try allocator.dupe(u8, layout_dir),
            .config = config,
            .allocator = allocator,
        };
    }

    pub fn render(
        self: *TemplateLoader,
        template_name: []const u8,
        context: anytype,
    ) ![]u8 {
        // Load template file
        const template_path = try std.fmt.allocPrint(
            self.allocator,
            "{s}/templates/{s}",
            .{ self.layout_dir, template_name },
        );
        defer self.allocator.free(template_path);

        const file = try std.fs.cwd().openFile(template_path, .{});
        defer file.close();

        const template_content = try file.readToEndAlloc(self.allocator, 1024 * 1024);
        defer self.allocator.free(template_content);

        // For now, return the template content as-is
        // A real implementation would parse and render the template
        return try self.allocator.dupe(u8, template_content);
    }

    pub fn formatDate(self: *TemplateLoader, value: []const u8) []const u8 {
        // Simple date formatter
        return value;
    }

    pub fn urlFor(self: *TemplateLoader, route: []const u8, slug: ?[]const u8) []const u8 {
        if (std.mem.eql(u8, route, "index")) {
            return "/";
        } else if (std.mem.eql(u8, route, "post")) {
            return slug orelse "";
        }
        return "";
    }

    pub fn deinit(self: *TemplateLoader) void {
        self.allocator.free(self.layout_dir);
    }
};

pub fn renderTemplate(
    allocator: std.mem.Allocator,
    template: []const u8,
    context: anytype,
) ![]u8 {
    // Basic template rendering - substitute variables like {{variable}}
    var result = std.ArrayList(u8).init(allocator);

    var i: usize = 0;
    while (i < template.len) {
        if (i + 1 < template.len and template[i] == '{' and template[i + 1] == '{') {
            // Find closing }}
            var j = i + 2;
            while (j + 1 < template.len) {
                if (template[j] == '}' and template[j + 1] == '}') {
                    break;
                }
                j += 1;
            }

            if (j + 1 < template.len) {
                const var_name = std.mem.trim(u8, template[i + 2 .. j], " \t");
                // Try to get variable from context (simplified)
                try result.appendSlice("{{ ");
                try result.appendSlice(var_name);
                try result.appendSlice(" }}");
                i = j + 2;
                continue;
            }
        }

        try result.append(template[i]);
        i += 1;
    }

    return result.toOwnedSlice();
}
