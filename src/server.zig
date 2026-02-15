const std = @import("std");
const net = std.net;

pub const Server = struct {
    allocator: std.mem.Allocator,
    port: u16 = 8000,
    host: []const u8 = "127.0.0.1",
    build_dir: []const u8,

    pub fn init(allocator: std.mem.Allocator, build_dir: []const u8) !Server {
        return .{
            .allocator = allocator,
            .build_dir = build_dir,
        };
    }

    pub fn run(self: *Server) !void {
        const address = try net.Address.parseIp(self.host, self.port);

        var server = try address.listen(.{
            .reuse_address = true,
        });
        defer server.deinit();

        std.debug.print("Starting server on http://{s}:{d}\n", .{ self.host, self.port });
        std.debug.print("Serving files from: {s}\n", .{self.build_dir});

        while (true) {
            const connection = try server.accept();
            defer connection.stream.close();

            try self.handleConnection(connection.stream);
        }
    }

    fn handleConnection(self: *Server, stream: net.Stream) !void {
        var buffer: [4096]u8 = undefined;
        const bytes_read = try stream.readAll(&buffer);

        if (bytes_read == 0) return;

        // Parse HTTP request
        var lines = std.mem.splitSequence(u8, buffer[0..bytes_read], "\r\n");
        const first_line = lines.next() orelse return;

        // Parse request line: GET /path HTTP/1.1
        var parts = std.mem.splitSequence(u8, first_line, " ");
        const method = parts.next() orelse return;
        const path = parts.next() orelse "/";

        std.debug.print("{s} {s}\n", .{ method, path });

        if (!std.mem.eql(u8, method, "GET")) {
            try sendResponse(stream, 405, "Method Not Allowed", "");
            return;
        }

        try self.serveFile(stream, path);
    }

    fn serveFile(self: *Server, stream: net.Stream, path: []const u8) !void {
        var file_path = std.ArrayList(u8).init(self.allocator);
        defer file_path.deinit();

        try file_path.appendSlice(self.build_dir);
        if (!std.mem.endsWith(u8, self.build_dir, "/")) {
            try file_path.append('/');
        }

        // Sanitize path
        var clean_path = std.ArrayList(u8).init(self.allocator);
        defer clean_path.deinit();

        for (path) |char| {
            if (char == '\\') {
                continue;
            }
            try clean_path.append(char);
        }

        if (std.mem.startsWith(u8, clean_path.items, "/")) {
            try file_path.appendSlice(clean_path.items[1..]);
        } else {
            try file_path.appendSlice(clean_path.items);
        }

        // Default to index.html for directories
        if (std.mem.endsWith(u8, file_path.items, "/")) {
            try file_path.appendSlice("index.html");
        }

        // Try to open the file
        const file = std.fs.cwd().openFile(file_path.items, .{}) catch |err| {
            try sendResponse(stream, 404, "Not Found", "");
            return;
        };
        defer file.close();

        const content = try file.readToEndAlloc(self.allocator, 1024 * 1024 * 10);
        defer self.allocator.free(content);

        const content_type = getContentType(file_path.items);
        try sendResponse(stream, 200, "OK", content);
    }

    fn getContentType(path: []const u8) []const u8 {
        if (std.mem.endsWith(u8, path, ".html")) {
            return "text/html";
        } else if (std.mem.endsWith(u8, path, ".css")) {
            return "text/css";
        } else if (std.mem.endsWith(u8, path, ".js")) {
            return "application/javascript";
        } else if (std.mem.endsWith(u8, path, ".json")) {
            return "application/json";
        } else if (std.mem.endsWith(u8, path, ".png")) {
            return "image/png";
        } else if (std.mem.endsWith(u8, path, ".jpg") or std.mem.endsWith(u8, path, ".jpeg")) {
            return "image/jpeg";
        } else if (std.mem.endsWith(u8, path, ".gif")) {
            return "image/gif";
        } else if (std.mem.endsWith(u8, path, ".svg")) {
            return "image/svg+xml";
        } else {
            return "text/plain";
        }
    }
};

fn sendResponse(stream: net.Stream, status_code: u16, status_text: []const u8, body: []const u8) !void {
    var response = std.ArrayList(u8).init(std.heap.page_allocator);
    defer response.deinit();

    try response.writer().print("HTTP/1.1 {} {s}\r\n", .{ status_code, status_text });
    try response.writer().print("Content-Length: {}\r\n", .{body.len});
    try response.writer().print("Content-Type: text/html\r\n", .{});
    try response.writer().writeAll("\r\n");
    try response.writer().writeAll(body);

    try stream.writeAll(response.items);
}

pub fn runServer(allocator: std.mem.Allocator, build_dir: []const u8) !void {
    var server = try Server.init(allocator, build_dir);
    try server.run();
}
