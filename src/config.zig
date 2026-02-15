const std = @import("std");

pub const ConfigMeta = struct {
    description: []const u8,
    title: []const u8,
    copyright: ?[]const u8 = null,
};

pub const ConfigSite = struct {
    title: []const u8,
    tagline: ?[]const u8 = null,
};

pub const NavigationItem = struct {
    link: []const u8,
    title: []const u8,
};

pub const HomeContentElement = struct {
    name: []const u8,
    url: []const u8,
};

pub const HomeContent = struct {
    section: []const u8,
    elements: []HomeContentElement,
};

pub const Visuals = struct {
    theme: []const u8 = "default",
};

pub const Config = struct {
    build_dir: []const u8,
    meta: ConfigMeta,
    navigation: []NavigationItem = &[_]NavigationItem{},
    recent_post_counter: u32 = 5,
    home_content: []HomeContent = &[_]HomeContent{},
    visuals: Visuals = .{},
    file_extension: []const u8 = "html",
    lang: []const u8 = "en_US",
    working_dir: []const u8,

    allocator: std.mem.Allocator,

    pub fn loadFromFile(allocator: std.mem.Allocator, path: []const u8) !Config {
        const file = try std.fs.cwd().openFile(path, .{});
        defer file.close();

        const file_content = try file.readToEndAlloc(allocator, 1024 * 1024);
        defer allocator.free(file_content);

        // Parse YAML content manually (simplified YAML parser)
        var config: Config = .{
            .build_dir = "html",
            .meta = .{
                .description = "A Tir site",
                .title = "My Site",
            },
            .working_dir = try allocator.dupe(u8, "."),
            .allocator = allocator,
        };

        // Parse line by line
        var lines = std.mem.splitSequence(u8, file_content, "\n");
        var current_section: []const u8 = "";
        var nav_items = std.ArrayList(NavigationItem).init(allocator);
        var in_navigation = false;

        while (lines.next()) |line| {
            const trimmed = std.mem.trim(u8, line, " \t");
            if (trimmed.len == 0) continue;

            // Skip comments
            if (std.mem.startsWith(u8, trimmed, "#")) continue;

            // Parse top-level keys
            if (!std.mem.startsWith(u8, trimmed, " ")) {
                in_navigation = false;
                if (std.mem.indexOf(u8, trimmed, ":")) |colon_idx| {
                    const key = trimmed[0..colon_idx];
                    const value = std.mem.trim(u8, trimmed[colon_idx + 1 ..], " \t");

                    if (std.mem.eql(u8, key, "build_dir")) {
                        config.build_dir = try allocator.dupe(u8, value);
                    } else if (std.mem.eql(u8, key, "file_extension")) {
                        config.file_extension = try allocator.dupe(u8, value);
                    } else if (std.mem.eql(u8, key, "lang")) {
                        config.lang = try allocator.dupe(u8, value);
                    } else if (std.mem.eql(u8, key, "navigation")) {
                        in_navigation = true;
                    } else if (std.mem.eql(u8, key, "meta")) {
                        current_section = "meta";
                    } else if (std.mem.eql(u8, key, "visuals")) {
                        current_section = "visuals";
                    }
                }
            } else if (in_navigation and std.mem.startsWith(u8, trimmed, "- ")) {
                // Parse navigation items
                if (std.mem.indexOf(u8, trimmed, ":")) |colon_idx| {
                    const key = trimmed[2..colon_idx];
                    const value = std.mem.trim(u8, trimmed[colon_idx + 1 ..], " \t\"");

                    if (std.mem.eql(u8, key, "link")) {
                        if (nav_items.items.len == 0 or nav_items.items[nav_items.items.len - 1].title.len > 0) {
                            try nav_items.append(.{
                                .link = try allocator.dupe(u8, value),
                                .title = "",
                            });
                        } else {
                            nav_items.items[nav_items.items.len - 1].link = try allocator.dupe(u8, value);
                        }
                    }
                }
            } else if (std.mem.startsWith(u8, trimmed, "  ")) {
                // Parse nested values
                if (std.mem.indexOf(u8, trimmed, ":")) |colon_idx| {
                    const key = std.mem.trim(u8, trimmed[0..colon_idx], " \t");
                    const value = std.mem.trim(u8, trimmed[colon_idx + 1 ..], " \t\"");

                    if (std.mem.eql(u8, current_section, "meta")) {
                        if (std.mem.eql(u8, key, "title")) {
                            config.meta.title = try allocator.dupe(u8, value);
                        } else if (std.mem.eql(u8, key, "description")) {
                            config.meta.description = try allocator.dupe(u8, value);
                        } else if (std.mem.eql(u8, key, "copyright")) {
                            config.meta.copyright = try allocator.dupe(u8, value);
                        }
                    } else if (std.mem.eql(u8, current_section, "visuals")) {
                        if (std.mem.eql(u8, key, "theme")) {
                            config.visuals.theme = try allocator.dupe(u8, value);
                        }
                    }
                }
            }
        }

        if (nav_items.items.len > 0) {
            config.navigation = try nav_items.toOwnedSlice();
        }

        return config;
    }

    pub fn deinit(self: *Config) void {
        self.allocator.free(self.build_dir);
        self.allocator.free(self.meta.title);
        self.allocator.free(self.meta.description);
        if (self.meta.copyright) |copy| {
            self.allocator.free(copy);
        }
        for (self.navigation) |nav| {
            self.allocator.free(nav.link);
            self.allocator.free(nav.title);
        }
        self.allocator.free(self.navigation);
    }
};
