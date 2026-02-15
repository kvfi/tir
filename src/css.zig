const std = @import("std");

pub fn minify(allocator: std.mem.Allocator, css: []const u8) ![]u8 {
    var output = std.ArrayList(u8).init(allocator);

    var i: usize = 0;
    var in_comment = false;
    var in_string = false;
    var string_char: u8 = 0;
    var last_was_whitespace = false;

    while (i < css.len) {
        const char = css[i];

        // Handle comments
        if (!in_string and i + 1 < css.len and char == '/' and css[i + 1] == '*') {
            in_comment = true;
            i += 2;
            continue;
        }

        if (in_comment and i + 1 < css.len and char == '*' and css[i + 1] == '/') {
            in_comment = false;
            i += 2;
            continue;
        }

        if (in_comment) {
            i += 1;
            continue;
        }

        // Handle strings
        if ((char == '"' or char == '\'') and (i == 0 or css[i - 1] != '\\')) {
            if (!in_string) {
                in_string = true;
                string_char = char;
            } else if (char == string_char) {
                in_string = false;
            }
            try output.append(char);
            i += 1;
            last_was_whitespace = false;
            continue;
        }

        if (in_string) {
            try output.append(char);
            i += 1;
            continue;
        }

        // Handle whitespace
        if (char == ' ' or char == '\t' or char == '\n' or char == '\r') {
            if (!last_was_whitespace and output.items.len > 0) {
                const last_char = output.items[output.items.len - 1];
                // Only add space if needed (not after { or before })
                if (last_char != '{' and last_char != ':' and last_char != ',' and char != '}' and char != ';') {
                    try output.append(' ');
                }
            }
            last_was_whitespace = true;
            i += 1;
            continue;
        }

        // Remove space before {, }, ;, :
        if (last_was_whitespace and output.items.len > 0) {
            if (char == '{' or char == '}' or char == ';' or char == ':') {
                // Remove last space
                if (output.items[output.items.len - 1] == ' ') {
                    _ = output.pop();
                }
            }
        }

        try output.append(char);
        last_was_whitespace = false;
        i += 1;
    }

    // Trim trailing whitespace
    while (output.items.len > 0 and (output.items[output.items.len - 1] == ' ' or output.items[output.items.len - 1] == '\n')) {
        _ = output.pop();
    }

    return output.toOwnedSlice();
}

pub fn minifyFile(allocator: std.mem.Allocator, file_path: []const u8) ![]u8 {
    const file = try std.fs.cwd().openFile(file_path, .{});
    defer file.close();

    const content = try file.readToEndAlloc(allocator, 1024 * 1024);
    defer allocator.free(content);

    return try minify(allocator, content);
}
