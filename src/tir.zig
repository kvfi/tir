const std = @import("std");
const Config = @import("config.zig").Config;
const Post = @import("post.zig").Post;
const TemplateLoader = @import("templates.zig").TemplateLoader;
const utils = @import("utils.zig");

pub const Tir = struct {
    config: Config,
    allocator: std.mem.Allocator,
    theme_path: []const u8,
    content_dir: []const u8,
    posts_dir: []const u8,
    notes_dir: []const u8,

    pub fn init(allocator: std.mem.Allocator) !Tir {
        const cwd = try std.fs.cwd().realpath(".", &[_]u8{});
        defer allocator.free(cwd);

        // Load config from tir.yml
        var config = try Config.loadFromFile(allocator, "tir.yml");

        const theme = config.visuals.theme;
        const theme_path = try std.fmt.allocPrint(
            allocator,
            "{s}/layout/{s}",
            .{ cwd, theme },
        );

        const content_dir = try std.fmt.allocPrint(allocator, "{s}/content", .{cwd});
        const posts_dir = try std.fmt.allocPrint(allocator, "{s}/posts", .{content_dir});
        const notes_dir = try std.fmt.allocPrint(allocator, "{s}/notes", .{content_dir});

        return .{
            .config = config,
            .allocator = allocator,
            .theme_path = theme_path,
            .content_dir = content_dir,
            .posts_dir = posts_dir,
            .notes_dir = notes_dir,
        };
    }

    pub fn initProject(self: *Tir) !void {
        std.debug.print("Initializing Tir project...\n", .{});

        // Create required directories
        const required_dirs = [_][]const u8{
            "content",
            "content/posts",
            "content/notes",
            "layout/default/templates",
            "layout/default/assets/css",
            "layout/default/assets/images",
            "layout/default/assets/scripts",
        };

        for (required_dirs) |dir| {
            try std.fs.cwd().makePath(dir);
            std.debug.print("Created directory: {s}\n", .{dir});
        }

        // Create default tir.yml if it doesn't exist
        if (std.fs.cwd().openFile("tir.yml", .{})) |file| {
            file.close();
        } else |_| {
            const default_config =
                \\build_dir: html
                \\meta:
                \\  title: My Site
                \\  description: A Tir site
                \\navigation:
                \\  - link: /
                \\    title: Home
                \\visuals:
                \\  theme: default
                \\file_extension: html
                \\lang: en_US
            ;

            const file = try std.fs.cwd().createFile("tir.yml", .{});
            defer file.close();
            try file.writeAll(default_config);
        }

        // Create default index.html template
        const index_template =
            \\<!DOCTYPE html>
            \\<html>
            \\<head>
            \\  <title>{{ config.site.title }}</title>
            \\</head>
            \\<body>
            \\  <h1>Welcome to {{ config.site.title }}</h1>
            \\  {{ post.html_content }}
            \\</body>
            \\</html>
        ;

        const tpl_file = try std.fs.cwd().createFile("layout/default/templates/index.html", .{});
        defer tpl_file.close();
        try tpl_file.writeAll(index_template);

        const post_template =
            \\<!DOCTYPE html>
            \\<html>
            \\<head>
            \\  <title>{{ post.meta.title }}</title>
            \\</head>
            \\<body>
            \\  <h1>{{ post.meta.title }}</h1>
            \\  <div class="content">
            \\    {{ post.html_content }}
            \\  </div>
            \\</body>
            \\</html>
        ;

        const post_file = try std.fs.cwd().createFile("layout/default/templates/post.html", .{});
        defer post_file.close();
        try post_file.writeAll(post_template);

        std.debug.print("Tir project was successfully initialized.\n", .{});
    }

    pub fn build(self: *Tir, path: ?[]const u8) !void {
        std.debug.print("Building site...\n", .{});

        // Clean build directory if not rebuilding a single file
        if (path == null) {
            if (std.fs.cwd().openDir(self.config.build_dir, .{})) |dir| {
                dir.close();
                try std.fs.cwd().deleteTree(self.config.build_dir);
            } else |_| {}
        }

        // Create build directory
        try std.fs.cwd().makePath(self.config.build_dir);

        std.debug.print("Selected theme: {s}\n", .{self.config.visuals.theme});

        // Copy theme assets
        const assets_src = try std.fmt.allocPrint(
            self.allocator,
            "{s}/assets",
            .{self.theme_path},
        );
        defer self.allocator.free(assets_src);

        const assets_target = try std.fmt.allocPrint(
            self.allocator,
            "{s}/static",
            .{self.config.build_dir},
        );
        defer self.allocator.free(assets_target);

        std.debug.print("Building static files...\n", .{});
        try self.copyAssets(assets_src, assets_target);

        // Initialize template loader
        var tpl_loader = try TemplateLoader.init(
            self.allocator,
            self.theme_path,
            &self.config,
        );
        defer tpl_loader.deinit();

        // Process markdown posts
        std.debug.print("Building content...\n", .{});
        var posts = try self.scanPosts();
        defer {
            for (posts) |post| {
                post.deinit();
            }
            self.allocator.free(posts);
        }

        for (posts) |post| {
            try self.buildPost(post, tpl_loader);
        }

        std.debug.print("Build was successful.\n", .{});
    }

    fn copyAssets(self: *Tir, src: []const u8, target: []const u8) !void {
        try std.fs.cwd().makePath(target);

        // Simple recursive copy
        var dir = try std.fs.cwd().openDir(src, .{ .iterate = true });
        defer dir.close();

        var walker = try std.fs.cwd().walk(self.allocator);
        defer walker.deinit();

        var it = walker.walk();
        while (try it.next()) |entry| {
            if (entry.kind == .directory) {
                const target_path = try std.fmt.allocPrint(
                    self.allocator,
                    "{s}/{s}",
                    .{ target, entry.path },
                );
                defer self.allocator.free(target_path);
                try std.fs.cwd().makePath(target_path);
            } else if (entry.kind == .file) {
                const target_path = try std.fmt.allocPrint(
                    self.allocator,
                    "{s}/{s}",
                    .{ target, entry.path },
                );
                defer self.allocator.free(target_path);

                try std.fs.cwd().copyFile(entry.path, std.fs.cwd(), target_path, .{});
            }
        }
    }

    fn scanPosts(self: *Tir) ![]Post {
        var posts = std.ArrayList(Post).init(self.allocator);

        if (std.fs.cwd().openDir(self.posts_dir, .{ .iterate = true })) |dir| {
            defer dir.close();

            var walker = try std.fs.cwd().walk(self.allocator);
            defer walker.deinit();

            var it = walker.walk();
            while (try it.next()) |entry| {
                if (entry.kind == .file and std.mem.endsWith(u8, entry.path, ".md")) {
                    const full_path = try std.fmt.allocPrint(
                        self.allocator,
                        "{s}/{s}",
                        .{ self.posts_dir, entry.path },
                    );

                    const post = try Post.init(self.allocator, full_path);
                    try posts.append(post);
                }
            }
        } else |_| {}

        return posts.toOwnedSlice();
    }

    fn buildPost(self: *Tir, post: Post, tpl_loader: TemplateLoader) !void {
        if (post.meta == null) return;

        const meta = post.meta.?;
        const slug = meta.slug;
        const output_path = try std.fmt.allocPrint(
            self.allocator,
            "{s}/{s}{s}",
            .{ self.config.build_dir, slug, self.config.file_extension },
        );
        defer self.allocator.free(output_path);

        std.debug.print("Generating {s} from {s}...\n", .{ output_path, post.source });

        try post.write("post.html", output_path);
    }

    pub fn deinit(self: *Tir) void {
        self.allocator.free(self.theme_path);
        self.allocator.free(self.content_dir);
        self.allocator.free(self.posts_dir);
        self.allocator.free(self.notes_dir);
        self.config.deinit();
    }
};
